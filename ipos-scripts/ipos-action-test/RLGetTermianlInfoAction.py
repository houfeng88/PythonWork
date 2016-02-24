from RLHttpAction import RLHttpAction
import thread

actionURL = '/terminal/GetTerminalInfo.action'
params = {'accesskey':'123ABC','clientid':'1','firmverion':'0x0118','serialno':'1','terminalType':'1','clienttime':'2015-11-06 16:43:52'}

ipadNumbers = 100
pressureTest = False

class RLGetTerminalInfoAction(RLHttpAction):
	def __init__(self,actionURL=actionURL,params=params):
		RLHttpAction.__init__(self)
		self.actionURL = actionURL
		self.requestData = params


action = RLGetTerminalInfoAction()

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
		files = open('TerminalInfo.xml','w')
		files.write(action.responseData)