from paddleocr import PaddleOCR
import json

ocr = PaddleOCR()
results = ocr.predict('D:\\Documents\\0124.pdf')

print(f"Results type: {type(results)}")
print(f"Results length: {len(results) if hasattr(results, '__len__') else 'N/A'}")

if hasattr(results, '__iter__'):
    for i, page in enumerate(results):
        print(f"\nPage {i} type: {type(page)}")
        print(f"Page {i} attributes: {dir(page)}")
        print(f"Page {i} has .json attr: {hasattr(page, 'json')}")
        
        # Try accessing json as a property
        if hasattr(page, 'json'):
            json_val = page.json
            print(f"Page {i} .json type: {type(json_val)}")
            print(f"Page {i} .json value: {json_val if isinstance(json_val, str) else 'Not a string'}")
        
        # Try accessing as dict keys
        if hasattr(page, 'keys'):
            print(f"Page {i} keys: {page.keys()}")
        
        break  # Just check first page
