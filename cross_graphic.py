from random import random , sample
from tkinter import *


descr = []
coord = []
coordText = []
directions = []
vocabulary = []
vocabularyRev = []
descriptions = []
wordLength = []
wordLengthRev =[]
row = []
array = []
words = []
wordsRev = []
abcNum100 = []
usedWords = []
dString= []
hL = []
descrH = []
descrV = []

fullLettSet = "-АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
goodLettSet = "АБВГДЕИКЛМНОПРСТ"
#vocPath = input("Path to vocabulary file")
vocPath = "_vocabulary1.txt"


#root = Tk()
#root.title("Crossword")
#root.geometry("1500x1000")
#root.resizable(width=True, height=True)
#nrEntry = Entry(width="5")
#nrEntry.grid(row=37,column=35, columnspan=2) #, rowspan=3)

# creates array of "." 80x80 with numbers of rows and columns
for i in range(1,80):
    row.append(i)
array.append(row)
for j in range(2,80):
    row=[j]
    for i in range(1,80):
        row.append(".")
    array.append(row)

# read vocabulary file
with open(vocPath) as file:
   voc = [row.strip() for row in file]

# wordLength - create empty array
for i in range(30):
    a=[]
    wordLength.append(a)
for i in range(30):
    a=[]
    wordLengthRev.append(a)
	
for item in voc: # fill wordLength: wordLength[i] is list of words with length == i or longer
    tabPos = item.find("\t")
    word = item[0:tabPos-1]
    description = item[tabPos:len(item)]
    vocabulary.append(word)
    vocabularyRev.append(word[::-1])
    descriptions.append(description)
    for i in range(1, len(word)+1):
        wordLength[i].append(word)
        wordLengthRev[i].append(word[::-1])

# words - create empty array
for i in range(30):
    a=[]
    for j in range(len(fullLettSet)):
        a.append([])
    words.append(a)
for i in range(14400): # fill words: words[a][b] is list of words with letter on "a"-position equal fullLettSet[b]
    for j in range(0,len(vocabulary[i])):
        if vocabulary[i][j] in fullLettSet:
            words[j][fullLettSet.find(vocabulary[i][j])].append(vocabulary[i])

# same for wordsRev
for i in range(30):
    a=[]
    for j in range(len(fullLettSet)):
        a.append([])
    wordsRev.append(a)
for i in range(14400):
    for j in range(0,len(vocabulary[i])):
        if vocabulary[i][::-1][j] in fullLettSet:
            wordsRev[j][fullLettSet.find(vocabulary[i][::-1][j])].append(vocabulary[i][::-1])

# alphabetic numeration for descriptions list
for i in range(10):
    for j in range(10):
        abcNum100.append("abcdefgijk"[i]+"abcdefgijk"[j])

def alphabeticNr(nr):
    return(abcNum100[nr])

def shiftCell(cell, direct, stepsNr):
    if direct == "south":
        return([cell[0]+stepsNr, cell[1]])
    if direct == "north":
        return([cell[0]-stepsNr, cell[1]])
    if direct == "east":
        return([cell[0], cell[1]+stepsNr])
    if direct == "west":
        return([cell[0], cell[1]-stepsNr])

def goodWords(crossNumbers,crossLetters): # list of words with appropriate crossing letters
    gW = vocabulary
    if crossNumbers[0]==0:
        gW = words[0][fullLettSet.find(crossLetters[0])]
    for i in range(len(crossNumbers)):
            gWcut = list(set(gW) - set(wordLength[crossNumbers[i]])) # cut words longer then "crossNumbers[i]"
            gWnew = list(set(words[crossNumbers[i]][fullLettSet.find(crossLetters[i])]) & set(gW)) # get words with appropriate "crossNumbers[i]"
            gW = list(set(gWcut) | set(gWnew))
    return(gW)

def goodWordsRev(crossNumbers,crossLetters): # same for reversed words
    gW = vocabularyRev
    if crossNumbers[0]==0:
        gW = wordsRev[0][fullLettSet.find(crossLetters[0])]
    for i in range(len(crossNumbers)):
            gWcut = list(set(gW) - set(wordLengthRev[crossNumbers[i]]))
            gWnew = list(set(wordsRev[crossNumbers[i]][fullLettSet.find(crossLetters[i])]) & set(gW))
            gW = list(set(gWcut) | set(gWnew))
    return(gW)

def sides(cell, direct, stepsNr): # check if there are filled cells touching specified area
    if direct == "south":
        if array[cell[0]+stepsNr][cell[1]+1]!="." or array[cell[0]+stepsNr][cell[1]-1]!=".":
            return("filled")
        else:
            return("empty")
    if direct == "north":
        if array[cell[0]-stepsNr][cell[1]+1]!="." or array[cell[0]-stepsNr][cell[1]-1]!=".":
            return("filled")
        else:
            return("empty")
    if direct == "east":
        if array[cell[0]+1][cell[1]+stepsNr]!="." or array[cell[0]-1][cell[1]+stepsNr]!=".":
            return("filled")
        else:
            return("empty")
    if direct == "west":
        if array[cell[0]+1][cell[1]-stepsNr]!="." or array[cell[0]-1][cell[1]-stepsNr]!=".":
            return("filled")
        else:
            return("empty")

def goodStartFromEmptyCell(cell, direct): # used in goodStart function
    if direct=="north" and ((array[cell[0]+1][cell[1]]!=".") or (array[cell[0]][cell[1]-1]!=".") or (array[cell[0]][cell[1]+1]!=".")):
        return(0)
    if direct=="south" and ((array[cell[0]-1][cell[1]]!=".") or (array[cell[0]][cell[1]-1]!=".") or (array[cell[0]][cell[1]+1]!=".")):
        return(0)
    if direct=="west" and ((array[cell[0]][cell[1]+1]!=".")  or (array[cell[0]-1][cell[1]]!=".") or (array[cell[0]+1][cell[1]]!=".")):
        return(0)
    if direct=="east" and ((array[cell[0]][cell[1]-1]!=".")  or (array[cell[0]-1][cell[1]]!=".") or (array[cell[0]+1][cell[1]]!=".")):
        return(0)
    return(1)

def goodStartFromFilledCell(cell, direct): # used in goodStart function
    if direct=="north" and (array[cell[0]+1][cell[1]]!=".") :
        return(0)
    if direct=="south" and (array[cell[0]-1][cell[1]]!=".")  :
        return(0)
    if direct=="west" and (array[cell[0]][cell[1]+1]!="." or (array[cell[0]][cell[1]-1]!="." and array[cell[0]][cell[1]-2]!=".")):
        return(0)
    if direct=="east" and (array[cell[0]][cell[1]-1]!="."):
        return(0)
    return(1)

def goodStart(cell, direct): # if cell is appropriate to begin word with
    if array[cell[0]][cell[1]]==".":
        return(goodStartFromEmptyCell(cell, direct))
    else:
        return(goodStartFromFilledCell(cell, direct))

def maxLength(cell, direct): # maximal possible word length from "cell" in "direction"
    for i in range(25):
        if str(array[shiftCell(cell, direct, i+1)[0]][shiftCell(cell, direct, i+1)[1]]) in "123456789":
            return(i)
        if sides(cell, direct, i+1)=="filled" and array[shiftCell(cell, direct, i+1)[0]][shiftCell(cell, direct, i+1)[1]]==".":
            return(i+1)
        if array[shiftCell(cell, direct, i+1)[0]][shiftCell(cell, direct, i+1)[1]]!="." and array[shiftCell(cell, direct, i+2)[0]][shiftCell(cell, direct, i+2)[1]]!=".":
            return(i+1)
    return(25)

def crossings(cell, direct,lengthMax): # returns list of crossing positions numbers and corresponding list of letters (counting from current cell)
    crossPositions=[]
    crossLetters=[]
    for i in range(min(lengthMax+1,(maxLength(cell, direct)+1))):
        if array[shiftCell(cell, direct, i)[0]][shiftCell(cell, direct, i)[1]]!=".":
            crossPositions.append(i)
            crossLetters.append(array[shiftCell(cell,direct, i)[0]][shiftCell(cell,direct, i)[1]])
    return([crossPositions,crossLetters])

def firstCrossing(cell, direct): # counting from next cell (not current)
    i=1
    while array[shiftCell(cell,direct,i)[0]][shiftCell(cell,direct,i)[1]]=="." and i<(min(30, maxLength(cell,direct))):
        i+=1
    return(i)



def goodLetters(word, gL): # check if letters on specified positions are "good"
    for i in gL:
        if word[i] not in goodLettSet:
            return(0)
    return(1)

def findWord(cell, direct, lengthMin, lengthMax, goodLettSet):
    if maxLength(cell, direct)<lengthMin:
        return("no match")
    if crossings(cell, direct, lengthMax)[0]==[]  or crossings(cell, direct, lengthMax)[0][0]>lengthMax:
        new_dict = vocabulary
    else:
        new_dict = goodWords(crossings(cell, direct, lengthMax)[0],crossings(cell, direct, lengthMax)[1])

    new_dict = list(set(new_dict)&set(wordLength[lengthMin])-set(wordLength[lengthMax+1]))
    new_dict = sample(new_dict, len(new_dict))
    for word in new_dict:
        if (len(word) in  crossings(cell, direct, lengthMax)[0])!=True or crossings(cell, direct, lengthMax)[0]==[]:
            if len(word)<=lengthMax and len(word)>=lengthMin:
                if goodLetters(word, goodLettSet) == 1:
                    if len(word)<= maxLength(cell, direct):
                        if word not in usedWords:
                            return(word)
    return("no match")

def findWordRev(cell, direct, lengthMin, lengthMax, goodLettSet):
    if maxLength(cell, direct)<lengthMin:
        return("no match")
    if crossings(cell, direct, lengthMax)[0]==[] or crossings(cell, direct, lengthMax)[0][0]>lengthMax:
        new_dict = vocabularyRev
    else:
        new_dict = goodWordsRev(crossings(cell, direct, lengthMax)[0],crossings(cell, direct, lengthMax)[1])

    new_dict = list(set(new_dict)&set(wordLengthRev[lengthMin])-set(wordLengthRev[lengthMax+1]))
    new_dict = sample(new_dict, len(new_dict))
    for word in new_dict:
        if (len(word) in  crossings(cell, direct, lengthMax)[0])!=True or crossings(cell, direct, lengthMax)[0]==[]:
            if len(word)<=lengthMax and len(word)>=lengthMin:
                if goodLetters(word, goodLettSet) == 1:
                    if len(word)<= maxLength(cell, direct):
                        if word not in usedWords:
                            return(word)
    return("no match")

def printWord(cell, direct, lenMin, lenMax, goodLettSet): # update array with word found in "findWord", descriptions, coordinates, and usedWords
    if goodStart(cell,direct)==0:
        return("no match")
    if direct in ('north', 'west'):
        word = findWordRev(cell, direct, lenMin, min(maxLength(cell, direct),lenMax), goodLettSet)
    else:
        word = findWord(cell, direct, lenMin, min(maxLength(cell, direct),lenMax), goodLettSet)
    if word!="no match" and word!=None:
        i = 0
        for lett in word:
            array[shiftCell(cell, direct, i)[0]][shiftCell(cell, direct, i)[1]]=lett
            i=i+1
        if direct in ('west','north'):
            newWord = word[::-1]
        else:
            newWord = word
        for v in range(len(vocabulary)):
            if vocabulary[v]==newWord:
                break
        descr.append(descriptions[v][1:len(descriptions[v])])
        usedWords.append(word)
        usedWords.append(word[::-1])
        if direct in ("south", "east"):
            crdn=[cell[0]+1,cell[1]+1]
        else:
               crdn=[shiftCell(cell, direct, len(word)-1)[0]+1,shiftCell(cell, direct, len(word)-1)[1]+1]
        coord.append(crdn)
        coordText.append(str(crdn[0])+":"+str(crdn[1]))

        if direct in ("south", "north"):
            directions.append("ver")
        else:
            directions.append("hor")
        return(word)
    else:
        return("no match")

def printWordWithShift(cell, direct, lenMin, lenMax, goodLettSet, shiftN): # if word not found shift back by one cell and try again (maxLength grows by 1, "shiftN" - iterations limit)
    word = printWord(cell, direct, max(firstCrossing(cell, direct)+1,lenMin),maxLength(cell,direct)+1,[])
    newCell=cell
    for i in range(1,shiftN):
        if word == "no match":
            newCell=shiftCell(newCell, direct, -i)
            word = printWord(newCell, direct, max(firstCrossing(cell, direct)+i+1,lenMin),maxLength(cell,direct)+1,[])
    return(word)

def printWordWithShiftCrossN(cell, direct, lenMin, lenMax, goodLettSet, shiftN, crossN): # if word not found shift back by one cell and try again (maxLength grows by 1, "shiftN" - iterations limit)
    word = printWordWithShift(cell, direct, max(firstCrossing(cell, direct)+1,lenMin),maxLength(cell,direct)+1,[],shiftN)
    newCell=cell
    for i in range(1,shiftN):
        if word == "no match":
            newCell=shiftCell(newCell, direct, -i)
            word = printWord(newCell, direct, max(firstCrossing(cell, direct)+i+1,lenMin),maxLength(cell,direct)+1,[],shiftN)
    return(word)

def printWordWithCrossN(cell,direct, maxLen,goodLettSet, crossN): # crossN - minimal nr of crossings in the word
    if array[cell[0]][cell[1]]==".":
        firstPos = 0
    else:
        firstPos = 1
    if len(crossings(cell, direct, 20)[0])>=crossN:
        minLen=crossings(cell, direct, 20)[0][crossN-1-firstPos]
    else:
        minLen = 100
    word = printWord(cell, direct, minLen,maxLen,goodLettSet)
    return(word)

def fillAreaHoriz(cell, direct, rows):
    i=0
    word = printWordWithShift(cell, direct, firstCrossing(cell, direct)+1,20,[],2)
    while i<=rows:
        if word!="no match":
            cell = shiftCell(cell, "south", 2)
            i+=2
        else:
            cell = shiftCell(cell, "south", 1)
            i+=1
        word = printWordWithShift(cell, direct, firstCrossing(cell, direct)+1,20,[],2)

def fillAreaVert(cell, height):
    i=0
    startRow = cell[0]
    word = printWordWithCrossN(cell,"south", height+startRow-cell[0]-1,[], 2)
    while cell[0] < startRow + height:
        if word!="no match":
            cell = shiftCell(cell, "south", len(word)+1)
            i+=len(word)+1
        else:
            cell = shiftCell(cell, "south", 1)
            i+=1
        word = printWordWithCrossN(cell,"south", height+startRow-cell[0]-1,[], 2)

def fillCenterColumns(cell, height):
    word = printWord(cell, "south", 15,min(height, 20),[])
    restHeight = height - len(word)
    cell = shiftCell(cell, "south", height)
    word = printWord(cell, "north", restHeight,min(restHeight, 20),[])

def leftWing(iniRow, iniCol):
    cell=[iniRow,iniCol]
    word = printWord(cell,'east',15,17,[])
    lenPrev = len(word)
    cell = shiftCell(cell, "south", 3)

    for i in range(10):
        iniCell=cell
        word = printWord(cell,'east',15,17,[])
        cellEnd = shiftCell(cell, "east", min(len(word),lenPrev))
        lenPrev = len(word)
        gLett = []
        cell = shiftCell(cell,'north',4)
        word = printWord(cell,"south",5,6,gLett)
        while word=="no match":
            cell = shiftCell(cell,"east",1)
            word = printWord(cell,"south",5,6,gLett)

        cell = shiftCell(cellEnd, "north", 4)
        word = printWord(cell,"south",5,6,gLett)
        while word=="no match":
            cell = shiftCell(cell,"west",1)
            word = printWord(cell,"south",5,6,gLett)
        cell = shiftCell(iniCell,'south',3)

def rightWing(iniRow, iniCol):
    cell=[iniRow,iniCol]
    word = printWord(cell,'west',15,17,[])
    lenPrev = len(word)
    cell = shiftCell(cell, "south", 3)

    for i in range(10):
        iniCell=cell
        word = printWord(cell,'west',15,17,[])
        cellEnd = shiftCell(cell, "west", min(len(word),lenPrev))
        lenPrev = len(word)
        gLett = []
        cell = shiftCell(cell,'north',4)
        word = printWord(cell,"south",5,6,gLett)
        while word=="no match":
            cell = shiftCell(cell,"west",1)
            word = printWord(cell,"south",5,6,gLett)
        cell = shiftCell(cellEnd, "north", 4)
        word = printWord(cell,"south",5,6,gLett)
        while word=="no match":
            cell = shiftCell(cell,"east",1)
            word = printWord(cell,"south",5,6,gLett)

        cell = shiftCell(iniCell,'south',3)


descr1 = []
dString1=[]
def printShortDescr():
    for d in descr:
        for nr in range(10):
            d = d.replace("  ", " ")
        descr1.append(d)
        
    i=0
    for direction, d, c in zip(directions, descr1, coord):
           
        if len(str(c[0]))==1:
            coordR="0"+str(c[0])
        else:
            coordR=str(c[0])
        if len(str(c[1]))==1:
            coordC="0"+str(c[1])
        else:
            coordC=str(c[1])
        newText = direction + "   "+alphabeticNr(c[0])+":"+alphabeticNr(c[1])+coordR+":"+coordC+"___"+str(i)+"&&&"+d
        dString.append(newText)
        i+=1
    dString.sort()

   
    print("По горизонтали:\n")
    #dString1.append("По горизонтали:")

    i=1
    for item in dString:
        if item[0:3]=="hor":
            print(str(i)+"  "+item[item.find("&&&")+3:])
            dString1.append(str(i)+"  "+item[item.find("&&&")+3:])
            descrH.append(item[item.find("&&&")+3:])
            i+=1
        else:
            vert = i+1
            break
    i=1
    print("\nПо вертикали:\n")
    #dString1.append("По вертикали:")
    for item in dString[vert-3:]:
            print(str(i-1)+"  "+item[item.find("&&&")+3:])
            dString1.append(str(i-1)+"  "+item[item.find("&&&")+3:])
            descrV.append(item[item.find("&&&")+3:])
            i+=1


def printArray(firstRow, lastRow):
  #  for j in range(secRow+1):
  #      for i in range(0, secRow+1):
  #          if i<firstRow or j<firstRow:
  #              fnt="Arial 9 bold"
  #              bckgr="white" #113f45"
  #              frgr="#555" #fff"
  #          else:
  #              fnt="Arial 11 bold"
  #              bckgr="white" #113f45"
  #              frgr="#555" #fff"

           # if array[j][i]!= ".":
           #     label = Label(text=array[j][i], justify=CENTER, bd="0", font=fnt, width=2, background=bckgr, foreground=frgr) #893f45 9B5150 pady="0", padx="0",
           #     label.grid(row=j, column=i)
           # else:
           #     if (array[j+1][i] in fullLettSet and array[j+2][i] in fullLettSet)  or (array[j][i+1] in fullLettSet and array[j][i+2] in fullLettSet):
           #         btn = Button(text=str(j+1)+":"+str(i+1),  width="2",height="2", font="Arial 5", command=clickWordButton, background="maroon", foreground="white")
           #         btn.grid(row=j, column=i)
    #btn = Button(text="Get description",  width="13",height="3", font="Arial 10", command=clickGetFullDescr) #, background="#ddd", foreground="black",)
    #btn.grid(row=38, column=35, columnspan=6, rowspan=4)

    for string in array[firstRow:lastRow]:
        strOutput=""
        for symb in string[firstRow:lastRow]:
            if str(symb) in ["0","1","2","3","4","5","6","7","8","9"]:
                symb = " 0"+str(symb)+" "
            elif symb == ".":
                symb="   "
            else:
                symb=" "+str(symb)+" "
            strOutput=strOutput+str(symb)
        print(strOutput)#+"\n")


def clickGetFullDescr():
    wdth = 80
    nr = nrEntry.get()
    descrH = str(nr) + "_" + descrByNr(nr)[0]
    descrV = str(nr) + "_" + descrByNr(nr)[1]
    descrH = descrH[:80].ljust(wdth,"_") + "\n" + descrH[80:160].ljust(wdth,"_") + "\n" + descrH[160:240].ljust(wdth,"_")
    descrV = descrV[:80].ljust(wdth,"_") + "\n" + descrV[80:160].ljust(wdth,"_") + "\n" + descrV[160:240].ljust(wdth,"_")
    #label = Label(text=descrH, justify=LEFT, bd="0", width=wdth, height="3", font="Arial 10", background="white", foreground="black") #893f45 9B5150 pady="0", padx="0",
    #label.grid(row=36,  column=1, columnspan=35, rowspan=3)
    #label = Label(text=descrV, justify=LEFT, bd="0", width=wdth, height="3", font="Arial 10", background="white", foreground="black") #893f45 9B5150 pady="0", padx="0",
    #label.grid(row=39,  column=1, columnspan=35, rowspan=3)

def descrByNr(nr):
	return(["По горизонтали: " + dString[int(nr)-1][23::], "По вертикали: " + dString[int(nr)+hL[0]-2][23::]])


class Callback:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
    def __call__(self):
        self.func(*self.args, **self.kwargs)

currI=0
currJ=0
currWord = ""
currDir = ""
openedCoord = []
openedWords=[]


def clickWordButton(coord):

    global currI
    global currJ
    global currWord
    global currDir
    
    i,j, currNV, currNH = coord
    selectedWord=""
    #if array[j+1][i] in fullLettSet and array[j+2][i] in fullLettSet:
    if currNV>0 and currNH>0:
        if currDir == "vert":
            clr="blue"
            direct = "hor"
            if ([i, j, direct] in openedCoord):
                return
            dText = "по горизонтали:"
            currN = currNH-2
            currDescr = descrH
            nr = 1
            while array[j][i+nr] != ".":
                selectedWord = selectedWord + array[j][i+nr]
                nr+=1
                label = Label(text=str(currN+1) + " " + dText + " " + currDescr[currN][:70]+"\n"+currDescr[currN][70:140]+"\n"+currDescr[currN][140:], justify=CENTER, bd="0", font="Arial 9 bold", width=87, height=3, background="white", foreground=clr)
                label.grid(row=38, column=3, columnspan=35, rowspan=3)
        else:
            clr="maroon"
            direct = "vert"
            if ([i, j, direct] in openedCoord):
                return
            dText = "по вертикали:"
            currN = currNV
            currDescr = descrV
            nr = 1
            while array[j+nr][i] != ".":
                selectedWord = selectedWord + array[j+nr][i]
                nr+=1
                label = Label(text=str(currN) + " " + dText + " " + currDescr[currN][:70]+"\n"+currDescr[currN][70:140]+"\n"+currDescr[currN][140:], justify=CENTER, bd="0", font="Arial 9 bold", width=87, height=3, background="white", foreground=clr)
                label.grid(row=38, column=3, columnspan=35, rowspan=3)
        currI = i
        currJ = j
        currWord = selectedWord
        currDir = direct
        return
            
    if currNV>0:
        clr="maroon"
        direct = "vert"
        if [i, j, direct] in openedCoord:
            return
        dText = "по вертикали:"
        currN = currNV
        currDescr = descrV
        nr = 1
        while array[j+nr][i] != ".":
            selectedWord = selectedWord + array[j+nr][i]
            nr+=1
            label = Label(text=str(currN) + " " + dText + " " + currDescr[currN][:70]+"\n"+currDescr[currN][70:140]+"\n"+currDescr[currN][140:], justify=CENTER, bd="0", font="Arial 9 bold", width=87, height=3, background="white", foreground=clr)
            label.grid(row=38, column=3, columnspan=35, rowspan=3)            
            
    #if array[j][i+1] in fullLettSet and array[j][i+2] in fullLettSet:
    if currNH>0:
        clr="blue"
        direct = "hor"
        if [i, j, direct] in openedCoord:
            return
        dText = "по горизонтали:"
        currN = currNH-2
        currDescr = descrH
        nr = 1
        while array[j][i+nr] != ".":
            selectedWord = selectedWord + array[j][i+nr]
            nr+=1
            label = Label(text=str(currN+1) + " " + dText + " " + currDescr[currN][:70]+"\n"+currDescr[currN][70:140]+"\n"+currDescr[currN][140:], justify=CENTER, bd="0", font="Arial 9 bold", width=87, height=3, background="white", foreground=clr)
            label.grid(row=38, column=3, columnspan=35, rowspan=3)
            
    currI = i
    currJ = j
    currWord = selectedWord
    currDir = direct
    
          
      
def fillWindow(firstRow=2, secRow=45):
    nrH=1
    nrV=1
    for j in range(secRow+1):
        for i in range(0, secRow+1):
            if i<firstRow or j<firstRow:
                fnt="Arial 7 bold"
                bckgr="white" #113f45"
                frgr="#555" #fff"
            else:
                fnt="Arial 9 bold"
                bckgr="white" #113f45"
                frgr="white" #"#555" #fff"
                
            if array[j][i]!= ".":
                label = Label(text=array[j][i], justify=CENTER, bd="0", font=fnt, width=2, height=1, background=bckgr, foreground=frgr) #893f45 9B5150 pady="0", padx="0",
                label.grid(row=j, column=i)
            else:
                
                if (array[j+1][i] in fullLettSet and array[j+2][i] in fullLettSet):
                    currNV = nrV
                    nrV+=1
                else:
                    currNV = 0

                if (array[j][i+1] in fullLettSet and array[j][i+2] in fullLettSet):
                    currNH = nrH+1
                    nrH+=1
                else:
                    currNH = 0
                    
                currNFull = ""
                div = ""
                
                if currNH >0:
                    clr="blue"
                    currNFull = str(currNH-1)
                    div = "/"

                if currNV >0:
                    clr="maroon"
                    currNFull = currNFull + div + str(currNV)
                    
                if "/" in currNFull:
                    clr = "purple"
                    
                if len(currNFull)>0:
                    btn = Button(text=str(currNFull), command=Callback(clickWordButton, [i,j, currNV, currNH]), width="2", height="1", font="Arial 7", background=clr, foreground="white")
                    btn.grid(row=j, column=i)
                    
    btn = Button(text="Check answer",  width="10", height="3", font="Arial 10", command=checkAnswer) #, background="#ddd", foreground="black",)
    btn.grid(row=38, column=35, columnspan=6, rowspan=4)

    btn = Button(text="Help",  width="10", height="3", font="Arial 10", command=helpAnswer) #, background="#ddd", foreground="black",)
    btn.grid(row=38, column=41, columnspan=6, rowspan=4)


guessed = 0
helped = 0

def checkAnswer():
    global currWord
    global currDir
    global guessed
    global guessedLbl

    if message.get().replace("ё", "е").replace("й", "и").upper() == currWord and currWord not in openedWords:
        nr = 1

        if currDir == "vert":
            while array[currJ+nr][currI] != ".":
                label = Label(text=array[currJ+nr][currI], justify=CENTER, bd="0", font="Arial 9 bold", width=2, background="white", foreground="black") #893f45 9B5150 pady="0", padx="0",
                label.grid(row=currJ+nr, column=currI)
                nr+=1
        else:
            while array[currJ][currI+nr] != ".":
                label = Label(text=array[currJ][currI+nr], justify=CENTER, bd="0", font="Arial 9 bold", width=2, background="white", foreground="black") #893f45 9B5150 pady="0", padx="0",
                label.grid(row=currJ, column=currI+nr)
                nr+=1

        message.set("")
        guessed+=1
        guessedLbl["text"]=(str(guessed))
        openedCoord.append([currI,currJ,currDir])
        openedWords.append(currWord)

def helpAnswer():
    global currWord
    global currDir
    global helped
    global helpedLbl
    
    if currWord not in openedWords:
        nr = 1

        if currDir == "vert":
            while array[currJ+nr][currI] != ".":
                label = Label(text=array[currJ+nr][currI], justify=CENTER, bd="0", font="Arial 9 bold", width=2, background="white", foreground="red") #893f45 9B5150 pady="0", padx="0",
                label.grid(row=currJ+nr, column=currI)
                nr+=1
        else:
            while array[currJ][currI+nr] != ".":
                label = Label(text=array[currJ][currI+nr], justify=CENTER, bd="0", font="Arial 9 bold", width=2, background="white", foreground="red") #893f45 9B5150 pady="0", padx="0",
                label.grid(row=currJ, column=currI+nr)
                nr+=1

        message.set("")     
        helped+=1
        helpedLbl["text"]=str(helped)
        openedCoord.append([currI,currJ,currDir])
        openedWords.append(currWord)
		
		
def fillDescr():

    hor = "По горизонтали: \n"
    vertB = "По вертикали: \n"
    vertR = ""    
    i=1
    for item in dString:
        if item[0:3]=="hor":
            #hor = hor + "(" +str(i) +")" + item[21:50]+">> ("+item[11:16]+")\n"
            hor = hor + dString1[i-1][:30] + "  " + item[11:16]+ "\n"
            i+=1
        else:
            hor = hor + "\n"
            break
    horLen = i
    hL.append(horLen)
    i=1
    for item in dString[horLen-1:int((len(dString)-3)/2)]:
        #vertB = vertB +"(" +str(i) +")" + item[21:50]+">> ("+item[11:16]+")\n"
        vertB = vertB + dString1[horLen + i - 1][:30]  + "  " + item[11:16]+ "\n"
        i+=1
    for item in dString[horLen+i-2:len(dString)]:
        #vertR = vertR +"(" +str(i) +")" + item[21:50]+">> ("+item[11:16]+")\n"
        vertR = vertR + dString1[horLen + i - 1][:30]  + "  " + item[11:16]+ "\n"
        i+=1

    #print("leftbox\n")
    #print(hor)
    #print(vertB)
    #print("rightbox\n")
    #print(vertR)
    
    descrList1 = hor + vertB
    descrList2 = vertR   
    label = Label(text=descrList1, bd="0", justify=LEFT,  font="Arial 8", width=40, background="#fff")#893f45 9B5150 pady="0", padx="0",
    label.grid(row=0, column = 49, columnspan=45,rowspan=70)
    label = Label(text=descrList2, bd="0", justify=LEFT, font="Arial 8", width=40, background="#fff")#893f45 9B5150 pady="0", padx="0",
    label.grid(row=0, column = 97, columnspan=45,rowspan=70)
    

def main(iniRow=4, iniCol=4):
    leftWing(iniRow, iniCol)
    rightWing(iniRow, iniCol+40)
    fillCenterColumns([iniRow, iniCol+18], 30)
    fillAreaHoriz([iniRow, iniCol+18], "west", 30)
    fillCenterColumns([iniRow, iniCol+22], 30)
    fillAreaHoriz([iniRow, iniCol+22], "east", 30)
    fillAreaHoriz([iniRow, iniCol+18], "east", 30)
    fillAreaHoriz([iniRow, iniCol+22], "west", 30)
    fillAreaHoriz([iniRow, iniCol+18], "west", 30)
    fillAreaHoriz([iniRow, iniCol+22], "east", 30)
    fillAreaVert([iniRow-1, iniCol+6], 33)
    fillAreaVert([iniRow-1, iniCol+8], 33)
    fillAreaVert([iniRow-1, iniCol+32], 33)
    fillAreaVert([iniRow-1, iniCol+34], 33)
    fillAreaVert([iniRow-1, iniCol+15], 33)
    fillAreaVert([iniRow-1, iniCol+16], 33)
    fillAreaVert([iniRow-1, iniCol+24], 33)
    fillAreaVert([iniRow-1, iniCol+25], 33)
    fillAreaHoriz([iniRow, iniCol+18], "west", 30)
    fillAreaHoriz([iniRow, iniCol+22], "east", 30)
    fillAreaVert([iniRow-1, iniCol+13], 33)
    fillAreaVert([iniRow-1, iniCol+14], 33)
    fillAreaVert([iniRow-1, iniCol+15], 33)
    fillAreaVert([iniRow-1, iniCol+16], 33)
    fillAreaVert([iniRow-1, iniCol+24], 33)
    fillAreaVert([iniRow-1, iniCol+25], 33)
    fillAreaVert([iniRow-1, iniCol+26], 33)
    fillAreaVert([iniRow-1, iniCol+27], 33)
    printArray(1,45)
    printShortDescr()


main()

window = Tk()
window.title("Crossword")
fillWindow()
fillDescr()
message = StringVar()
wordEntry = Entry(textvariable=message, width=50)
wordEntry.grid(row=41, column=3, columnspan=20, rowspan=2)
guessedLbl = Label(foreground="black", text="0", font="Arial 12 bold")
helpedLbl = Label(foreground="red", text="0", font="Arial 12 bold")
guessedLbl.grid(row=38, column=1, columnspan=3)
helpedLbl.grid(row=40, column=1, columnspan=3)
window.mainloop()
