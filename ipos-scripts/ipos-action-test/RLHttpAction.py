#!/usr/bin/env python
#coding=utf8
import httplib
import urllib
import thread
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
class RLHttpAction:
	def __init__(self,actionURL=''):
		self.actionNUM = 1
		self.serverURL = None
		self.app = None
		self.actionURL = actionURL
		self.responseData = None
		self.requestData = None
		self.port  = 443
		self.timeout = 60
		self.headers = {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}

		self.loadServerInfo()
		print self.serverURL,self.app

	def loadServerInfo(self):
		files = open('server.txt','r')
		dic = {}
		for line in files:
			line = line.strip()
			arr = line.split(':')
			dic[arr[0]] = arr[1]
		self.serverURL = dic['server']
		self.app = dic['app']

	def run(self):
		self.runWithRequestData(self.requestData)

	def runWithRequestData(self,data):
		httpClient = None
		print 'POST %s/%s%s' %(self.serverURL,self.app,self.actionURL)
		print 'with '+ str(data)
		try:
			appActionURL = '/%s%s' % (self.app,self.actionURL)
			print appActionURL
			params = urllib.urlencode(data)
			httpClient = httplib.HTTPSConnection(self.serverURL,self.port,timeout=self.timeout)
			httpClient.request('POST',appActionURL,params,self.headers)
			response = httpClient.getresponse()
			print response.status
			print response.reason
			print response.getheaders()
			self.responseData =response.read()
			print self.responseData
		except Exception,e:
			print e
		finally:
			if httpClient:
				httpClient.close()

	def asyncRun(self):
		self.asyncRunWithRequestData(data)

	def asyncRunWithRequestData(self,data):
		thread.start_new_thread(self.runWithRequestData,(self,data))

		

if __name__ == '__main__':
	action = RLHttpAction()
	action.actionURL = '/terminal/GetTerminalInfo.action'
	data = {'accesskey':'123ABC','clientid':'1','firmverion':'0x0118','serialno':'1','terminalType':'1','clienttime':'2015-11-06 16:43:52'}
	action.runWithRequestData(data)
	
