import toml
import json
from google.oauth2.credentials import Credentials

CREDS_PATH = "./secrets/secrets.toml"

with open(CREDS_PATH, 'r') as f:
    secrets = toml.load(f)

# Access values from the config
#print(secrets["installed"])
#print(secrets["token"])
#json_object = json.dumps(secrets)

# Print JSON object
#print(json_object)

creds = Credentials.from_authorized_user_info(secrets["token"])
print(creds)