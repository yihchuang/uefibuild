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
##YIH##archiveDir = inputDict['archiveDir'] #"C:\\uEFI_build\\archive\\\\TCE101YUS-1.YC_Brickland_archivedAt_2014-09-12-1127_113"
#append '\\' to archiveDir to prevent shutil.rmtree() wipes out the entire parent directory!
##YIH##if archiveDir.endswith("\\") == False:
##YIH##    archiveDir = "".join((archiveDir, '\\'))
##YIH##ensureDirExists(archiveDir)
#buildCollection = getMongoDbCollectionClone()
##YIH##removeFromMongoDbClone(archiveDir)
##YIH##delTree(archiveDir)

##
printMongoDbCollection(buildCollection)
dictForGUI = getDictFromMongoDbCollection(buildCollection)
iternateThroughDictionay(dictForGUI)

listForGUI = getListFromMongoDbCollection(buildCollection, 'archiveDir')
##
client.close()
## if found existing record and successfully remove it, print: {u'ok': 1, u'n': 1}
## if not found existing record, print: {u'ok': 1, u'n': 0}
####
def sel():
    print var.get()
    _text =  radioButtonDict[var.get()]
    print _text
    selection = "You selected the option " + str(var.get())
    #label.config(text = selection)
    label.config(text = _text)

root = Tkinter.Tk()
var = Tkinter.IntVar()
##var = Tkinter.StringVar()

radioButtonDict = {}

for index, value in enumerate(listForGUI):
#    button = Tkinter.Button(root, text=value + dictForGUI.get(value), relief='raised', command = sel)
    #button = Tkinter.Radiobutton(root, text=value, relief='raised', command = sel)
    ##button = Tkinter.Radiobutton(root, text=value, value=index, variable=var, command=sel)
    button = Tkinter.Radiobutton(root, text=value, value=index, variable=var, command=sel)
    button.grid(row=index, column=0)
    button.pack( anchor = Tkinter.W )
    radioButtonDict.update({index: value})

label = Tkinter.Label(root)
label.pack()
root.mainloop()



###frame1 = Tkinter.Frame()
###s = Tkinter.Scrollbar(frame1)
###listBox = Tkinter.Listbox(frame1)

###s.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
###listBox.pack(side=Tkinter.LEFT, fill=Tkinter.Y)

###s['command'] = listBox.yview
###listBox['yscrollcommand'] = s.set

##for index in range(30): 
##   listBox.insert(Tkinter.END, str(index))
###for record in dictForGUI:
###        # print out the document
###        listBox.insert(Tkinter.END, record)
###frame1.pack(side=Tkinter.TOP)
###
###frame2 = Tkinter.Frame()
###lab = Tkinter.Label(frame2)
###
###def poll():
###    lab.after(200, poll)
###    sel = listBox.curselection()
###    value = ""
###    if not sel == ():
###        value = listBox.get(sel)
###    lab.config(text=value)
###
###lab.pack()
###frame2.pack(side=Tkinter.TOP)
###
###poll()
###Tkinter.mainloop()
