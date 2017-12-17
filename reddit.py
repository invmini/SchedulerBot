#!/usr/bin/python

import requests
import requests.auth
import sys,argparse

class Reddit():

	client_auth = None
	headers = {"User-Agent":"script/SchedulerBot/v0.1 by u/dihydrogen_oxide"}
	token = None
	client_id = "NVIMJV1nueHicg"
	client_secret = None
	debug = False
	username = None
	password = None

	def obtain_sub_settings(self,sub):

		settings =(self.get("r/"+sub+"/about/edit.json",{},True)).json()["data"]

		return settings

	def set_sub_settings(self,desc):

		return self.post("api/site_admin/",desc,True)

	def request_new_token(self):

		if self.client_secret is not None:

			self.client_auth = requests.auth.HTTPBasicAuth(self.client_id,self.client_secret)
			post_data = {"grant_type":"password","username":self.username,"password":self.password}
			url = "api/v1/access_token"

			response = self.post(url, post_data, auth=self.client_auth)

			self.token = (response.json())["access_token"]
		else:
			print "Client secret not set"

	def revoke_token(self):

		if self.token is not None:

			response = self.post("api/v1/revoke_token", {"token":self.token}, oauth=False, auth=self.client_auth)

			return True if response.status_code == 204 else False

		else:

			print "No token to revoke"

			return True

	def post(self,url,data,oauth=False,auth=None):

		api_url = "https://www.reddit.com/"+url
		if self.token is not None and oauth:
			data["token"] = self.token
			data["grant_type"] = "client_credentials"
			api_url = "https://oauth.reddit.com/"+url
			self.headers["Authorization"] = "bearer " + self.token

		res = requests.post(api_url, auth=auth, data=data, headers=self.headers)

		if self.debug:

			res_str = ""

			try:
				res_str = "\n=====POST\nURL: "+api_url+"\nHeader: "+ str(self.headers)+ "\nData: "+str(data)+"\nResponse: "+str(res)+"\nJSON: "+str(res.json())+"\n=====\n"
			except:
				res_str = "\n=====POST\nURL: "+api_url+"\nHeader: "+ str(self.headers)+ "\nData: "+str(data)+"\nResponse: "+str(res)+"\n=====\n"

			print res_str

		return res

	def get(self,url,data,oauth=False):

		api_url = "https://www.reddit.com/"+url
		if self.token is not None and oauth:
			data = {}
			data["token"] = self.token
			api_url = "https://oauth.reddit.com/"+url
			self.headers.update({"Authorization": "bearer " + self.token})

		res = requests.get(api_url, headers=self.headers)

		if self.debug:

			try:
				res_str = "\n=====GET\nURL: "+api_url+"\nHeader: "+ str(self.headers)+ "\nData: "+str(data)+"\nResponse: "+str(res)+"\nJSON: "+str(res.json())+"\n=====\n"
			except:
				res_str = "\n=====GET\nURL: "+api_url+"\nHeader: "+ str(self.headers)+ "\nData: "+str(data)+"\nResponse: "+str(res)+"\n=====\n"

			print res_str

		return res

def main():

	reddit = Reddit()
	reddit.debug = True

	args = argparse.ArgumentParser()
	args.add_argument('--new',action='store_true',dest='new_token',help='Generate new OAuth token')
	args.add_argument('--revoke',type=str,dest='revoke_token',help='Revoke OAuth token')
	args.add_argument('--client_id',action='store_true',dest='client_id',help='Generate new OAuth token')
	#args.add_argument('',action='store_true',dest='',help='')
	args.add_argument('--username',type=str,dest='username',help='account username')
	args.add_argument('--password',type=str,dest='password',help='account password')
	args.add_argument('--secret',type=str,dest='secret',help='app secret')

	option = args.parse_args()

	if option.username == None or option.password == None and option.secret == None:
		print "Username, password, and/or secret not given"
		return
	else:
		reddit.username = option.username
		reddit.password = option.password
		reddit.secret = option.secret

	if option.new_token:
		reddit.request_new_token()
		print reddit.token

	elif option.revoke_token is not None:
		print reddit.revoke_token(option.revoke_token)

	elif option.client_id:
		print reddit.client_id()

	else:
		print "invalid arguments given"

	if reddit.token is not None:
		print reddit.revoke_token()

if __name__ == "__main__":
	main()
