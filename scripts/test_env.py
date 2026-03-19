from dotenv import dotenv_values
import pprint
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'
print('loading', env_path)
data = dotenv_values(env_path)
pprint.pprint(data)
