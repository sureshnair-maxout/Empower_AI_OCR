"""
Generic field extractor using pre-extracted OCR layout data + LLM spatial reasoning.

This script takes OCR layout JSON as input and uses LLM to extract fields
without hardcoded patterns - purely using spatial heuristics.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import ollama


def load_ocr_layout(json_path: Path) -> List[Dict]:
    """
    Load OCR layout data from JSON file.
    
    Expected format: List of dicts with 'text', 'bbox', 'confidence' keys
    or a dict with 'extracted_text' or 'lines' key containing the list.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle different JSON formats
    if isinstance(data, list):
        lines = data
    elif isinstance(data, dict):
        if 'extracted_text' in data:
            lines = data['extracted_text']
        elif 'lines' in data:
            lines = data['lines']
        else:
            raise ValueError("JSON format not recognized. Expected list or dict with 'extracted_text'/'lines' key")
    else:
        raise ValueError("JSON format not recognized")
    
    # Calculate center coordinates if not present
    for line in lines:
        if 'cx' not in line or 'cy' not in line:
            bbox = line['bbox']
            if len(bbox) == 4 and isinstance(bbox[0], (int, float)):
                # Format: [x1, y1, x2, y2]
                line['cx'] = (bbox[0] + bbox[2]) / 2
                line['cy'] = (bbox[1] + bbox[3]) / 2
            elif len(bbox) >= 4 and isinstance(bbox[0], list):
                # Format: [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                line['cx'] = sum(p[0] for p in bbox[:4]) / 4
                line['cy'] = sum(p[1] for p in bbox[:4]) / 4
    
    return lines


def build_layout_context(lines: List[Dict]) -> str:
    """Build a structured representation of the layout for the LLM."""
    # Sort by vertical position (top to bottom), then horizontal (left to right)
    sorted_lines = sorted(lines, key=lambda l: (l.get('cy', 0), l.get('cx', 0)))
    
    layout_text = "DOCUMENT LAYOUT (sorted top-to-bottom, left-to-right):\n\n"
    
    for idx, line in enumerate(sorted_lines, 1):
        bbox = line['bbox']
        
        # Handle different bbox formats
        if len(bbox) == 4 and isinstance(bbox[0], (int, float)):
            x1, y1, x2, y2 = bbox
        else:
            xs = [p[0] for p in bbox]
            ys = [p[1] for p in bbox]
            x1, y1, x2, y2 = min(xs), min(ys), max(xs), max(ys)
        
        layout_text += f"[{idx}] Text: \"{line['text']}\"\n"
        layout_text += f"    Position: x={int(x1)}-{int(x2)}, y={int(y1)}-{int(y2)}\n"
        layout_text +=f"    Center: ({int(line.get('cx', 0))}, {int(line.get('cy', 0))})\n\n"
    
    return layout_text


def build_llm_prompt(lines: List[Dict], fields: List[str]) -> str:
    """Build the prompt for the LLM with layout information and extraction task."""
    layout_context = build_layout_context(lines)
    
    prompt = f"""You are analyzing an invoice document. Each text element below has its position (x, y coordinates).

{layout_context}

Extract these fields:
{json.dumps({field: "" for field in fields}, indent=2)}

SPATIAL MATCHING RULES:
1. Find the LABEL first (e.g., "Invoice No:", "IRN:", "Date:", "Seller:", "Buyer:", "Total:")
2. The VALUE is usually:
   - To the RIGHT of the label (similar y-coordinate, higher x-coordinate)
   - BELOW the label (similar x-coordinate, higher y-coordinate)
3. Two elements are on the SAME LINE if their y-coordinates are within 20 pixels

FIELD-SPECIFIC HINTS (generic patterns):
- invoice_number: Near "Invoice No" label, format varies (e.g., XX-XX/XXXX, or just numbers)
- irn: Near "IRN" label, usually a long alphanumeric/hex string (30+ chars)
- invoice_date: Near "Date" or "Dated" label, date format (e.g., DD-MMM-YY, DD/MM/YYYY)
- seller_name: Near "Seller" label, usually a company name
- buyer_name: Near "Buyer" or "Billed To" label, company name
- total_amount: Near "Total" or "Grand Total" label, numeric value
- currency: Usually "INR", "USD", etc., near amount fields

Return ONLY the JSON object with extracted values:
"""
    
    return prompt


def extract_fields_with_llm(
    lines: List[Dict],
    fields: List[str],
    model: str = 'llama3.2:3b',
) -> Dict[str, Any]:
    """Extract fields using LLM with layout-aware prompting."""
    print(f"Sending layout data to {model} for field extraction...")
    print(f"Total text lines: {len(lines)}")
    print(f"Text Lines: {lines[:5]} ...")  # Print first 5 lines for debugging
    print(f"Fields: {fields[:5]} ...")  # Print first 5 fields for debugging
    
    prompt = build_llm_prompt(lines, fields)
    
    print(f"PROMPT: {prompt[:500]} ...")  # Print first 500 characters of the prompt for debugging
    response = ollama.chat(
        model=model,
        messages=[{
            'role': 'system',
            'content': 'You are a JSON extraction API. Return ONLY valid JSON, no markdown, no explanations.',
        }, {
            'role': 'user',
            'content': prompt,
        }],
        options={
            'temperature': 0.5,  #Moderate temperature for balanced extraction
            'num_predict': 500,
        },
        format='json',  # Request JSON format from Ollama
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
        description='Extract invoice fields from OCR layout JSON using LLM spatial reasoning'
    )
    parser.add_argument(
        '--layout',
        type=Path,
        required=True,
        help='Path to OCR layout JSON file'
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
        '--output',
        type=Path,
        default='extracted_fields.json',
        help='Output JSON file path (default: extracted_fields.json)'
    )
    
    args = parser.parse_args()
    
    if not args.layout.exists():
        print(f"Error: Layout file not found: {args.layout}")
        return 1
    
    try:
        # Step 1: Load OCR layout data
        print(f"Loading OCR layout from {args.layout}...")
        ocr_lines = load_ocr_layout(args.layout)
        print(f"Loaded {len(ocr_lines)} text lines")
        
        if not ocr_lines:
            print("Error: No text lines in layout data")
            return 1
        
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
