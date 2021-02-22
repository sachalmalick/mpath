import requests
import json
import pickle
import base64
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth

URL_BASE = "https://api-m.sandbox.paypal.com"
OAUTH_URL = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
ACCESS_TOKEN = ""
CLIENT_ID = "AVpyDcyLmcag_yZHQNTXclWAqDm-JCryjogfllt_PmEbf24UiOUsNvUEYQKryDWYbGvJf3wAb0iPHfzf"
CLIENT_SECRET = "EENJqgjUxuiOX9WgmYfpVQ-Dtd_WbJLv1tbZ2CuOroraf-G0MaX9_QBUvt-_mywEDNq56ngeXROWxhyL"

MERCHANT_ID = ""

def get_header(access_token):
	return {"Authorization": "Bearer {}".format(access_token),"Content-Type": "application/json"}


def get_jwt():
	
	jose_header = {"alg": "none"}
	payload = {"iss": CLIENT_ID,"payer_id": MERCHANT_ID}
	signature = ""
	
	headerstr = base64.urlsafe_b64encode(json.dumps(jose_header).encode())
	headerstr = headerstr.decode("utf-8")
	
	payloadstr = base64.urlsafe_b64encode(json.dumps(payload).encode())
	payloadstr = payloadstr.decode("utf-8")
	
	signaturestr = base64.urlsafe_b64encode(signature.encode())
	signaturestr = signaturestr.decode()
	
	return "{}.{}.{}".format(headerstr, payloadstr, signaturestr)

def get_request(url, payload, merchant=False):
	header = get_header(ACCESS_TOKEN)
	if(merchant):
		header["PayPal-Auth-Assertion"] = get_jwt()
	print(header)
	return requests.get(url, data=payload, headers=header).text

"""curl -v https://api-m.sandbox.paypal.com/v1/oauth2/token \
  -H "Accept: application/json" \
  -H "Accept-Language: en_US" \
  -u "AVpyDcyLmcag_yZHQNTXclWAqDm-JCryjogfllt_PmEbf24UiOUsNvUEYQKryDWYbGvJf3wAb0iPHfzf:EENJqgjUxuiOX9WgmYfpVQ-Dtd_WbJLv1tbZ2CuOroraf-G0MaX9_QBUvt-_mywEDNq56ngeXROWxhyL" \
  -d "grant_type=client_credentials"
"""
def get_access_token():
	auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
	client = BackendApplicationClient(client_id=CLIENT_ID)
	oauth = OAuth2Session(client=client)
	token = oauth.fetch_token(token_url=OAUTH_URL, auth=auth)
	return oauth, token
	
class PayPalConnector:
	def __init__(self):
		self.oauth, self.token = get_access_token()
	def refresh_token(self):
		self.oauth, self.token = get_access_token()
	def header(self):
		return {"Accept" : "application/json", "Authorization": "Bearer {}".format(self.token["access_token"]),"Content-Type": "application/json"}
	def process_get(self, url, data, merchant=False):
		try:
			header = self.header()
			if(merchant):
				header["PayPal-Auth-Assertion"] = get_jwt()
			print(header)
			result = self.oauth.get(url, data=data, headers=header)
			return result.text
		except TokenExpiredError as tee:
			print("token expired")
			result = self.oauth.get(url, data=data, headers=header)
			return result.text
	def list_transactions(self, tag):
		url = URL_BASE + "/v1/reporting/transactions?transaction_amount=33.30"
		print(self.process_get(url, {}))
		
	
#curl -v -X GET https://api-m.sandbox.paypal.com/v2/payments/authorizations/4EY91394TC2395244 \
#-H "Content-Type: application/json" \
#-H "Authorization: Bearer A21AAIx2w-4kJ9edz_AWfwwz34Sxf5irNu4JGqG-DyXt_G67_ZOLd9x1aNmDa03--8FNj2kTD4AwGGi39a8FeU6jR9emvjIog"
#
#
#"4EY91394TC2395244"


connector = PayPalConnector()
#connector.list_transactions("nothing")
ACCESS_TOKEN = connector.token["access_token"]
print(ACCESS_TOKEN)
#print(get_request("https://api-m.sandbox.paypal.com/v1/reporting/transactions?start_date=2014-07-01T00:00:00-0700&end_date=2014-07-30T23:59:59-0700&transaction_id=5TY05013RG002845M&fields=all&page_size=100&page=1", {}))
#
#curl -v -X GET https://api-m.sandbox.paypal.com/v1/reporting/transactions?start_date=2014-07-01T00:00:00-0700&end_date=2014-07-30T23:59:59-0700&transaction_id=5TY05013RG002845M&fields=all&page_size=100&page=1 \
#-H "Content-Type: application/json" \
#-H "Authorization: Bearer A21AAIx2w-4kJ9edz_AWfwwz34Sxf5irNu4JGqG-DyXt_G67_ZOLd9x1aNmDa03--8FNj2kTD4AwGGi39a8FeU6jR9emvjIog"
#
