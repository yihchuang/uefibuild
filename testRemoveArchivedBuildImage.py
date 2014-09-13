import sys, getopt
from pymongo import MongoClient
from yihutils import getMongoDbCollectionClone as getMongoDbCollectionClone
from yihutils import removeFromMongoDbClone as removeFromMongoDbClone

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

from yihutils import printMongoDbCollection as printMongoDbCollection

def main(argv):
    archiveDir = ''
    try:
        opts, args = getopt.getopt(argv,"hi:i:",["adir="])
    except getopt.GetoptError:
        print sys.argv[0] + ' -i <archiveDir>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print sys.argv[0] + ' -i <archiveDir>'
            sys.exit()
        elif opt in ("-i", "--adir"):
            archiveDir = arg
    print 'archiveDir is "', archiveDir
    direc = {
        'archiveDir' : archiveDir,
    }
    print direc
    return direc

if __name__ == "__main__":
    returnDirec = main(sys.argv[1:])

print returnDirec

client = MongoClient()
#db = client.mydb #uefibuild
#yihtest = db.testData

#db = client.dbName #uefibuild
#buildCollection = db.dbCollectionName
buildCollection = getMongoDbCollectionClone()
##
printMongoDbCollection(buildCollection)
##
archiveDir = "C:\\myArchive\\1"
#buildCollection = getMongoDbCollectionClone()
removeFromMongoDbClone(archiveDir)

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