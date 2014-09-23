import sys, getopt, Tkinter
from pymongo import MongoClient
from yihutils import getMongoDbCollectionClone as getMongoDbCollectionClone
from yihutils import removeFromMongoDbClone as removeFromMongoDbClone
from yihutils import ensureDirExists as ensureDirExists
from yihutils import delTree as delTree
from yihutils import getDictFromMongoDbCollection as getDictFromMongoDbCollection
from yihutils import iternateThroughDictionay as iternateThroughDictionay
from yihutils import getListFromMongoDbCollection as getListFromMongoDbCollection

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
printMongoDbCollection(buildCollection)
dictForGUI = getDictFromMongoDbCollection(buildCollection)
iternateThroughDictionay(dictForGUI)

listForGUI = getListFromMongoDbCollection(buildCollection, 'archiveDir')
##

## if found existing record and successfully remove it, print: {u'ok': 1, u'n': 1}
## if not found existing record, print: {u'ok': 1, u'n': 0}
####

def purgeArchive():
    #append '\\' to archiveDir to prevent shutil.rmtree() wipes out the entire parent directory!
    archiveDir = radioButtonDict[var.get()]
    buildCollection = getMongoDbCollectionClone()
    removeFromMongoDbClone(archiveDir)
    if archiveDir.endswith("\\") == False:
        archiveDir = "".join((archiveDir, '\\'))
    ensureDirExists(archiveDir)
    delTree(archiveDir)
    return

# prepare for GUI display
def sel():
    print var.get()
    _text =  radioButtonDict[var.get()]
    print _text
    label.config(text = _text)
    buttonText = "Is it OK to purge :  " + _text + "  ?"
    buttonPurge.config(text = buttonText, state=Tkinter.NORMAL)

root = Tkinter.Tk()
var = Tkinter.IntVar()

radioButtonDict = {}

for index, value in enumerate(listForGUI):
    radioButton = Tkinter.Radiobutton(root, text=value, value=index, variable=var, command=sel, state=Tkinter.NORMAL)
    radioButton.grid(row=index, column=0)
    radioButton.pack( anchor = Tkinter.W )
    radioButtonDict.update({index: value})

buttonPurge = Tkinter.Button(root, text="Purge", relief='raised', command=purgeArchive, state=Tkinter.DISABLED)
buttonPurge.pack()
buttonRefresh = Tkinter.Button(root, text="Refresh", relief='raised')
buttonRefresh.pack()
label = Tkinter.Label(root)
label.pack()
root.mainloop()

client.close()
