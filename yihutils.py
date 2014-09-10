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

def rectifyList(_list):
    "rectify input _list to decode (remove) escape character"
    logging.info("--> enters rectifyList function")
    for i in range(len(_list)):
        _list[i] = _list[i].decode('string_escape')        
    logging.info("<-- exits rectifyList function")
    return _list

def rectifyString(_str):
    "rectify input string to decode (remove) escape character"
    logging.info("--> enters rectify function")
    _str = _str.decode('string_escape')
    logging.info("<-- exits rectifyString function")
    return _str

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

def archiveBuild(targetDir, strBuildIniFile, srcImageFile):
    "Archiving build config file and output image file."
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    shutil.copy(strBuildIniFile, targetDir)
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

def ensureFileExists(fileName):
    "ensure input file does exist, or raise exception"
    if not os.path.isfile(fileName):
        logging.debug(fileName + " was not found.")
        raise ValueError(fileName + " was not found.")
    return
