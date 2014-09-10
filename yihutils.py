import os
import winsound
import shutil
import logging
import subprocess

#class BraceMessage(object):
#    def __init__(self, fmt, *args, **kwargs):
#        self.fmt = fmt
#        self.args = args
#        self.kwargs = kwargs
#
#    def __str__(self):
#        return self.fmt.format(*self.args, **self.kwargs)

def delTree(f):
    d = os.path.dirname(f)
    if os.path.exists(d):
        shutil.rmtree(d)
	return
	
def winBeep():
	Freq = 2500 # Set Frequency To 2500 Hertz
	Dur = 1000 # Set Duration To 1000 ms == 1 second
	winsound.Beep(Freq,Dur)
	return
	
def rectifyList(list):
	"rectify input list to decode (remove) escape character"
	print "entering rectify function"
	for i in range(len(list)):
		list[i] = list[i].decode('string_escape')
	return list
	
def rectifyString(str):
	"rectify input string to decode (remove) escape character"
	print "entering rectify function"
	str = str.decode('string_escape')
	return str
	
def uefiBuild(pythonExe, buildScript, strBUILDID, strBUILDDATE, strBUILDVERSION, strTOOL_CHAIN_TAG):
	"uefi build"
	print "pythonExe: " + pythonExe
	print "buildScript: " + buildScript
	print "strBUILDID: " + strBUILDID
	print "strBUILDDATE: " + strBUILDDATE
	print "strBUILDVERSION: " + strBUILDVERSION
	print "strTOOL_CHAIN_TAG: " + strTOOL_CHAIN_TAG

	runCmd = []
	runCmd.append(pythonExe)
	runCmd.append(buildScript)
	runCmd.append("BUILDID=" + strBUILDID)  
	runCmd.append("BUILDDATE=" + strBUILDDATE)  
	runCmd.append("BUILDVERSION=" + strBUILDVERSION)
	runCmd.append("TOOL_CHAIN_TAG=" + strTOOL_CHAIN_TAG)
	logging.debug("runCmd to build:")
	logging.debug(runCmd)
	print runCmd
	logging.debug("start building")
	p = subprocess.Popen(runCmd)
	p.wait() # wait until subprocess to complete  
	return
	
def archiveBuild(targetDir, strConfigfile, srcImageFile):
	"Archiving build config file and output image file."
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)
	shutil.copy(strConfigfile, targetDir)
	shutil.copy(srcImageFile, targetDir)
	return
	
def platformInfo(strPlatform):
	buildOutputSubDirectoryPrefix = ''
	aslExe = ''
	if strPlatform == "Grantley": 
		buildOutputSubDirectoryPrefix = "\\Build\\PlatformPkg\\DEBUG_"
		aslExe = "C:\\ASL_Grantley\\iasl.exe"
	elif strPlatform == "Brickland":
		buildOutputSubDirectoryPrefix = "\\Build\\\BricklandPkg\\DEBUG_"
		aslExe = "C:\\ASL_Brickland\\iasl.exe"	
	direc = {'buildOutputSubDirectoryPrefix' : buildOutputSubDirectoryPrefix, 'aslExe' : aslExe}
	return direc