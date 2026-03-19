from dotenv import load_dotenv
load_dotenv()
import os, sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
print('os env', os.environ.get('DATABASE_URL'))
from app.core.config import Settings
s=Settings()
print('settings', s.database_url)

# try again constructing one more to ensure validator runs twice
s2 = Settings()
print('settings2', s2.database_url)
