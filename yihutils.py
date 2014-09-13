import os, ConfigParser, shutil, logging, subprocess
from pymongo import MongoClient

dbName = "uefi"
dbCollectionName = "build"

def delTree(f):
    d = os.path.dirname(f)
    if os.path.exists(d):
        shutil.rmtree(d)
    return

def rectifyList(_list):
    "rectify input _list to decode (remove) escape character"
    #logging.info("--> enters rectifyList function")
    for i in range(len(_list)):
        _list[i] = _list[i].decode('string_escape')        
    #logging.info("<-- exits rectifyList function")
    return _list

def rectifyString(_str):
    "rectify input string to decode (remove) escape character"
    #logging.info("--> enters rectify function")
    _str = _str.decode('string_escape')
    #logging.info("<-- exits rectifyString function")
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

def platformInfoRetrieval(Platform, SandBox, TOOL_CHAIN_TAG, BUILDID):
    "platform info retrieval"
    logging.info("--> enters platformInfoRetrieval function")
    buildOutputSubDirectoryPrefix = ''
    aslExe = ''
    buildScript = ''
    srcImageFile = ''
    if Platform == "Grantley": 
        buildOutputSubDirectoryPrefix = "\\Build\\PlatformPkg\\DEBUG_"
        aslExe = "C:\\ASL_Grantley\\iasl.exe"
        buildScript = "PlatformPkg\\PlatformBuild.py"
        srcImageFile=SandBox.decode('string_escape') + "\\Build\\PlatformPkg\\DEBUG_" + TOOL_CHAIN_TAG + "\\FV\\" + BUILDID + ".upd"
    elif Platform == "Brickland":
        buildOutputSubDirectoryPrefix = "\\Build\\\BricklandPkg\\DEBUG_"
        aslExe = "C:\\ASL_Brickland\\iasl.exe"	
        buildScript = "BricklandPkg\PlatformBuild.py"
        srcImageFile=SandBox.decode('string_escape') + "\\Build\\\BricklandPkg\\DEBUG_" + TOOL_CHAIN_TAG + "\\FV\\" + BUILDID + ".upd"
    dictPlatform = {'buildOutputSubDirectoryPrefix' : buildOutputSubDirectoryPrefix, 'aslExe' : aslExe, 
                     'srcImageFile' : srcImageFile, 'buildScript': buildScript}
    logging.info("<-- exits platformInfoRetrieval function")
    return dictPlatform

def ensureFileExists(fileName):
    "ensure input file does exist, or raise exception"
    if not os.path.isfile(fileName):
        logging.debug(fileName + " was not found.")
        raise ValueError(fileName + " was not found.")
    return

def packageupBuildInput(buildIniFile):
    logging.info("--> enters packageupBuildInput function")
    config = ConfigParser.SafeConfigParser()  
    config.optionxform = str
    config.read(buildIniFile)
    dictBuild = dict(config.items('build') + config.items('Jazz sm') + config.items('meta'))
    logging.info("<-- exits packageupBuildInput function")
    return dictBuild

def packageupSystemInput(systemIniFile):
    logging.info("--> enters packageupSystemInput function")
    config = ConfigParser.SafeConfigParser()  
    config.optionxform = str
    config.read(systemIniFile)
    dictSystem = dict(config.items('system'))
    logging.info("<-- exits packageupSystemInput function")
    return dictSystem

def printMongoDbCollection(dbCollection):
    results = dbCollection.find()
    print()
    print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-')

    # display documents from collection
    for record in results:
        # print out the document
        print(record)

    print()
    return


def addToMongoDb(dictBuild, archiveDir):
    logging.info("--> enters addToMongoDb function")
    client = MongoClient()
    db = client.uefi
    buildCollection = db.build
    newRecordToAddToDB = dictBuild
    del newRecordToAddToDB['TOOL_CHAIN_TAG']
    del newRecordToAddToDB['SandBox']
    del newRecordToAddToDB['RepositoyWorkSpaceName']
    newRecordToAddToDB['archiveDir'] = archiveDir
    logging.debug("newRecord to add to mongoDB: " + str(newRecordToAddToDB))
    post_id = buildCollection.insert(newRecordToAddToDB)
    logging.debug("post_id: " + str(post_id))
    client.close()
    logging.info("<-- exits addToMongoDb function")
    return

def getMongoDbCollectionClone():
    client = MongoClient()
    db = client.dbName
    buildCollection = db.dbCollectionName
    return buildCollection

def removeFromMongoDbClone(archiveDir):
    buildCollection = getMongoDbCollectionClone()
    print buildCollection
    recordToremoveFromDB = { "archiveDir" : archiveDir }
    print "recordToremoveFromDB:" + str(recordToremoveFromDB)
    print buildCollection.find(recordToremoveFromDB).count()
    print buildCollection.remove(recordToremoveFromDB)
    return
    
    return
def addToMongoDbClone(dictBuild, archiveDir):
    logging.info("--> enters addToMongoDb function")
    buildCollection = getMongoDbCollectionClone()
    print buildCollection
    newRecordToAddToDB = dictBuild
    if 'TOOL_CHAIN_TAG' in newRecordToAddToDB.keys():
        del newRecordToAddToDB['TOOL_CHAIN_TAG']
    if 'SandBox' in newRecordToAddToDB.keys():
        del newRecordToAddToDB['SandBox']
    if 'RepositoyWorkSpaceName' in newRecordToAddToDB.keys():
            del newRecordToAddToDB['RepositoyWorkSpaceName']
    newRecordToAddToDB['archiveDir'] = archiveDir
    logging.debug("newRecord to add to mongoDB: " + str(newRecordToAddToDB))
    #post_id = buildCollection.insert(newRecordToAddToDB)
    post_id = buildCollection.save(newRecordToAddToDB)
    logging.debug("post_id: " + str(post_id))
    ##
    printMongoDbCollection(buildCollection)
    ##
    
#TODO:    client.close()
    logging.info("<-- exits addToMongoDb function")
    return