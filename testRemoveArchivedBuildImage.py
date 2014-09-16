import sys, getopt
from pymongo import MongoClient
from yihutils import getMongoDbCollectionClone as getMongoDbCollectionClone
from yihutils import removeFromMongoDbClone as removeFromMongoDbClone
from yihutils import ensureDirExists as ensureDirExists
from yihutils import delTree as delTree

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

from yihutils import printMongoDbCollection as printMongoDbCollection

def main(argv):
    archiveDir = ''
    try:
        opts, args = getopt.getopt(argv,"hi:a:",["adir="])
    except getopt.GetoptError:
        print sys.argv[0] + ' -a <archiveDir>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print sys.argv[0] + ' -a <archiveDir>'
            sys.exit()
        elif opt in ("-a", "--adir"):
            archiveDir = arg
    print 'archiveDir is "', archiveDir
    direc = {
        'archiveDir' : archiveDir,
    }
    print direc
    return direc

if __name__ == "__main__":
    inputDict = main(sys.argv[1:])

print inputDict

client = MongoClient()
#db = client.mydb #uefibuild
#yihtest = db.testData

#db = client.dbName #uefibuild
#buildCollection = db.dbCollectionName
buildCollection = getMongoDbCollectionClone()
##
printMongoDbCollection(buildCollection)
##
archiveDir = inputDict['archiveDir'] #"C:\\uEFI_build\\archive\\\\TCE101YUS-1.YC_Brickland_archivedAt_2014-09-12-1127_113"
#append '\\' to archiveDir to prevent shutil.rmtree() wipes out the entire parent directory!
if archiveDir.endswith("\\") == False:
    archiveDir = "".join((archiveDir, '\\'))
ensureDirExists(archiveDir)
#buildCollection = getMongoDbCollectionClone()
removeFromMongoDbClone(archiveDir)
delTree(archiveDir)
#recordToremoveFromDB = { "archiveDir" : archiveDir }
#print "recordToremoveFromDB:" + str(recordToremoveFromDB)
#print buildCollection.find(recordToremoveFromDB).count()
#print buildCollection.remove(recordToremoveFromDB)


##
printMongoDbCollection(buildCollection)
##
client.close()
## if found existing record and successfully remove it, print: {u'ok': 1, u'n': 1}
## if not found existing record, print: {u'ok': 1, u'n': 0}