import base64
import requests

client_key = '8crHlv99DlNHF39R8kctDUs7D'
client_secret = 'XuGBuY1JnldHHgb8R4uVxvJtEG06uVOPIuAGjjRafDRjNFaqom'

key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

print(auth_resp.status_code)
print(auth_resp.json().keys())

access_token = auth_resp.json()['access_token']

print(access_token)