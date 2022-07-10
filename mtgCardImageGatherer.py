#mtgCardImageGatherer.py

#7-9-2022
#Logan White
#This takes a .txt file with with 1 card per line formatted as "# cardname", 
# it currently ignores the # as I designed this for commander decks, but it can accept any number of card images


#when started it opens a dialog to choose the decklist file
#then another dialog is opened to choose what folder to save the images to
#There is sleep(.1) call between http requests to scryfall to respect their API guidelines 

import requests
import os
import io
from PIL import Image
import json
from tkinter.filedialog import askopenfile, askdirectory
from time import sleep
    
    #choose the file with a list of cards
    #format as # cardname
cardListFile = askopenfile(filetypes=[("text files",".txt")], title="Choose the decklist file", initialdir= os.getcwd())
    #error prevention
if(cardListFile == None):
    print("No list of cards file Chosen")
    exit()

    #choose the directory to save the cards
folder = askdirectory(title="Choose directory to save the cards into", initialdir= os.getcwd())
    #error prevention
if(len(folder) == 0):
    print("No Folder Chosen")
    exit()

cardListString = cardListFile.read()
cardList = cardListString.split("\n")
for x in cardList:
    if(x == ""):
        print("Reached end of list")
        exit()
    print(x[2:])
    print(cardListFile.read())

    #cardToSearch = "Altar of Bhaal // Bone Offering"
    cardToSearch = x[2:]
    temp = requests.get("https://api.scryfall.com/cards/search?q="+ cardToSearch)
    temp.raise_for_status()
    #print(temp.content)
    cardOBJ = json.loads(temp.content)
    dataDict = cardOBJ["data"]
    #print(dataDict)


    url = dataDict[0]["image_uris"]["png"]
    print(url)

    temp = requests.get(url)
    temp.raise_for_status()
    im = Image.open(io.BytesIO(temp.content))
    #im.show()
    print(folder)
    imageFileName = cardToSearch.replace('/','').replace(' ','').strip()
    im.save(folder +"/"+ imageFileName +".png")
    sleep(.1)



