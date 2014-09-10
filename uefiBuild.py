import os, getopt, ConfigParser, sys
import datetime, shutil, logging, winsound
from jazz_scm_utils import load as load
##from jazz_scm_utils import unload as unload

from yihutils import rectifyString as rectifyString
from yihutils import delTree as delTree
from yihutils import uefiBuild as uefiBuild
from yihutils import archiveBuild as archiveBuild
from yihutils import ensureFileExists as ensureFileExists

logging.basicConfig(filename='yih.log',level=logging.DEBUG)
logging.info("\n---------------------------------------------")
logging.info(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

# pre-set but can be overridden if system.ini is input.
pythonExe="C:\\Python27\\python.exe"
scmExe="C:\\RTC-Client-Win-4.0.5\\jazz\\scmtools\\eclipse\\scm.exe"
aslGrantleyExe ="C:\\ASL_Grantley\\iasl.exe"
aslBricklandExe = "C:\\ASL_Brickland\\iasl.exe"
aslDir = "C:\\ASL\\"
archiveRootDir="C:\\uEFI_build\\archive\\"

#get input parameters: build ini file (required) and system ini file (optional)
def main(argv):
    buildIniFile = ''
    systemIniFile = ''
    try:
        opts, args = getopt.getopt(argv,"hb:s:",["buildIniFile=","systemIniFile="])
    except getopt.GetoptError:
        print sys.argv[0] + ' -b <buildConfig.ini> -s <systemConfig.ini>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print sys.argv[0] + ' -b <buildConfig.ini> -s <systemConfig.ini>'
            sys.exit()
        elif opt in ("-b", "--buildIniFile"):
            buildIniFile = arg
        elif opt in ("-s", "--systemIniFile"):
            systemIniFile = arg
    print 'Build ini file is: ', buildIniFile
    print 'System ini file is: ', systemIniFile
    direc = {
    'buildIniFile' : buildIniFile,
    'systemIniFile' : systemIniFile
    }
    return direc 

direcIni = {}
if __name__ == "__main__":
    direcIni = main(sys.argv[1:])

logging.debug("direcIni:")
logging.debug(direcIni)

strBuildIniFile = direcIni['buildIniFile']
logging.debug("strBuildIniFile: " + strBuildIniFile)
ensureFileExists(strBuildIniFile)
config = ConfigParser.ConfigParser()
config.sections()
config.read(strBuildIniFile)
strBUILDID = config.get("build", "BUILDID")
strBUILDDATE = config.get("build", "BUILDDATE")
strBUILDVERSION = config.get("build", "BUILDVERSION")
strTOOL_CHAIN_TAG = config.get("build", "TOOL_CHAIN_TAG")
strPlatform = config.get("build", "Platform")
strSandBox = config.get("Jazz sm", "SandBox")

strRepoWS = config.get("Jazz sm", "RepositoyWorkSpaceName")
## compose a python directory to contain parameters
direc = { 
'strBuildIniFile' : strBuildIniFile,
'strBUILDID' : strBUILDID,
'strBUILDDATE' : strBUILDDATE,
'strBUILDVERSION' : strBUILDVERSION,
'strTOOL_CHAIN_TAG' : strTOOL_CHAIN_TAG,
'strPlatform' : strPlatform,
'strSandBox' : strSandBox,
'strRepoWS' : strRepoWS
}

logging.debug(direc)

## configure system settings
strSystemIniFile = direcIni['systemIniFile']
if not strSystemIniFile == "":
    ensureFileExists(strSystemIniFile)
    logging.debug("strSystemIniFile: " + strSystemIniFile)
    config = ConfigParser.ConfigParser()
    config.sections()
    config.read(strSystemIniFile)
    pythonExe = config.get("system", "pythonExe")
    scmExe = config.get("system", "scmExe")
## compose a python directory to contain parameters
direcSys = { 
'pythonExe' : pythonExe,
'scmExe' : scmExe
}

logging.debug("direcSys")
logging.debug(direcSys)

## clean up build directory to make sure a clean build
outputDir=strSandBox.decode('string_escape') + "\\Build\\"
logging.debug("cleaning up build output directory: " + outputDir)
delTree(outputDir)

## copy iasl.exe per platform 
if strPlatform == "Grantley": 
    logging.debug("copy iasl.exe to C:\ASL for Grantley build")
    shutil.copy("C:\\ASL_Grantley\\iasl.exe", "C:\\ASL\\")
elif strPlatform == "Brickland":
    logging.debug("copy iasl.exe to C:\ASL for Brickland build")
    shutil.copy("C:\\ASL_Brickland\\iasl.exe", "C:\\ASL\\")
else: 
    logging.critical("unknown platform was found!")
    print "error!"

## scm load local sandbox
logging.info("->start scm load local sandbox")
load(scmExe, direc['strSandBox'], direc['strRepoWS'])
logging.info("<- end scm load local sandbox")
#TODO: need to check error to make sure enlist completes successfully
## end of scm load

#cache the current working directory before change directory to sandbox
workingDir=os.getcwd()
logging.debug("cache current working directory: ", workingDir)

#change directory to sandbox
logging.debug("before rectification : "  + strSandBox)
strSandBox = rectifyString(strSandBox)
logging.debug("after rectification : "  + strSandBox)
os.chdir(strSandBox)

logging.debug("->start uefi build")
uefiBuild(pythonExe, "PlatformPkg\\PlatformBuild.py", direc['strBUILDID'], direc['strBUILDDATE'], direc['strBUILDVERSION'], direc['strTOOL_CHAIN_TAG'])
logging.debug("<- end uefi build")

#archiveDir = workingDir + "\\" + strBUILDID + "-" + strBUILDVERSION + "_" + strPlatform + "_archivedAt_" + datetime.datetime.now().strftime("%Y-%m-%d-%H%M_%S")
archiveDir = archiveRootDir + "\\" + strBUILDID + "-" + strBUILDVERSION + "_" + strPlatform + "_archivedAt_" + datetime.datetime.now().strftime("%Y-%m-%d-%H%M_%S")
logging.debug("new directory to archive build input and output: " + archiveDir)
print "archiveDir " + archiveDir
if strPlatform == "Grantley": 
    print "archiveGrantley"
    srcImageFile=strSandBox.decode('string_escape') + "\\Build\\PlatformPkg\\DEBUG_" + strTOOL_CHAIN_TAG + "\\FV\\" + strBUILDID + ".upd"
    logging.debug("save build output file: " + srcImageFile)
    print "srcImageFile: " + srcImageFile
    archiveBuild(archiveDir, strBuildIniFile, srcImageFile)
elif strPlatform == "Brickland":
        print "archiveBrickland"
        srcImageFile=strSandBox.decode('string_escape') + "\\Build\\\BricklandPkg\\DEBUG_" + strTOOL_CHAIN_TAG + "\\FV\\" + strBUILDID + ".upd"
        logging.debug("save build output file: " + srcImageFile)
        print "srcImageFile: " + srcImageFile
        archiveBuild(archiveDir, strBuildIniFile, srcImageFile)
else: 
    logging.critical("unknown platform was found!")
    print "error!"
    
#beep to notify    
winsound.Beep(440, 250)