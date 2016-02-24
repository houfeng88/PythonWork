#!/usr/bin/env python
#coding=utf8
from RLHttpAction import RLHttpAction
import thread

actionURL = '/terminal/QueryCustomerInfo.action'
params = {'accesskey':'123ABC','clientid':'1'}
params['onlySearchMyShop']='0'
params['queryItems']='''<queryItems><customerInfo><queryItem><id>customer.identity</id><value>8</value></queryItem></customerInfo></queryItems>'''

ipadNumbers = 100
pressureTest = False

class RLSearchCustomers(RLHttpAction):
	def __init__(self,actionURL=actionURL,params=params):
		RLHttpAction.__init__(self)
		self.actionURL = actionURL
		self.requestData = params


action = RLSearchCustomers()

def pressureTestAction(index,a):
	print '-------------------------------------------------------ipad%d start run aciton ------------------------' %index
	action.run()

if __name__ == '__main__':

	if pressureTest:
		for i in range(0,ipadNumbers):
			thread.start_new_thread(pressureTestAction,(i,None))
		while True:
			pass
	else:
		action.run()
		files = open('SearchCustomers.xml','w')
		files.write(action.responseData)