import os
from dotenv import load_dotenv
from pathlib import Path

# load manually
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path, override=True)
print('env raw after load', os.getenv('DATABASE_URL'))

import sys
sys.path.append(str(Path(__file__).parent.parent))
from app.core.config import Settings
s = Settings()
print('settings.database_url', s.database_url)
print('env raw now', os.getenv('DATABASE_URL'))
