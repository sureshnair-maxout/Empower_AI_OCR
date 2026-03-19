from dotenv import load_dotenv, dotenv_values
from pathlib import Path
import os, sys
sys.path.append(str(Path(__file__).parent.parent))

print('dotenv_values:', dotenv_values(Path(__file__).parent.parent / '.env').get('DATABASE_URL'))

load_dotenv(Path(__file__).parent.parent / '.env')
print('os env after load:', repr(os.getenv('DATABASE_URL')))
