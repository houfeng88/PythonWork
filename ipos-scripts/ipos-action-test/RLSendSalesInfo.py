#!/usr/bin/env python
#coding=utf8
from RLHttpAction import RLHttpAction
import thread

actionURL = '/terminal/GetTerminalInfo.action'
params = {'accesskey':'123ABC','clientid':'1'}
params['customerid']= '8605000301079919'
params['rvCustomerID']= '4625'
params['giftCard']= '''<giftCard><DVPoint><money>0</money><num>0</num></DVPoint><Other><money>0</money><num>0</num></Other></giftCard>'''
params['incentive']= '''<incentive><pointUsed><point>0</point><pointUsedForDiscount>1</pointUsedForDiscount><flag>0</flag></pointUsed><chargeUsed>0</chargeUsed></incentive>'''
params['newCustomerFlag']= '''0'''
params['salesinfo']= '''<salesinfo><refound>0</refound><type>sale</type><totalMoney>1944</totalMoney><tax>144</tax><items><item><product>0010010003</product><num>1</num><money>1944</money><discount>0</discount><tax>144</tax><salestaffid>999999</salestaffid><salestaff><type>2</type><staffs><staff><staffid>999999</staffid><staffname>RL\U30b9\U30bf\U30c3\U30d5</staffname><appointstaff>false</appointstaff><undertake>30</undertake></staff></staffs></salestaff></item></items></salesinfo>'''
params['serialno']= '''1'''
params['staffid']= '''999999'''
params['regDate']= '''015-11-05'''
params['timeStamp']= '''2015-11-06 18:18:00'''

ipadNumbers = 100
pressureTest = False

class RLSendSalesInfo(RLHttpAction):
	def __init__(self,actionURL=actionURL,params=params):
		RLHttpAction.__init__(self)
		self.actionURL = actionURL
		self.requestData = params


action = RLSendSalesInfo()

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
		files = open('SendSalesInfo.xml','w')
		files.write(action.responseData)