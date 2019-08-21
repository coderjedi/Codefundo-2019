from adal import AuthenticationContext
import requests
from pprint import pprint
import json

AUTHORITY = 'https://login.microsoftonline.com/chiragvmj2012gmail.onmicrosoft.com'
WORKBENCH_API_URL = 'https://safevote-3wpvhp.azurewebsites.net'
RESOURCE = '9569b296-589d-488b-a582-246d957827de'
CLIENT_APP_Id = 'b4d34ae7-b24d-4aab-87a5-a72c23d60dec'
CLIENT_SECRET = '.M-m0UajsaeD*uCc6@WlLigK5oVMPbj8'

auth_context = AuthenticationContext(AUTHORITY)

if __name__ == '__main__':
    try:
        # Acquiring the token
        token = auth_context.acquire_token_with_client_credentials(
            RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
        # print(token['accessToken'])
        endpoint = 'https://safevote-3wpvhp-api.azurewebsites.net/api/v2/36/actions'
        url = endpoint
        headers = {'Authorization': 'Bearer ' + token['accessToken']}
        response = requests.get(url, headers=headers)
        mydata=json.loads(response.text)
        print(mydata["nextLink"])
    except Exception as error:
        print(error)
