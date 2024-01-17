from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from variables import BASE_URL, TENANT_ID, CLIENT_ID, CLIENT_SECRET, CLIENT_NAME, PROJECT_NAME


creds = OAuthClientCredentials(
    token_url=f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scopes=[f"{BASE_URL}/.default"]
)

cnf = ClientConfig(
    client_name=CLIENT_NAME,
    project=PROJECT_NAME,
    credentials=creds,
    base_url=BASE_URL
)

client = CogniteClient(cnf)