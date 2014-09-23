import yihutils, pymongo, sys, getopt
import unittest
from pymongo import MongoClient

from yihutils import getListOfDictFromMongoDbCollection as getListOfDictFromMongoDbCollection
from yihutils import getMongoDbCollectionClone as getMongoDbCollectionClone
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

listOfDictDbCollection = getListOfDictFromMongoDbCollection(buildCollection)
print "listOfDictDbCollection: " 
print listOfDictDbCollection
for dictRecord in listOfDictDbCollection:
    print dictRecord['archiveDir'] 