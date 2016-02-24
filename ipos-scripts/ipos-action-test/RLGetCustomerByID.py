#!/usr/bin/env python
#coding=utf8
from RLHttpAction import RLHttpAction
import thread

actionURL = '/terminal/GetTerminalInfo.action'
params = {'accesskey':'123ABC','clientid':'1'}
params['customerid']= '8605000301079919'
params['rvCustomerID']= '4625'
ipadNumbers = 100
pressureTest = False

class RLGetCustomerByID(RLHttpAction):
	def __init__(self,actionURL=actionURL,params=params):
		RLHttpAction.__init__(self)
		self.actionURL = actionURL
		self.requestData = params


action = RLGetCustomerByID()

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
		files = open('CustomerByID.xml','w')
		files.write(action.responseData)