import asyncio
import base64
import json
from io import BytesIO

import aiohttp
from pdf2image import convert_from_path
from PIL import Image, ImageOps


async def main() -> None:
    image = convert_from_path('/tmp/0124.pdf', first_page=1, last_page=1, dpi=200)[0]
    image = image.convert('L')
    image = ImageOps.autocontrast(image)
    image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)

    buffer = BytesIO()
    image.save(buffer, format='PNG', optimize=True)
    b64_image = base64.b64encode(buffer.getvalue()).decode('ascii')


#    prompt_text = "Text Recognition: Please output the text information in the image according to the following JSON format:" \
#    "{\n" \
#    '   "PODate": "", \n' \
#    '   "PONumber": "", \n' \
#    '   "PartyGSTINNO": "", \n' \
#    '   "PartyName": "", \n' \
#    '   "BillNo": "", \n' \
#    '   "BillDate": "", \n' \
#    '   "VehicleNo": "", \n' \
#    '   "BranchName": "", \n' \
#    '   "DriverName": "", \n' \
#    '   "DriverConNo": "", \n' \
#    '   "PartyMasterAccNo": "", \n' \
#    '   "PartyMasterIFSCcode": "", \n' \
#    '   "AccountNo": "", \n' \
#    '   "IFSCCode": "", \n' \
#    '   "ItemDetails": [\n' \
#    '     {\n' \
#        '       "ItemName": "",\n' \
#        '       "unit": "",\n' \
#        '       "RemainingQty": "",\n' \
#        '       "PORate": "",\n' \
#        '       "gstper": "",\n' \
#        '       "BillRate": "",\n' \
#        '       "BillQty": "",\n' \
#        '       "NoOfPacking": "",\n' \
#        '       "BasicAmount": "",\n' \
#        '       "TotalBillAmount": ""\n' \
#        '     }\n' \
#    '   ]\n' \
#  '}\n' 
#    '  "invoice_number": "",\n' \
#    '  "invoice_date": "",\n' \
#    '  "total_amount": ""\n' \
#    "}\n" \
    #"If any field is missing or cannot be extracted, set its value to null. Do
#        'prompt': 'Table Recognition: Consider the whole invoice as a big complex table with or without headings and format all the content into a meaningful complex table',
    payload = {
        'model': 'glm-ocr:latest',
        'prompt': """Text Recognition: Extract all text from this invoice and return in Markdown, omiting any content in table format.
Preserve reading order, emphasize structures like bolding, headers, tables formatting and section/grouping as much as possible.
Return only Markdown.""",
    #    'prompt': prompt_text,
        'images': [b64_image],
        'stream': False,
        'temperature': 0.8,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://host.docker.internal:11434/api/generate',
            json=payload,
            timeout=aiohttp.ClientTimeout(total=180),
        ) as response:
            raw_text = await response.text()
        #    print(f'Prompt: {prompt_text}')
            print(f'STATUS: {response.status}')
            print('RAW_RESPONSE_START')
            print(raw_text)
            print('RAW_RESPONSE_END')
            try:
                parsed = json.loads(raw_text)
                print('PARSED_RESPONSE_FIELD_START')
                print(parsed.get('response'))
                print('PARSED_RESPONSE_FIELD_END')
            except json.JSONDecodeError:
                pass


if __name__ == '__main__':
    asyncio.run(main())
