"""
Generic invoice field extraction using PaddleOCR layout + LLM spatial reasoning.

This script extracts text with layout information using PaddleOCR, then provides
it to an LLM (llama3.2:3b) to perform heuristic neighbor matching and field extraction
without hardcoded patterns.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, TypedDict

import ollama
from paddleocr import PaddleOCR


class OCRLine(TypedDict):
    """Represents a single line of OCR output with layout info."""
    text: str
    bbox: List[List[float]]  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    confidence: float
    cx: float  # center x
    cy: float  # center y


def run_paddle_ocr(file_path: Path, lang: str = 'en') -> List[OCRLine]:
    """
    Run PaddleOCR basic extraction to get text with layout information.
    
    Args:
        file_path: Path to the image or PDF file
        lang: Language code for OCR (default: 'en')
    
    Returns:
        List of OCR lines with text, bounding boxes, and positions
    """
    print(f"Running PaddleOCR on {file_path}...")
    
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        lang=lang,
    )
    
    results = ocr.predict(str(file_path))
    
    ocr_lines: List[OCRLine] = []
    
    for page_idx, page in enumerate(results):
        print(f"Processing page {page_idx}, type: {type(page)}")
        print(f"Has .json attr: {hasattr(page, 'json')}")
        
        if not hasattr(page, 'json'):
            print(f"Page has no .json attribute, skipping")
            continue
        
        print(f"Page.json length: {len(page.json)}")
        
        for line_idx, line in enumerate(page.json):
            # Debug first line
            if line_idx == 0:
                print(f"First line type: {type(line)}")
                print(f"First line content: {line}")
            
            # line is a dict with 'text', 'bbox', 'score' keys
            if isinstance(line, str):
                continue  # Skip if line is somehow a string
            
            text = line.get('text', '')
            confidence = line.get('score', 0.0)
            bbox_raw = line.get('bbox', [])
            
            # bbox might be in different formats, normalize to [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
            if len(bbox_raw) == 4 and isinstance(bbox_raw[0], (int, float)):
                # Format: [x1, y1, x2, y2] -> convert to 4 corners
                x1, y1, x2, y2 = bbox_raw
                bbox = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
            else:
                bbox = bbox_raw
            
            # Calculate center point
            if len(bbox) >= 4:
                cx = sum(point[0] for point in bbox[:4]) / 4
                cy = sum(point[1] for point in bbox[:4]) / 4
            else:
                cx, cy = 0, 0
            
            ocr_lines.append({
                'text': text,
                'bbox': bbox,
                'confidence': confidence,
                'cx': cx,
                'cy': cy,
            })
    
    print(f"Extracted {len(ocr_lines)} text lines")
    return ocr_lines


def build_layout_context(lines: List[OCRLine]) -> str:
    """
    Build a structured representation of the layout for the LLM.
    
    Args:
        lines: List of OCR lines with layout information
    
    Returns:
        Formatted string describing the layout
    """
    # Sort by vertical position (top to bottom), then horizontal (left to right)
    sorted_lines = sorted(lines, key=lambda l: (l['cy'], l['cx']))
    
    layout_text = "DOCUMENT LAYOUT (sorted top-to-bottom, left-to-right):\n\n"
    
    for idx, line in enumerate(sorted_lines, 1):
        bbox = line['bbox']
        x1, y1 = bbox[0]
        x2, y2 = bbox[2]
        
        layout_text += f"[{idx}] Text: \"{line['text']}\"\n"
        layout_text += f"    Position: x={int(x1)}-{int(x2)}, y={int(y1)}-{int(y2)}\n"
        layout_text += f"    Center: ({int(line['cx'])}, {int(line['cy'])})\n\n"
    
    return layout_text


def build_llm_prompt(lines: List[OCRLine], fields: List[str]) -> str:
    """
    Build the prompt for the LLM with layout information and extraction task.
    
    Args:
        lines: List of OCR lines with layout information
        fields: List of field names to extract
    
    Returns:
        Formatted prompt string
    """
    layout_context = build_layout_context(lines)
    
    prompt = f"""You are an expert document analyzer. I will provide you with the complete text content of an invoice along with precise layout information (bounding boxes and positions).

Your task is to extract specific fields using SPATIAL HEURISTIC NEIGHBOR MATCHING:

1. Look for label text (e.g., "Invoice No:", "Date:", "Total:")
2. Find the corresponding value by checking nearby text elements
3. Use spatial relationships:
   - Values are typically to the RIGHT of labels (same horizontal line)
   - Values may be BELOW labels (vertically aligned)
   - Consider proximity (center coordinates) to match labels with values

{layout_context}

FIELDS TO EXTRACT:
{json.dumps(fields, indent=2)}

INSTRUCTIONS:
- Use the position information to match labels with their values
- For each field, identify the label text first, then find the nearest value
- If a field cannot be found, return null for that field
- Return ONLY valid JSON with no additional text

OUTPUT FORMAT (JSON only):
{{
"""
    
    for field in fields:
        prompt += f'  "{field}": "",\n'
    
    prompt = prompt.rstrip(',\n') + '\n}\n'
    
    return prompt


def extract_fields_with_llm(
    lines: List[OCRLine],
    fields: List[str],
    model: str = 'llama3.2:3b',
) -> Dict[str, Any]:
    """
    Extract fields using LLM with layout-aware prompting.
    
    Args:
        lines: List of OCR lines with layout information
        fields: List of field names to extract
        model: Ollama model name
    
    Returns:
        Dictionary with extracted field values
    """
    print(f"Sending layout data to {model} for field extraction...")
    
    prompt = build_llm_prompt(lines, fields)
    
    response = ollama.chat(
        model=model,
        messages=[{
            'role': 'user',
            'content': prompt,
        }],
        options={
            'temperature': 0.1,  # Low temperature for consistent extraction
            'num_predict': 1000,
        },
    )
    
    content = response['message']['content'].strip()
    
    # Try to parse JSON from response
    try:
        # Remove markdown code blocks if present
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
            content = content.strip()
        
        result = json.loads(content)
        print("Successfully extracted fields")
        return result
    
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse LLM response as JSON: {e}")
        print(f"Raw response:\n{content}")
        
        # Return empty dict with null values
        return {field: None for field in fields}


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Extract invoice fields using PaddleOCR layout + LLM spatial reasoning'
    )
    parser.add_argument(
        '--file',
        type=Path,
        required=True,
        help='Path to invoice image or PDF file'
    )
    parser.add_argument(
        '--fields',
        nargs='+',
        default=[
            'invoice_number',
            'irn',
            'invoice_date',
            'seller_name',
            'buyer_name',
            'total_amount',
            'currency',
        ],
        help='List of fields to extract (default: common invoice fields)'
    )
    parser.add_argument(
        '--model',
        default='llama3.2:3b',
        help='Ollama model name (default: llama3.2:3b)'
    )
    parser.add_argument(
        '--lang',
        default='en',
        help='OCR language (default: en)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=None,
        help='Output JSON file path (default: <input>_extracted.json)'
    )
    parser.add_argument(
        '--save-layout',
        type=Path,
        default=None,
        help='Save raw OCR layout data to this file'
    )
    
    args = parser.parse_args()
    
    if not args.file.exists():
        print(f"Error: File not found: {args.file}")
        return 1
    
    # Set default output path
    if args.output is None:
        args.output = args.file.parent / f"{args.file.stem}_extracted.json"
    
    try:
        # Step 1: Extract text with layout using PaddleOCR
        ocr_lines = run_paddle_ocr(args.file, args.lang)
        
        if not ocr_lines:
            print("Error: No text extracted from document")
            return 1
        
        # Save layout data if requested
        if args.save_layout:
            with open(args.save_layout, 'w', encoding='utf-8') as f:
                json.dump(ocr_lines, f, indent=2, ensure_ascii=False)
            print(f"Saved layout data to {args.save_layout}")
        
        # Step 2: Extract fields using LLM with spatial reasoning
        extracted_fields = extract_fields_with_llm(
            ocr_lines,
            args.fields,
            args.model,
        )
        
        # Step 3: Save results
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(extracted_fields, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print("EXTRACTION RESULTS:")
        print('='*60)
        print(json.dumps(extracted_fields, indent=2, ensure_ascii=False))
        print('='*60)
        print(f"\nSaved to: {args.output}")
        
        return 0
    
    except Exception as e:
        print(f"Error during extraction: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
