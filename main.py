import pymongo
import os
import datetime
import time
import dns
import random
key=os.getenv("KEY")
client = pymongo.MongoClient(key)
db = client.bank
def menu():
  print("What would you like to do? T: Transfer | M: Mine | B: Balance | H: History")
  task=input("PlexCoin ~ ")
  if task=="B" or task=="b":
    user=input("Who's balance would you like to check: ")
    collection=db.wallet
    regex_query = { "Username" : {"$regex" : user} }
    result = collection.find( regex_query )
    for doc in result:
      print("Balance for "+doc["Username"]+": "+str(doc["Wallet"]))
      menu()
  if task=="T"or task=="t":
    os.system('clear')
    time.sleep(0.5)
    print("Please login to authenticate your transfers session!")
    loginuser=input("Username: ")
    loginpass=input("Password: ")
    collection=db.authentication
    regex_query = { "Username" : {"$regex" : loginuser} }
    result = collection.find(regex_query)
    correctUser = False
    for doc in result:
        if doc["Username"]==loginuser:
          if doc["Password"]==loginpass:
            correctUser = True
    if correctUser == True:
      transferto=input("Who are you transferring to: ")
      transferamt=input("How much would you like to transfer: ")
      collection=db.authentication
      regex_query = { "Username" : {"$regex" : transferto} }
      resultb = collection.find( regex_query )
      alreadya = False
      for doc in resultb:
        if doc["Username"] == transferto:
          alreadya=True
      if alreadya == False:
        print("The account you typed does not exist!")
        menu()
      collection=db.wallet
      if alreadya == True:
        regex_query = { "Username" : {"$regex" : loginuser} }
        resulta = collection.find( regex_query )
        for doc in resulta:
          if doc["Username"] == loginuser:
            alreadyb=True
            prevbal=doc["Wallet"]
        if alreadyb==True:
          transferamt=float(transferamt)
          if float(transferamt) <= prevbal:
            newbal=prevbal-transferamt
            regex_query = { "Username" : {"$regex" : transferto} }
            resultc = collection.find( regex_query )
            for doc in resultc:
              if doc["Username"]==transferto:
                prevbalb=float(doc["Wallet"])
                newbalb=float(prevbalb)+float(transferamt)
            collection.replace_one({"Username": loginuser},{"Username":loginuser,"Wallet":newbal})
            print("Transfer complete!")
            collection.replace_one({"Username": transferto},{"Username":transferto,"Wallet":newbalb})
            doc={"From":loginuser,"To":transferto,"Amount":transferamt,"Time":datetime.datetime.now()}
            collection=db.logs
            collection.insert_one(doc)
            menu()
  if task=="M"or task=="m":
    os.system('clear')
    time.sleep(0.5)
    print("Please login to authenticate your mining session!")
    loginuser=input("Username: ")
    loginpass=input("Password: ")
    collection=db.authentication
    regex_query = { "Username" : {"$regex" : loginuser} }
    result = collection.find(regex_query)
    correctUser = False
    for doc in result:
        if doc["Username"]==loginuser:
          if doc["Password"]==loginpass:
            correctUser = True
    if correctUser == True:
      collection=db.wallet
      print("Correct login details!")
      time.sleep(0.2)
      os.system("clear")
      print("===========Mining===========")
      print("Mining Session started.")
      x=0
      y=0
      while x==0:
        y=y+0.0001
        os.system('clear')
        print("Mining ("+str(y)+" so far)")
        time.sleep(0.2)
        regex_query = { "Username" : {"$regex" : loginuser} }
        result = collection.find( regex_query )
        already = False
        for doc in result:
          if doc["Username"] == loginuser:
            already=True
            prevbal=doc["Wallet"]
        if already==True:
          newbal=prevbal+0.0001
          collection.replace_one({"Username": loginuser, "Wallet":prevbal},{"Username":loginuser,"Wallet":newbal})
    else:
      print("Incorrect login details!")
      menu()
def roll():
  collection=db.authentication
  print("Type S to signup and L to login")
  task=input("S/L: ")
  if task=="S"or task=="s":
    newname=input("Pick a username: ")
    newpass=input("Pick a password: ")
    regex_query = { "Username" : {"$regex" : newname} }
    result = collection.find( regex_query )
    already = False
    for doc in result:
      if doc["Username"] == newname:
        already=True
    if already == False:
      doc={"Username":newname,"Password":newpass}
      collection.insert_one(doc)
      collection=db.wallet
      doc={"Username":newname,"Wallet":0}
      collection.insert_one(doc)
      print("Account created! Reload and login to use online banking!")
      roll()
    if already == True:
      print("Someone already has a account with that username!")
      roll()
  if task == "L"or task=="l":
    loginuser=input("Username: ")
    loginpass=input("Password: ")
    collection=db.authentication
    regex_query = { "Username" : {"$regex" : loginuser} }
    result = collection.find(regex_query)
    correctUser = False
    for doc in result:
        if doc["Username"]==loginuser:
          if doc["Password"]==loginpass:
            correctUser = True
    if correctUser == True:
      print("Correct login details!")
      time.sleep(0.2)
      os.system("clear")
      menu()
    else:
      print("Incorrect login details!")
      os.system('clear')
      roll()
roll()