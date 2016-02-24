#!/usr/bin/python
#coding=utf-8

import os
import sys 
from datetime import datetime

CONFIG_DIR = "./Config/"
CLIENT_LIST = "%s/client.list" % CONFIG_DIR
PLIST_FNAME = "%s/buildinfo.plist" % CONFIG_DIR
IPOS_CONFIG_DIR = "../pos/Config/"
TARGET_DIR = "./build/ipa-build/"
RELEASE_SERVER = "192.168.1.187"
RELEASE_USER = "repeatlink"
RELEASE_PASSWD = "repeatlink"
RELEASE_DIR = "/var/www/html/ipos/"
SVN_NUMBER = ""
def write_plist(rev, timestamp, appName):
	wf = open(PLIST_FNAME, "w")	
	content = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>build_timestamp</key>
	<string>%s</string>
	<key>svn_revision</key>
	<string>%d</string>
	<key>client</key>
	<string>%s</string>
</dict>
</plist>
	""" % (timestamp, rev, appName)

	print content
	wf.write(content)
	wf.close()

def printUsage():
	print "Usage: buildipa.py <app name>  <svn number>"
	print "app name can be set like the following values."
	print g_Clients.getAllUsage()

class Client:
	def __init__(self, row):	
		self.Name = row[0]
		self.FullName = row[1]

	def getUsage(self):
		return "  %8s : for %s use.\n" % (self.Name, self.FullName)
	
class Clients:
	def __init__(self):
		self.clist = set()
		self.readClientList(CLIENT_LIST)

	def readClientList(self, fileName):
		f = open(fileName, "r")
		lines = f.readlines()
		for line in lines:
			line = line.replace("\n", "")
			tokens = line.split(",")
			if len(tokens) > 1:
				client = Client(tokens)
				self.clist.add(client)
		f.close()

	def getValidName(self):
		ret = set()
		for c in self.clist:
			ret.add(c.Name)
		return ret

	def getAllUsage(self):
		usage = ""
		for c in self.clist:
			usage += c.getUsage()
		return usage

def writeInfoList(appName):
	#os_stream = os.popen("svn info buildipa.py | grep Revision")
	os_stream = os.popen("svn info . | grep \"Last Changed Rev\"")
	rev_str = os_stream.read()
	rev = 0
	if len(rev_str) > 1 and rev_str.find(":") != -1:
		tokens = rev_str.split(":")
		print "rev = %d" % int(tokens[1]) 
		rev = int(tokens[1])

	timeStamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	write_plist(rev, timeStamp, appName)

SERVER = "192.168.1.187"
PRINTER = "192.168.1.199"
APPNAME = {
"UNN":"RLASP3_UNNEAU",
"KF":"RLASP3_KF",
"CJ":"RLASP2_CJ",
"KKB":"RLASP3_KKB",
"MH":"RLASP3_MH",
"MNI":"RLASP3_MNI",
"MHBS":"RLASP3_MHBS",
"HGM":"RLASP3_HGM",
"MS":"RLASP4_MS",
"CD":"RLASP3_MH",
"JPDell":"RLASP3_MH",
"JPHP":"RLASP3_MH",
"YC":"RLASP4_YSCARE",
"MUSE":"RLASP4_MUSE",
"TR":"RLASP4_TRICIA",
"BLX":"RLASP4_BELLEX",
"RF":"RLASP4_RAYFIELD"
}
def modifyForTest(configFile, client):
	f = open(configFile, "r")
	lines = f.readlines()
	contents = ""
	for line in lines:
		if line.find("<server>") > 0:
			mline = "\t\t<server>%s</server>\n" % SERVER
			contents += mline
			print mline
		elif line.find("<domain>") > 0:
			mline = "\t\t<domain>https://%s</domain>\n" % SERVER
			contents += mline
			print mline
		elif line.find("<app_name>") > 0:
			appName = APPNAME[client]
			mline = "\t\t<app_name>%s</app_name>\n" % appName
			contents += mline
			print mline
		elif line.find("<ipaddress>") > 0:
			mline = "\t\t<ipaddress>%s</ipaddress>\n" % PRINTER
			contents += mline
			print mline
		else:
			contents += line
		#print line
	f.close()

	wf = open(configFile, "w")
	wf.write(contents)
	wf.close()


#
# Main
#
g_Clients = Clients()
if len(sys.argv) <= 1:
	printUsage()
	exit()

ValidAppName = g_Clients.getValidName()
if sys.argv[1] != "ALL" and sys.argv[1] not in ValidAppName:
	printUsage()
	exit()

appName = sys.argv[1]
if(len(sys.argv) >= 3):
	SVN_NUMBER = sys.argv[2]


#
# Step1. Update the source code to lastest version
#
print "########################################################"
print "Step1. 更新代码到最新版本."
print "########################################################"

if SVN_NUMBER != "":
	command = "svn up -r %s" % (SVN_NUMBER)
else:
	command = "svn up"
print command
os.system(command)
print "\n\n"

#
# Step2. Update the SVN revesion and timestamp.
#
print "########################################################"
print "Step2. 更新SVN版本号和编译时间"
print "########################################################"
writeInfoList(appName)
command = "cd %s;cp -f config_%s.xml config.xml" % (CONFIG_DIR, appName)
print command
os.system(command)
modifyForTest("%s/config.xml" % CONFIG_DIR, appName)
command = "cd %s;./RLAES2;cp -f pconfig.xml %s/pconfig.xml;cp -f buildinfo.plist %s/buildinfo.plist" % (CONFIG_DIR, IPOS_CONFIG_DIR, IPOS_CONFIG_DIR)
print command
os.system(command)
print "\n\n"

#
# Step3. Build rlterm3 project.
#
print "########################################################"
print "Step3. 编译项目"
print "########################################################"
command = "./ipa-build . -n"
print command
os.system(command)
print "\n\n"

#
# Step4. Upload the targe file to publish site
#
print "########################################################"
print "Step4. 上传编译成功的文件到发布目录"
print "########################################################"
#command = "./sftpUploadFile %s/rlterm3_*.ipa %s %s %s %s rlterm3.ipa" % (TARGET_DIR, RELEASE_SERVER, RELEASE_USER, RELEASE_PASSWD, RELEASE_DIR)
command = "scp %s/rlterm3_*.ipa %s@%s:%s/rlterm3.ipa" % (TARGET_DIR, RELEASE_USER, RELEASE_SERVER, RELEASE_DIR)
print command
os.system(command)
print "\n\n"


