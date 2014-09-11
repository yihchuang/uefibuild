import os, ConfigParser, shutil, logging, subprocess

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

def uefiBuild(pythonExe, buildScript, BUILDID, BUILDDATE, BUILDVERSION, TOOL_CHAIN_TAG):
    "uefi build"
    print "pythonExe: " + pythonExe
    print "buildScript: " + buildScript
    print "BUILDID: " + BUILDID
    print "BUILDDATE: " + BUILDDATE
    print "BUILDVERSION: " + BUILDVERSION
    print "TOOL_CHAIN_TAG: " + TOOL_CHAIN_TAG

    logging.info("--> enters uefiBuild function")
    runCmd = []
    runCmd.append(pythonExe)
    runCmd.append(buildScript)
    runCmd.append("BUILDID=" + BUILDID)  
    runCmd.append("BUILDDATE=" + BUILDDATE)  
    runCmd.append("BUILDVERSION=" + BUILDVERSION)
    runCmd.append("TOOL_CHAIN_TAG=" + TOOL_CHAIN_TAG)
    logging.debug("runCmd to build:")
    logging.debug(runCmd)
    print runCmd
    logging.debug("start building")
    p = subprocess.Popen(runCmd)
    p.wait() # wait until subprocess to complete  
    logging.info("<-- exits uefiBuild function")
    return

def archiveBuild(targetDir, strBuildIniFile, srcImageFile):
    "Archiving build config file and output image file."
    logging.info("--> enters archiveBuild function")
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    shutil.copy(strBuildIniFile, targetDir)
    shutil.copy(srcImageFile, targetDir)
    logging.info("<-- exits archiveBuild function")
    return

def platformInfoRetrieval(Platform):
    "platform info retrieval"
    logging.info("--> enters platformInfoRetrieval function")
    buildOutputSubDirectoryPrefix = ''
    aslExe = ''
    buildScript = ''
    if Platform == "Grantley": 
        buildOutputSubDirectoryPrefix = "\\Build\\PlatformPkg\\DEBUG_"
        aslExe = "C:\\ASL_Grantley\\iasl.exe"
        buildScript = "PlatformPkg\\PlatformBuild.py"
    elif Platform == "Brickland":
        buildOutputSubDirectoryPrefix = "\\Build\\\BricklandPkg\\DEBUG_"
        aslExe = "C:\\ASL_Brickland\\iasl.exe"	
        buildScript = "BricklandPkg\PlatformBuild.py"
    direcBuild = {'buildOutputSubDirectoryPrefix' : buildOutputSubDirectoryPrefix, 'aslExe' : aslExe, 'buildScript': buildScript}
    logging.info("<-- exits platformInfoRetrieval function")
    return direcBuild

def ensureFileExists(fileName):
    "ensure input file does exist, or raise exception"
    if not os.path.isfile(fileName):
        logging.debug(fileName + " was not found.")
        raise ValueError(fileName + " was not found.")
    return

def packageupBuildInput(buildIniFile):
    config = ConfigParser.SafeConfigParser()  
    config.optionxform = str
    config.read(buildIniFile)
    direcBuild = dict(config.items('build') + config.items('Jazz sm'))
    return direcBuild

def packageupSystemInput(systemIniFile):
    config = ConfigParser.SafeConfigParser()  
    config.optionxform = str
    config.read(systemIniFile)
    direcSystem = dict(config.items('system'))
    return direcSystem