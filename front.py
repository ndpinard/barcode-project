import pandas as pd
from db import Database
from datetime import datetime
import posts
from pull import Pull
from scannertest import Vscan
from airdropped import Findy
from singleimage import Oneimage


pull = Pull()
startscan = Vscan()
database = Database()
image = Oneimage()
finder = Findy()

with open("config.txt","r") as file:
    path = file.read()

def menu():
    print("Welcome to PyVentory, what would you like to do?")
    print("1. View current inventory")
    print("2. Scan items")
    print("3. Input item manually")
    print("4. Update quantities")
    print("5. Airdrop barcodes")
    print("6. Change configurations")
    print("0. Exit")
    print("To bring the menu back up type 'help'.")
menu()
while True:
    x = str(input(":"))
    if x == "0":
        break
    elif x == "1":
        print(database.pandasview())
    elif x == "2":
        startscan.startscan()
    elif x == "3":
        name = str(input("What is the item's name? "))
        upc = input("What is the items barcode number? ")
        #expiration = int(input("How many days approximately until the item has expired? "))
        database.insert( name, upc)
    elif x == "4":
        print(database.pandasview())
        print("When finished updating quantities type 'stop'.")
        while True:
            id = str(input("Select an item by id: "))
            if id == "stop":
                break
            quantity = str(input("Enter the desired quantity: "))
            if quantity == "stop":
                break
            i = database.selectbyid(quantity,id)
        print("Finished updating quantities")
    elif x == "5": #batch image barcode identification >todo< create a class for this
        print("Finding all files...")
        files = finder.findall(path)
        print("Processing all files...")
        for file in files:
            upc = image.process(file)
            testupc = None
            sqlcheck = len(database.checkforitem(upc))
            if sqlcheck is 0: #check if data is stored in mysql before asking api server
                testupc = pull.pullitem(upc)
            if sqlcheck is 0 and testupc is None: #data does not exist locally or in api db
                #cv2.imshow(file)
                name = input("What is the name of this item: ")
                #cv2.destroyallwindows()
                database.insert(name,upc)
                print("Inserted {} into the database.".format(name))
            elif sqlcheck is not 0: # data is stored locally already - increase quantity instead
                name = str(database.findnamebyupc(upc))
                name = name.strip("[](),'")
                database.selectbyupc(upc)
                print("Increased quantity of {} by one.".format(str(name)))
            elif testupc is not None: # when found from an api req store it in db
                name = testupc
                database.insert(testupc,upc)
                print("Inserted {} into the database from api database.".format(name))
    elif x == "6":
        check = input("Current filepath is {}, would you like to change this? y/n:".format(str(path)))
        if check == "y":
            path = input("What is the absolute path for your airdrop folder?")
            with open("config.txt","w") as file:
                file.write(path)
                file.close()
    elif x == "help":
        menu()
