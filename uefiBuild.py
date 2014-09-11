import os, getopt, sys
import datetime, shutil, logging, winsound

from jazz_scm_utils import scmLoad as scmLoad
from jazz_scm_utils import scmUnload as scmUnload
from yihutils import rectifyString as rectifyString
from yihutils import delTree as delTree
from yihutils import uefiBuild as uefiBuild
from yihutils import archiveBuild as archiveBuild
from yihutils import ensureFileExists as ensureFileExists
from yihutils import platformInfoRetrieval as platformInfoRetrieval
from yihutils import packageupBuildInput as packageupBuildInput
from yihutils import packageupSystemInput as packageupSystemInput

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
scmUnloadAtTheEnd=True

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
    direcBuild = {
    'buildIniFile' : buildIniFile,
    'systemIniFile' : systemIniFile
    }
    return direcBuild 

direcIni = {}
if __name__ == "__main__":
    direcIni = main(sys.argv[1:])

logging.debug("direcIni:")
logging.debug(direcIni)

strBuildIniFile = direcIni['buildIniFile']
logging.debug("strBuildIniFile: " + strBuildIniFile)
ensureFileExists(strBuildIniFile)

direcBuild = packageupBuildInput(strBuildIniFile)
logging.debug(direcBuild)
BUILDID = direcBuild['BUILDID']
BUILDDATE = direcBuild['BUILDDATE']
BUILDVERSION = direcBuild['BUILDVERSION']
TOOL_CHAIN_TAG = direcBuild['TOOL_CHAIN_TAG']
Platform = direcBuild['Platform']
SandBox = direcBuild['SandBox']
RepoWS = direcBuild['RepositoyWorkSpaceName']


## configure system settings
strSystemIniFile = direcIni['systemIniFile']
if not strSystemIniFile == "":
    ensureFileExists(strSystemIniFile)
    logging.debug("strSystemIniFile: " + strSystemIniFile)
    direcSystem = packageupSystemInput(strSystemIniFile)
    logging.debug("direcSystem: " + str(direcSystem))
    if not direcSystem['pythonExe'] == '':
        pythonExe = direcSystem['pythonExe']

    if not direcSystem['scmExe'] == '':
        scmExe = direcSystem['scmExe']

    if not direcSystem['aslDir'] == '':
        aslDir = direcSystem['aslDir']

# retrieve platform dependent info:
direcPlatform = platformInfoRetrieval(direcBuild['Platform'], direcBuild['SandBox'], direcBuild['TOOL_CHAIN_TAG'], direcBuild['BUILDID'])
buildOutputSubDirectoryPrefix = direcPlatform['buildOutputSubDirectoryPrefix']
aslExe = direcPlatform['aslExe']    
buildScript = direcPlatform['buildScript']
srcImageFile = direcPlatform['srcImageFile']

## clean up build directory to make sure a clean build
outputDir=SandBox.decode('string_escape') + "\\Build\\"
logging.debug("cleaning up build output directory: " + outputDir)
delTree(outputDir)

## copy iasl.exe per platform 
shutil.copy(aslExe, aslDir)

## scm scmLoad local sandbox
logging.info("-> starts scm scmLoad local sandbox")
scmLoad(scmExe, SandBox, RepoWS)
logging.info("<- ends scm scmLoad local sandbox")

#cache the current working directory before change directory to sandbox
workingDir=os.getcwd()
logging.debug("cache current working directory: " + workingDir)

#change directory to sandbox
logging.debug("before rectification : "  + SandBox)
SandBox = rectifyString(SandBox)
logging.debug("after rectification : "  + SandBox)
os.chdir(SandBox)

logging.debug("-> starts uEFI build")
uefiBuild(pythonExe, buildScript, direcBuild['BUILDID'], direcBuild['BUILDDATE'], direcBuild['BUILDVERSION'], direcBuild['TOOL_CHAIN_TAG'])
logging.debug("<- ends uEFI build")

archiveDir = archiveRootDir + "\\" + BUILDID + "-" + BUILDVERSION + "_" + Platform + "_archivedAt_" + datetime.datetime.now().strftime("%Y-%m-%d-%H%M_%S")
logging.debug("new directory to archive build input and output: " + archiveDir)
print "archiveDir " + archiveDir

logging.debug("-> starts archiving uEFI build")
archiveBuild(archiveDir, strBuildIniFile, srcImageFile)
logging.debug("<- ends archiving uEFI build")

logging.debug("-> scmUnloadAtTheEnd:" + str(scmUnloadAtTheEnd))
if scmUnloadAtTheEnd == True:
    logging.debug("-> starts scm unload")
    scmUnload(scmExe, SandBox, RepoWS)
    logging.debug("<- ends scm unload")
#beep to notify    
winsound.Beep(440, 250)