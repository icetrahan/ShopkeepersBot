import os
import discord
from discord.ext import commands
import json
import asyncio
import random

intents=discord.Intents().all()
client = commands.Bot(command_prefix='!s ', intents=intents, help_command=None)

with open("./players.json") as j:
  players = json.load(j)
with open("./shops.json") as j:
  shops = json.load(j)
with open("./cards.json") as j:
  cards = json.load(j)
with open("./roles.json") as j:
  roles = json.load(j)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def setup(ctx):
  user = ctx.author
  found=False
  for k, v in players.items():
    if k == str(user.name)+"#"+str(user.discriminator):
      found = True
      break
    else:
      found = False
  if found:
    await ctx.send("You already setup an account")
  else:
    foundA=False
    for role in user.roles:
      for r in roles:
        print(str(role.id)+"  "+roles[r]["RoleId"])
        if str(role.id) == roles[r]["RoleId"]:
          aC=roles[r]["TC"]
          foundA=True
          break
        else:
          foundA=False
          continue
      if foundA:
        break
    if foundA:
      playerObj=({
        str(user.name)+"#"+str(user.discriminator):
        {
          "ActionCh": str(aC),
          "Gold": "30",
          "Battle": "Null",
          "Mana": "0",
          "Cards Drawn": "0",
          "Health": "100",
          "Shop" : "Null",
          "Inventory": []
        }
      })
      players.update(playerObj)
      with open("./players.json", "w") as j:
        json.dump(players, j, indent = 4)
      await ctx.send("Account Setup!")

    else:
      await ctx.send("You don't have a player role. You need to get an admin to give you a player role to participate.")





    #############################################################################################################################
    #############################################################################################################################
    #############################################################################################################################
    #############################################################################################################################




@client.command()
async def shop(ctx):
  shopList=[]
  userN=str(ctx.author.name)+"#"+str(ctx.author.discriminator)
  found=False
  for x in players:
    if x == userN:
      found = True
      break
    else:
      found = False
  if found==False:
    await ctx.send("You haven't setup an account yet or your account is missing")
  else:
  ## Defining what shops the user in whitelisted in
    for key, value in shops.items():
      for k, v in value.items():
        if k == "Whitelist":
          for users in v:
            if users == userN:
              shopList.append(key)
            else:
              continue
        else:
          continue
  ## Printing shop List
    List1 = []
    List1Print = []
    emojiList =       ['❎','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟','➡']
    
    if len(shopList) <= 10:
      for x in shopList:
        List1.append(x)
        List1Print.append(str(int(shopList.index(x))+1)+" "+x)
      msg = await ctx.send("Please react to the number that corresponds with the shop you would like to see \n"+"\n".join(List1Print)+"\nTo cancel select the X")
      for emoji in emojiList[0:(len(shopList)+1)]:
        await msg.add_reaction(emoji)
  
      ## Check for reaction
  
      def check(reaction, user):
        return user == ctx.author
      
      try:
        reaction, user = await client.wait_for("reaction_add" ,timeout=30.0, check=check)
  
      except asyncio.TimeoutError:
        await msg.delete()
      else:
        if reaction.emoji == '❎':
          await msg.delete()
          return
  
          ## Shop1
        elif reaction.emoji == '1️⃣':
          itemDict={}
          itemList=[]
          itemCount=0
          ##Too many values error
          for k,v in shops[shopList[0]]["Inventory"].items():
            itemCount+=1
            itemList.append(str(itemCount)+" "+k+" : "+v)
            itemDict[str(itemCount)]=k
          await msg.delete()
          if itemCount<=10:
            msg = await ctx.send('Which item would you like to purchase?\nTo exit select❎\n'+"\n".join(itemList))
            for emoji in emojiList[0:itemCount+1]:
              await msg.add_reaction(emoji)
            can=True
            ## Purchase Function
            def Purchase(itemNum):
              cost=int(shops[shopList[0]]["Inventory"][str(itemDict[itemNum])])
              if int(players[userN]["Gold"]) >= cost:
                newBalance=int(players[userN]["Gold"])-cost
                players[userN]["Gold"]=str(newBalance)
                players[userN]["Inventory"].append(itemDict[itemNum])
              else:
                can=False
                return can
  
            def check(reaction, user):
              return user == ctx.author
            
            try:
              reaction, user = await client.wait_for("reaction_add" ,timeout=30.0, check=check)
  
        
            except asyncio.TimeoutError:
              await msg.delete()
            else:
              if reaction.emoji == '❎':
                await msg.delete()
                return
              ##Item 1
              elif reaction.emoji == '1️⃣':
                if Purchase("1") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                  
              ##Item 2
              elif reaction.emoji == '2️⃣':
                Purchase("2")
                if can == False:
                  await ctx.send("You don't have enough gold")
                  exit
                if can == True:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
  
              ##Item 3
              elif reaction.emoji == '3️⃣':
                Purchase("3")
                if can == False:
                  await ctx.send("You don't have enough gold")
                  exit
                if can == True:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 4
              elif reaction.emoji == '4️⃣':
                Purchase("4")
                if can == False:
                  await ctx.send("You either don't have enough gold")
                  exit
                if can == True:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 5
              elif reaction.emoji == '5️⃣':
                Purchase("5")
                if can == False:
                  await ctx.send("You don't have enough gold")
                  exit
                if can == True:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 6
              elif reaction.emoji == '6️⃣':
                Purchase("6")
                if can == False:
                  await ctx.send("You don't have enough gold")
                  exit
                if can == True:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 7
              elif reaction.emoji == '7️⃣':
                Purchase("7")
                if can == False:
                  await ctx.send("You don't have enough gold")
                  exit
                if can == True:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 8
              elif reaction.emoji == '8️⃣':
                Purchase("8")
                if can == False:
                  await ctx.send("You don't have enough gold")
                  exit
                if can == True:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 9
              elif reaction.emoji == '9️⃣':
                Purchase("9")
                if can == False:
                  await ctx.send("You don't have enough gold")
                  exit
                if can == True:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 10
              elif reaction.emoji == '🔟':
                Purchase("10")
                if can == False:
                  await ctx.send("You don't have enough gold")
                  exit
                if can == True:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              else:
                print("ugh ohh")
                                
  
        ###############################################Shop2
        elif reaction.emoji == '2️⃣':
          itemDict={}
          itemList=[]
          itemCount=0
          ##Too many values error
          for k,v in shops[shopList[1]]["Inventory"].items():
            itemCount+=1
            itemList.append(str(itemCount)+" "+k+" : "+v)
            itemDict[str(itemCount)]=k
          await msg.delete()
          if itemCount<=10:
            msg = await ctx.send('Which item would you like to purchase?\nTo exit select❎\n'+"\n".join(itemList))
            for emoji in emojiList[0:itemCount+1]:
              await msg.add_reaction(emoji)
  
            ## Purchase Function
            can=True
            def Purchase(itemNum):
              cost=int(shops[shopList[1]]["Inventory"][str(itemDict[itemNum])])
              owner=str(shops[shopList[1]]["Owner"])
              if int(players[userN]["Gold"]) >= cost:
                bNewBalance=int(players[userN]["Gold"])-cost
                sNewBalance=int(players[owner]["Gold"])+cost
              ## Buyer
                players[userN]["Gold"]=str(bNewBalance)
                players[userN]["Inventory"].append(itemDict[itemNum])
              ##Seller
                players[owner]["Gold"]=str(sNewBalance)
                del shops[shopList[1]]["Inventory"][str(itemDict[itemNum])]
                
              else:
                can=False
                return can
  
            def check(reaction, user):
              return user == ctx.author
            
            try:
              reaction, user = await client.wait_for("reaction_add" ,timeout=30.0, check=check)
  
        
            except asyncio.TimeoutError:
              await msg.delete()
            else:
              if reaction.emoji == '❎':
                await msg.delete()
                return
                
              ##Item 1
              elif reaction.emoji == '1️⃣':
                if Purchase("1") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                  
              ##Item 2
              elif reaction.emoji == '2️⃣':
                if Purchase("2") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
  
              ##Item 3
              elif reaction.emoji == '3️⃣':
                if Purchase("3") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 4
              elif reaction.emoji == '4️⃣':
                if Purchase("4") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 5
              elif reaction.emoji == '5️⃣':
                if Purchase("5") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 6
              elif reaction.emoji == '6️⃣':
                if Purchase("6") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 7
              elif reaction.emoji == '7️⃣':
                if Purchase("7") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 8
              elif reaction.emoji == '8️⃣':
                if Purchase("8") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 9
              elif reaction.emoji == '9️⃣':
                if Purchase("9") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 10
              elif reaction.emoji == '🔟':
                if Purchase("10") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              else:
                print("ugh ohh")
          ###########################################Store 3
        elif reaction.emoji == '3️⃣':
          itemDict={}
          itemList=[]
          itemCount=0
          ##Too many values error
          for k,v in shops[shopList[2]]["Inventory"].items():
            itemCount+=1
            itemList.append(str(itemCount)+" "+k+" : "+v)
            itemDict[str(itemCount)]=k
          await msg.delete()
          if itemCount<=10:
            msg = await ctx.send('Which item would you like to purchase?\nTo exit select❎\n'+"\n".join(itemList))
            for emoji in emojiList[0:itemCount+1]:
              await msg.add_reaction(emoji)
  
            ## Purchase Function
            can=True
            def Purchase(itemNum):
              cost=int(shops[shopList[2]]["Inventory"][str(itemDict[itemNum])])
              owner=str(shops[shopList[2]]["Owner"])
              if int(players[userN]["Gold"]) >= cost:
                bNewBalance=int(players[userN]["Gold"])-cost
                sNewBalance=int(players[owner]["Gold"])+cost
              ## Buyer
                players[userN]["Gold"]=str(bNewBalance)
                players[userN]["Inventory"].append(itemDict[itemNum])
              ##Seller
                players[owner]["Gold"]=str(sNewBalance)
                del shops[shopList[1]]["Inventory"][str(itemDict[itemNum])]
                
              else:
                can=False
                return can
  
            def check(reaction, user):
              return user == ctx.author
            
            try:
              reaction, user = await client.wait_for("reaction_add" ,timeout=30.0, check=check)
  
        
            except asyncio.TimeoutError:
              await msg.delete()
            else:
              if reaction.emoji == '❎':
                await msg.delete()
                return
                
              ##Item 1
              elif reaction.emoji == '1️⃣':
                if Purchase("1") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                  
              ##Item 2
              elif reaction.emoji == '2️⃣':
                if Purchase("2") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
  
              ##Item 3
              elif reaction.emoji == '3️⃣':
                if Purchase("3") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 4
              elif reaction.emoji == '4️⃣':
                if Purchase("4") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 5
              elif reaction.emoji == '5️⃣':
                if Purchase("5") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 6
              elif reaction.emoji == '6️⃣':
                if Purchase("6") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 7
              elif reaction.emoji == '7️⃣':
                if Purchase("7") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 8
              elif reaction.emoji == '8️⃣':
                if Purchase("8") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 9
              elif reaction.emoji == '9️⃣':
                if Purchase("9") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 10
              elif reaction.emoji == '🔟':
                if Purchase("10") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              else:
                print("ugh ohh")
          ########################################Store 4
        elif reaction.emoji == '4️⃣':
          itemDict={}
          itemList=[]
          itemCount=0
          ##Too many values error
          for k,v in shops[shopList[3]]["Inventory"].items():
            itemCount+=1
            itemList.append(str(itemCount)+" "+k+" : "+v)
            itemDict[str(itemCount)]=k
          await msg.delete()
          if itemCount<=10:
            msg = await ctx.send('Which item would you like to purchase?\nTo exit select❎\n'+"\n".join(itemList))
            for emoji in emojiList[0:itemCount+1]:
              await msg.add_reaction(emoji)
  
            ## Purchase Function
            can=True
            def Purchase(itemNum):
              cost=int(shops[shopList[3]]["Inventory"][str(itemDict[itemNum])])
              owner=str(shops[shopList[3]]["Owner"])
              if int(players[userN]["Gold"]) >= cost:
                bNewBalance=int(players[userN]["Gold"])-cost
                sNewBalance=int(players[owner]["Gold"])+cost
              ## Buyer
                players[userN]["Gold"]=str(bNewBalance)
                players[userN]["Inventory"].append(itemDict[itemNum])
              ##Seller
                players[owner]["Gold"]=str(sNewBalance)
                del shops[shopList[1]]["Inventory"][str(itemDict[itemNum])]
                
              else:
                can=False
                return can
  
            def check(reaction, user):
              return user == ctx.author
            
            try:
              reaction, user = await client.wait_for("reaction_add" ,timeout=30.0, check=check)
  
        
            except asyncio.TimeoutError:
              await msg.delete()
            else:
              if reaction.emoji == '❎':
                await msg.delete()
                return
                
              ##Item 1
              elif reaction.emoji == '1️⃣':
                if Purchase("1") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                  
              ##Item 2
              elif reaction.emoji == '2️⃣':
                if Purchase("2") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
  
              ##Item 3
              elif reaction.emoji == '3️⃣':
                if Purchase("3") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 4
              elif reaction.emoji == '4️⃣':
                if Purchase("4") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 5
              elif reaction.emoji == '5️⃣':
                if Purchase("5") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 6
              elif reaction.emoji == '6️⃣':
                if Purchase("6") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 7
              elif reaction.emoji == '7️⃣':
                if Purchase("7") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 8
              elif reaction.emoji == '8️⃣':
                if Purchase("8") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 9
              elif reaction.emoji == '9️⃣':
                if Purchase("9") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 10
              elif reaction.emoji == '🔟':
                if Purchase("10") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              else:
                print("ugh ohh")
  
        ########################################Store 5
        elif reaction.emoji == '5️⃣':
          itemDict={}
          itemList=[]
          itemCount=0
          ##Too many values error
          for k,v in shops[shopList[4]]["Inventory"].items():
            itemCount+=1
            itemList.append(str(itemCount)+" "+k+" : "+v)
            itemDict[str(itemCount)]=k
          await msg.delete()
          if itemCount<=10:
            msg = await ctx.send('Which item would you like to purchase?\nTo exit select❎\n'+"\n".join(itemList))
            for emoji in emojiList[0:itemCount+1]:
              await msg.add_reaction(emoji)
  
            ## Purchase Function
            can=True
            def Purchase(itemNum):
              cost=int(shops[shopList[4]]["Inventory"][str(itemDict[itemNum])])
              owner=str(shops[shopList[4]]["Owner"])
              if int(players[userN]["Gold"]) >= cost:
                bNewBalance=int(players[userN]["Gold"])-cost
                sNewBalance=int(players[owner]["Gold"])+cost
              ## Buyer
                players[userN]["Gold"]=str(bNewBalance)
                players[userN]["Inventory"].append(itemDict[itemNum])
              ##Seller
                players[owner]["Gold"]=str(sNewBalance)
                del shops[shopList[1]]["Inventory"][str(itemDict[itemNum])]
                
              else:
                can=False
                return can
  
            def check(reaction, user):
              return user == ctx.author
            
            try:
              reaction, user = await client.wait_for("reaction_add" ,timeout=30.0, check=check)
  
        
            except asyncio.TimeoutError:
              await msg.delete()
            else:
              if reaction.emoji == '❎':
                await msg.delete()
                return
                
              ##Item 1
              elif reaction.emoji == '1️⃣':
                if Purchase("1") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                  
              ##Item 2
              elif reaction.emoji == '2️⃣':
                if Purchase("2") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
  
              ##Item 3
              elif reaction.emoji == '3️⃣':
                if Purchase("3") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 4
              elif reaction.emoji == '4️⃣':
                if Purchase("4") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 5
              elif reaction.emoji == '5️⃣':
                if Purchase("5") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 6
              elif reaction.emoji == '6️⃣':
                if Purchase("6") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 7
              elif reaction.emoji == '7️⃣':
                if Purchase("7") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 8
              elif reaction.emoji == '8️⃣':
                if Purchase("8") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 9
              elif reaction.emoji == '9️⃣':
                if Purchase("9") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 10
              elif reaction.emoji == '🔟':
                if Purchase("10") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              else:
                print("ugh ohh")
  
        ########################################Store 6
        elif reaction.emoji == '6️⃣':
          itemDict={}
          itemList=[]
          itemCount=0
          ##Too many values error
          for k,v in shops[shopList[5]]["Inventory"].items():
            itemCount+=1
            itemList.append(str(itemCount)+" "+k+" : "+v)
            itemDict[str(itemCount)]=k
          await msg.delete()
          if itemCount<=10:
            msg = await ctx.send('Which item would you like to purchase?\nTo exit select❎\n'+"\n".join(itemList))
            for emoji in emojiList[0:itemCount+1]:
              await msg.add_reaction(emoji)
  
            ## Purchase Function
            can=True
            def Purchase(itemNum):
              cost=int(shops[shopList[5]]["Inventory"][str(itemDict[itemNum])])
              owner=str(shops[shopList[5]]["Owner"])
              if int(players[userN]["Gold"]) >= cost:
                bNewBalance=int(players[userN]["Gold"])-cost
                sNewBalance=int(players[owner]["Gold"])+cost
              ## Buyer
                players[userN]["Gold"]=str(bNewBalance)
                players[userN]["Inventory"].append(itemDict[itemNum])
              ##Seller
                players[owner]["Gold"]=str(sNewBalance)
                del shops[shopList[1]]["Inventory"][str(itemDict[itemNum])]
                
              else:
                can=False
                return can
  
            def check(reaction, user):
              return user == ctx.author
            
            try:
              reaction, user = await client.wait_for("reaction_add" ,timeout=30.0, check=check)
  
        
            except asyncio.TimeoutError:
              await msg.delete()
            else:
              if reaction.emoji == '❎':
                await msg.delete()
                return
                
              ##Item 1
              elif reaction.emoji == '1️⃣':
                if Purchase("1") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                  
              ##Item 2
              elif reaction.emoji == '2️⃣':
                if Purchase("2") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
  
              ##Item 3
              elif reaction.emoji == '3️⃣':
                if Purchase("3") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 4
              elif reaction.emoji == '4️⃣':
                if Purchase("4") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 5
              elif reaction.emoji == '5️⃣':
                if Purchase("5") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 6
              elif reaction.emoji == '6️⃣':
                if Purchase("6") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 7
              elif reaction.emoji == '7️⃣':
                if Purchase("7") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 8
              elif reaction.emoji == '8️⃣':
                if Purchase("8") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 9
              elif reaction.emoji == '9️⃣':
                if Purchase("9") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 10
              elif reaction.emoji == '🔟':
                if Purchase("10") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              else:
                print("ugh ohh")
  
        ########################################Store 7
        elif reaction.emoji == '7️⃣':
          itemDict={}
          itemList=[]
          itemCount=0
          ##Too many values error
          for k,v in shops[shopList[6]]["Inventory"].items():
            itemCount+=1
            itemList.append(str(itemCount)+" "+k+" : "+v)
            itemDict[str(itemCount)]=k
          await msg.delete()
          if itemCount<=10:
            msg = await ctx.send('Which item would you like to purchase?\nTo exit select❎\n'+"\n".join(itemList))
            for emoji in emojiList[0:itemCount+1]:
              await msg.add_reaction(emoji)
  
            ## Purchase Function
            can=True
            def Purchase(itemNum):
              cost=int(shops[shopList[6]]["Inventory"][str(itemDict[itemNum])])
              owner=str(shops[shopList[6]]["Owner"])
              if int(players[userN]["Gold"]) >= cost:
                bNewBalance=int(players[userN]["Gold"])-cost
                sNewBalance=int(players[owner]["Gold"])+cost
              ## Buyer
                players[userN]["Gold"]=str(bNewBalance)
                players[userN]["Inventory"].append(itemDict[itemNum])
              ##Seller
                players[owner]["Gold"]=str(sNewBalance)
                del shops[shopList[1]]["Inventory"][str(itemDict[itemNum])]
                
              else:
                can=False
                return can
  
            def check(reaction, user):
              return user == ctx.author
            
            try:
              reaction, user = await client.wait_for("reaction_add" ,timeout=30.0, check=check)
  
        
            except asyncio.TimeoutError:
              await msg.delete()
            else:
              if reaction.emoji == '❎':
                await msg.delete()
                return
                
              ##Item 1
              elif reaction.emoji == '1️⃣':
                if Purchase("1") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                  
              ##Item 2
              elif reaction.emoji == '2️⃣':
                if Purchase("2") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
  
              ##Item 3
              elif reaction.emoji == '3️⃣':
                if Purchase("3") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 4
              elif reaction.emoji == '4️⃣':
                if Purchase("4") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 5
              elif reaction.emoji == '5️⃣':
                if Purchase("5") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 6
              elif reaction.emoji == '6️⃣':
                if Purchase("6") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 7
              elif reaction.emoji == '7️⃣':
                if Purchase("7") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 8
              elif reaction.emoji == '8️⃣':
                if Purchase("8") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 9
              elif reaction.emoji == '9️⃣':
                if Purchase("9") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 10
              elif reaction.emoji == '🔟':
                if Purchase("10") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              else:
                print("ugh ohh")
  
        ########################################Store 8
        elif reaction.emoji == '8️⃣':
          itemDict={}
          itemList=[]
          itemCount=0
          ##Too many values error
          for k,v in shops[shopList[7]]["Inventory"].items():
            itemCount+=1
            itemList.append(str(itemCount)+" "+k+" : "+v)
            itemDict[str(itemCount)]=k
          await msg.delete()
          if itemCount<=10:
            msg = await ctx.send('Which item would you like to purchase?\nTo exit select❎\n'+"\n".join(itemList))
            for emoji in emojiList[0:itemCount+1]:
              await msg.add_reaction(emoji)
  
            ## Purchase Function
            can=True
            def Purchase(itemNum):
              cost=int(shops[shopList[7]]["Inventory"][str(itemDict[itemNum])])
              owner=str(shops[shopList[7]]["Owner"])
              if int(players[userN]["Gold"]) >= cost:
                bNewBalance=int(players[userN]["Gold"])-cost
                sNewBalance=int(players[owner]["Gold"])+cost
              ## Buyer
                players[userN]["Gold"]=str(bNewBalance)
                players[userN]["Inventory"].append(itemDict[itemNum])
              ##Seller
                players[owner]["Gold"]=str(sNewBalance)
                del shops[shopList[1]]["Inventory"][str(itemDict[itemNum])]
                
              else:
                can=False
                return can
  
            def check(reaction, user):
              return user == ctx.author
            
            try:
              reaction, user = await client.wait_for("reaction_add" ,timeout=30.0, check=check)
  
        
            except asyncio.TimeoutError:
              await msg.delete()
            else:
              if reaction.emoji == '❎':
                await msg.delete()
                return
                
              ##Item 1
              elif reaction.emoji == '1️⃣':
                if Purchase("1") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                  
              ##Item 2
              elif reaction.emoji == '2️⃣':
                if Purchase("2") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
  
              ##Item 3
              elif reaction.emoji == '3️⃣':
                if Purchase("3") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 4
              elif reaction.emoji == '4️⃣':
                if Purchase("4") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 5
              elif reaction.emoji == '5️⃣':
                if Purchase("5") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 6
              elif reaction.emoji == '6️⃣':
                if Purchase("6") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 7
              elif reaction.emoji == '7️⃣':
                if Purchase("7") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 8
              elif reaction.emoji == '8️⃣':
                if Purchase("8") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 9
              elif reaction.emoji == '9️⃣':
                if Purchase("9") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 10
              elif reaction.emoji == '🔟':
                if Purchase("10") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              else:
                print("ugh ohh")
  
        ########################################Store 9
        elif reaction.emoji == '9️⃣':
          itemDict={}
          itemList=[]
          itemCount=0
          ##Too many values error
          for k,v in shops[shopList[8]]["Inventory"].items():
            itemCount+=1
            itemList.append(str(itemCount)+" "+k+" : "+v)
            itemDict[str(itemCount)]=k
          await msg.delete()
          if itemCount<=10:
            msg = await ctx.send('Which item would you like to purchase?\nTo exit select❎\n'+"\n".join(itemList))
            for emoji in emojiList[0:itemCount+1]:
              await msg.add_reaction(emoji)
  
            ## Purchase Function
            can=True
            def Purchase(itemNum):
              cost=int(shops[shopList[8]]["Inventory"][str(itemDict[itemNum])])
              owner=str(shops[shopList[8]]["Owner"])
              if int(players[userN]["Gold"]) >= cost:
                bNewBalance=int(players[userN]["Gold"])-cost
                sNewBalance=int(players[owner]["Gold"])+cost
              ## Buyer
                players[userN]["Gold"]=str(bNewBalance)
                players[userN]["Inventory"].append(itemDict[itemNum])
              ##Seller
                players[owner]["Gold"]=str(sNewBalance)
                del shops[shopList[1]]["Inventory"][str(itemDict[itemNum])]
                
              else:
                can=False
                return can
  
            def check(reaction, user):
              return user == ctx.author
            
            try:
              reaction, user = await client.wait_for("reaction_add" ,timeout=30.0, check=check)
  
        
            except asyncio.TimeoutError:
              await msg.delete()
            else:
              if reaction.emoji == '❎':
                await msg.delete()
                return
                
              ##Item 1
              elif reaction.emoji == '1️⃣':
                if Purchase("1") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                  
              ##Item 2
              elif reaction.emoji == '2️⃣':
                if Purchase("2") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
  
              ##Item 3
              elif reaction.emoji == '3️⃣':
                if Purchase("3") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 4
              elif reaction.emoji == '4️⃣':
                if Purchase("4") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 5
              elif reaction.emoji == '5️⃣':
                if Purchase("5") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 6
              elif reaction.emoji == '6️⃣':
                if Purchase("6") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 7
              elif reaction.emoji == '7️⃣':
                if Purchase("7") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 8
              elif reaction.emoji == '8️⃣':
                if Purchase("8") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 9
              elif reaction.emoji == '9️⃣':
                if Purchase("9") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 10
              elif reaction.emoji == '🔟':
                if Purchase("10") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              else:
                print("ugh ohh")
  
        ########################################Store 10
        elif reaction.emoji == '🔟':
          itemDict={}
          itemList=[]
          itemCount=0
          ##Too many values error
          for k,v in shops[shopList[9]]["Inventory"].items():
            itemCount+=1
            itemList.append(str(itemCount)+" "+k+" : "+v)
            itemDict[str(itemCount)]=k
          await msg.delete()
          if itemCount<=10:
            msg = await ctx.send('Which item would you like to purchase?\nTo exit select❎\n'+"\n".join(itemList))
            for emoji in emojiList[0:itemCount+1]:
              await msg.add_reaction(emoji)
  
           ## Purchase Function
            can=True
            def Purchase(itemNum):
              cost=int(shops[shopList[9]]["Inventory"][str(itemDict[itemNum])])
              owner=str(shops[shopList[9]]["Owner"])
              if int(players[userN]["Gold"]) >= cost:
                bNewBalance=int(players[userN]["Gold"])-cost
                sNewBalance=int(players[owner]["Gold"])+cost
              ## Buyer
                players[userN]["Gold"]=str(bNewBalance)
                players[userN]["Inventory"].append(itemDict[itemNum])
              ##Seller
                players[owner]["Gold"]=str(sNewBalance)
                del shops[shopList[1]]["Inventory"][str(itemDict[itemNum])]
                
              else:
                can=False
                return can
  
            def check(reaction, user):
              return user == ctx.author
            
            try:
              reaction, user = await client.wait_for("reaction_add" ,timeout=30.0, check=check)
  
        
            except asyncio.TimeoutError:
              await msg.delete()
            else:
              if reaction.emoji == '❎':
                await msg.delete()
                return
                
              ##Item 1
              elif reaction.emoji == '1️⃣':
                if Purchase("1") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                  
              ##Item 2
              elif reaction.emoji == '2️⃣':
                if Purchase("2") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
  
              ##Item 3
              elif reaction.emoji == '3️⃣':
                if Purchase("3") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 4
              elif reaction.emoji == '4️⃣':
                if Purchase("4") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 5
              elif reaction.emoji == '5️⃣':
                if Purchase("5") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 6
              elif reaction.emoji == '6️⃣':
                if Purchase("6") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 7
              elif reaction.emoji == '7️⃣':
                if Purchase("7") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 8
              elif reaction.emoji == '8️⃣':
                if Purchase("8") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 9
              elif reaction.emoji == '9️⃣':
                if Purchase("9") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              ##Item 10
              elif reaction.emoji == '🔟':
                if Purchase("10") == False:
                  await ctx.send("You don't have enough gold")
                  exit
                else:
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                  with open("./shops.json", "w") as s:
                    json.dump(shops, s, indent = 4)
                  await ctx.send("Your new balance is: "+players[userN]["Gold"])
                
              else:
                print("ugh ohh")
                
        else:
          print("ugh oh")
      
      return
  
        
    else:
      await ctx.send("Please Contact Owner. Bot needs to be updated")
  
    
  
  
      #############################################################################################################################
      #############################################################################################################################
      #############################################################################################################################
      #############################################################################################################################


@client.command()
async def setupshop(ctx):
  user = ctx.author
  found=False
  for k, v in players.items():
    if k == str(user.name)+"#"+str(user.discriminator):
      found = True
      break
    else:
      found = False
  if found == False:
    await ctx.send("You need to setup and account first. \nUse !s setup")
  else:
    for key, value in shops.items():
      if shops[str(key)]["Owner"]==str(user.name)+"#"+str(user.discriminator):
        found = True
        break
      else:
        found = False
    if found == True:
      await ctx.send("You already setup a shop named: "+str(key))
    else:
      msg= await ctx.send("What would you like to name your shop?\n(Please type your shop name exactly as you want it to appear)")
      def check(m):
        return m.channel == ctx.channel and m.author == ctx.author
      
      try:
        re= await client.wait_for("message",timeout=30.0,check=check)
  
      except asyncio.TimeoutError:
        await msg.delete()
        await ctx.send("Sorry you took too long.")
        
      else: 
        playerShop=({
          str(re.content):{
            "Owner":str(user.name)+"#"+str(user.discriminator),
            "Whitelist":[],
            "Inventory": {}
          }
        })
        shops.update(playerShop)
        players[str(user.name)+"#"+str(user.discriminator)]["Shop"]=str(re.content)
        with open("./shops.json", "w") as j:
          json.dump(shops, j, indent = 4)
        with open("./players.json", "w") as j:
          json.dump(players, j, indent = 4)
        await ctx.send("Shop Setup! Your shop name is:"+str(re.content)+"\n     -To add items to your shop use !s shopadd\n     -To allow players to view your shop use !s shoplist")

####################    ADD    TO     SHOP #############

@client.command()
async def shopadd(ctx):
  user = ctx.author
  userName = str(user.name)+"#"+str(user.discriminator)
  userShop= str(players[userName]["Shop"])
  invList= []
  shopList=[]
  found=False
  for k,v in shops[userShop]["Inventory"].items():
    shopList.append(k)
    
  for item in players[userName]["Inventory"]:
    for shopItem in shopList:
      if item == shopItem:
        found=True
        break
      else:
        found=False
      if found:
        pass
      else:
        invList.append(item)
  invList= list(dict.fromkeys(invList))
  if len(invList) > 0:
    msg= await ctx.send("What items would you like to add to your shop\n"+"\n".join(invList)+"\n\nPlease be sure to type the item EXACTLY as it appears above.")
    
    def check(m):
      return m.channel == ctx.channel and m.author == ctx.author
    
    try:
      re= await client.wait_for("message",timeout=30.0,check=check)
  
    except asyncio.TimeoutError:
      await msg.delete()
      await ctx.send("Sorry you took too long.")
      
    else:
      found = False
      addedItem = str(re.content)
      for listItem in invList:
        if addedItem == listItem:
          found = True
          break
        else:
          found = False
      if found:
        cost= await ctx.send("How much gold do you want to sell the item for? Only enter an answer in a whole number form.\n Ex: 10")
    
        def check(m):
          return m.channel == ctx.channel and m.author == ctx.author
        
        try:
          re= await client.wait_for("message",timeout=30.0,check=check)
      
        except asyncio.TimeoutError:
          await cost.delete()
          await ctx.send("Sorry you took too long.")
          
        else:
          if int(re.content) > 0:
            players[userName]["Inventory"].remove(addedItem)
            shops[userShop]["Inventory"][addedItem]=str(re.content)
            with open("./shops.json", "w") as j:
              json.dump(shops, j, indent = 4)
            with open("./players.json", "w") as j:
              json.dump(players, j, indent = 4)
            await ctx.send(addedItem+" has been added to your shop for "+re.content+" gold.")
          else:
            await ctx.send("You did not enter a valid number. Please try again")
      else:
        await ctx.send("You did not enter a valid item. Please be sure to type the item exactly as it appears.")
  else:
    await ctx.send("You don't have any items in your inventory that can be added to your shop.\n\nPlease note:\nYou cannot add duplicates of an item to your shop.")


####################    REMOVE    FROM     SHOP #############

@client.command()
async def shopremove(ctx):
  user = ctx.author
  userName = str(user.name)+"#"+str(user.discriminator)
  userShop= str(players[userName]["Shop"])
  shopList= []
  for key, value in shops[userShop]["Inventory"].items():
    shopList.append(key)
    
  msg= await ctx.send("What items would you like to remove from your shop\n"+"\n".join(shopList))
  
  def check(m):
    return m.channel == ctx.channel and m.author == ctx.author
  
  try:
    re= await client.wait_for("message",timeout=30.0,check=check)

  except asyncio.TimeoutError:
    await msg.delete()
    await ctx.send("Sorry you took too long.")
    
  else:
    found = False
    addedItem = str(re.content)
    for listItem in shopList:
      if addedItem == listItem:
        found = True
        break
      else:
        found = False
    if found:
      players[userName]["Inventory"].append(addedItem)
      del shops[userShop]["Inventory"][addedItem]
      with open("./shops.json", "w") as j:
        json.dump(shops, j, indent = 4)
      with open("./players.json", "w") as j:
        json.dump(players, j, indent = 4)
      await ctx.send(addedItem+" has been moved from your shop and added to your inventory")
    else:
      await ctx.send("You did not enter a valid item. Please be sure to type the item exactly as it appears.")

################### CHECK     INVENTORY    ###############
@client.command()
async def checkprofile(ctx):
  userN=str(ctx.author.name)+"#"+str(ctx.author.discriminator)
  userShop= str(players[userN]["Shop"])
  balance = str(players[userN]["Gold"])
  inventory = players[userN]["Inventory"].copy()
  await ctx.send("Shop: "+userShop+"\nBalance: "+balance+" gold"+"\nInventory:\n"+"\n     ".join(inventory))
  
###################   CHECK      SHOP      ###############
@client.command()
async def checkshop(ctx):
  userN=str(ctx.author.name)+"#"+str(ctx.author.discriminator)
  userShop= str(players[userN]["Shop"])
  inventory = shops[userShop]["Inventory"].copy()
  await ctx.send("Shop: "+userShop+"\nInventory:\n     Item: "+"\n     Item: ".join("   Price:".join((key,val)) for (key,val) in inventory.items()))
###################    SHOP    WHITELIST   ###############
  
@client.command()
async def shoplist(ctx):
  userName=str(ctx.author.name)+"#"+str(ctx.author.discriminator)
  userShop= str(players[userName]["Shop"])
  whiteList= []
  for aUser in shops[userShop]["Whitelist"]:
    whiteList.append(aUser)
  msg = await ctx.send("Here's a list of all the users on your whiteList:\n"+"\n".join(whiteList)+"\n \nTo add users to your list say: add\nTo remove users from your list say: remove")
  def check(m):
    return m.channel == ctx.channel and m.author == ctx.author
  
  try:
    re= await client.wait_for("message",timeout=30.0,check=check)

  except asyncio.TimeoutError:
    await msg.delete()
    await ctx.send("Sorry you took too long.")
    
  else:
    if str(re.content) == "add":
      msg = await ctx.send("Enter the name of the user you want to add.\n\n Example: ThisPlayer#0000\n\nIf you do not type the players name in the same format that player will not have access to your shop.")
      def check(m):
        return m.channel == ctx.channel and m.author == ctx.author
      
      try:
        reply= await client.wait_for("message",timeout=30.0,check=check)
    
      except asyncio.TimeoutError:
        await msg.delete()
        await ctx.send("Sorry you took too long.")
        
      else:
        shops[userShop]["Whitelist"].append(reply.content)
        with open("./shops.json", "w") as j:
          json.dump(shops, j, indent = 4)
        await msg.delete()
        await ctx.send(reply.content+" has been successfully added to your shop whitelist")
        await reply.delete()
        await re.delete()

        
    elif str(re.content) == "remove":
      msg = await ctx.send("Enter the name of the user you want to remove.\n\n Example: ThisPlayer#0000\n\nIf you do not type the players name in the same format that player may still have access to your shop.")
      def check(m):
        return m.channel == ctx.channel and m.author == ctx.author
      
      try:
        reply= await client.wait_for("message",timeout=30.0,check=check)
    
      except asyncio.TimeoutError:
        await msg.delete()
        await ctx.send("Sorry you took too long.")
        
      else:
        shops[userShop]["Whitelist"].remove(reply.content)
        with open("./shops.json", "w") as j:
          json.dump(shops, j, indent = 4)
        await msg.delete()
        await ctx.send(reply.content+" has been successfully remove from your shop whitelist")
        await reply.delete()
        await re.delete()
      
    else:
      await ctx.send("You didn't type a valid option. Please try again")
  

@client.command()
async def balance(ctx):
  userN=str(ctx.author.name)+"#"+str(ctx.author.discriminator)
  await ctx.send("Your balance is: "+players[userN]["Gold"])


##battle setup

  ##TODO Check if enemy is in a battle
@client.command()
async def startbattle(ctx, role: discord.Role):
  memberCount=0

  ##Filter out observer role
  if role.id == 962756897843335218:
    print("You can't battle an observer. Please use a player role.")

  else:
    passed=False
    for m in role.members:
      memberCount+=1
    if memberCount >=2:
      await ctx.send(f"There seems to be multiple players set for {role}. Please contact an admin.")
      passed=False
    else: 
      uE = m
      userEnemy=str(m.name)+"#"+str(m.discriminator)
      
      passed=True
    if passed:
      user = ctx.author
      userName=str(ctx.author.name)+"#"+str(ctx.author.discriminator)
      emojiList = ["✅","❌"]
      cBattle=players[userName]["Battle"]
      eBattle=players[userEnemy]["Battle"]
      if cBattle == "Null":
        if eBattle =="Null":
    
          msg = await ctx.send(f"You're clear to start a battle! Please confirm that you would like to start a battle with {userEnemy}")
      
          for emoji in emojiList:
            await msg.add_reaction(emoji)
          
          def check(reaction, user):
            return user == ctx.author
          
          try:
            reaction, user = await client.wait_for("reaction_add" ,timeout=30.0, check=check)
        
          except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send("Sorry you took too long.")
            
          else:
            if reaction.emoji == '✅':
              await msg.delete()
              enemy=userEnemy
              try:
                players[userName]["Battle"]=enemy
                players[enemy]["Battle"]=userName
              except KeyError:
                await ctx.send("The member you selected has not setup an account yet.")
              else:
                enemyCh= client.get_channel(int(players[enemy]["ActionCh"]))
  
                ##Setup Decks
                for card in players[userName]["Inventory"]:
                  players[userName]["Deck"].append(card)
                random.shuffle(players[userName]["Deck"])
  
                print(players[userName]["Deck"])
                
                for card in players[enemy]["Inventory"]:
                  players[enemy]["Deck"].append(card)
                random.shuffle(players[enemy]["Deck"])
  
                ##StartHealth
                players[userName]["Health"]="100"
                players[enemy]["Health"]="100"
  
                
                
                with open("./players.json", "w") as j:
                  json.dump(players, j, indent = 4)

                await enemyCh.send(f"{userName} has started a battle with you. Use the startturn command to make your first move")
                await ctx.send(f"You have started a battle with {userEnemy}. Use the startturn command to make your first move")
                return
        
            elif reaction.emoji == "❌":
              await msg.delete()
              await ctx.send(f"You have selected not to start a battle with {userEnemy}.")
              return
  
            else:
              await ctx.send("You did not select one of the emoji we provided. Please try again.")

        else: await ctx.send(f"{userEnemy} is already in a battle, either wait until their battle is over or choose someone else to battle.")
          
      else:
        await ctx.send(f"You are NOT clear to start a battle with {userEnemy}. Please end your currently battle with {cBattle} or ask an admin for help.")
  

@client.command()
async def startturn(ctx):
  userName=str(ctx.author.name)+"#"+str(ctx.author.discriminator)
  if players[userName]["Battle"]=="Null":
    await ctx.send("You are not currently in a battle. Use the startbattle command to start one.")
  else:
    if players[userName]["TurnEnded"]=="True":
      await ctx.send("Please wait for you opponent to end their turn before starting a new turn.")
    else:
      if players[userName]["StartedTurn"]=="True":
        await ctx.send("You already started your turn. Use the playcard command to play your cards.")
      else:
        if len(players[userName]["Deck"])>0:
          hand = players[userName]["Deck"][:5]
        else:
          for card in players[userName]["Inventory"]:
            players[userName]["Deck"].append(card)
          random.shuffle(players[userName]["Deck"])
          
        players[userName]["StartedTurn"]="True"
        players[userName]["Mana"]="10"
        players[userName]["Hand"]=hand
        for card in hand:
          players[userName]["Deck"].remove(card)
        await ctx.send("Turn Started")
        with open("./players.json", "w") as j:
          json.dump(players, j, indent = 4)
      
  

@client.command()
async def playcard(ctx):
  userName=str(ctx.author.name)+"#"+str(ctx.author.discriminator)
  if players[userName]["Battle"]=="Null":
    await ctx.send("You are not currently in a battle. Use the startbattle command to start one.")
  else:
    if players[userName]["TurnEnded"]=="True":
      await ctx.send("You've already ended you turn. Please wait for you opponent to end their turn.")
    else:
      if players[userName]["StartedTurn"]=="False":
        await ctx.send("You need to start your turn first. Use the startturn command")
      else:
        if len(players[userName]["Hand"])==0:
          await ctx.send("You do not have any remaining cards in your hand. Use the endturn command to end your turn.")
        else:
          hand = players[userName]["Hand"]
          printList=[]
          emojiList = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣']
          count=0
          for card in hand:
            count+=1
            printList.append(str(count)+". "+str(card)+"\n     ManaCost: "+str(cards[card]["ManaCost"])+"\n     Damage: "+str(cards[card]["Damage"])+"\n     Healing: "+str(cards[card]["Healing"])+"\n     Description: "+str(cards[card]["Desc"]))
          msg =await ctx.send("You have "+players[userName]["Mana"]+" mana.\n"+"What card would you like to play?\n"+"\n\n".join(printList)+"\n\n\nYou have 60 seconds. To end your turn use the endturn command.")
          for emoji in emojiList[:count]:
            await msg.add_reaction(emoji)
          
          def check(reaction, user):
            return user == ctx.author
          
          try:
            reaction, user = await client.wait_for("reaction_add" ,timeout=60.0, check=check)
        
          except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send("Sorry you took too long.")
            
          else:
            mana=int(players[userName]["Mana"])
            if reaction.emoji == '1️⃣':
              if count>=1:
                manaCost=int(cards[hand[0]]["ManaCost"])
                rMana=mana-manaCost
                if rMana >= 0:
                  players[userName]["TurnPile"].append(hand[0])
                  players[userName]["Mana"]=str(rMana)
                  await ctx.send(hand[0]+" has been added to your play que.")
                  players[userName]["Hand"].remove(hand[0])
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                else:
                  await ctx.send("You do not have enough mana to play this card.")
                  await msg.delete()
              else:
                await ctx.send("That card is no longer in your hand.")
                
            elif reaction.emoji == '2️⃣':
              if count>=2:
                manaCost=int(cards[hand[1]]["ManaCost"])
                rMana=mana-manaCost
                if rMana >= 0:
                  players[userName]["TurnPile"].append(hand[1])
                  players[userName]["Mana"]=str(rMana)
                  await ctx.send(hand[1]+" has been added to your play que.")
                  players[userName]["Hand"].remove(hand[1])
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                else:
                  await ctx.send("You do not have enough mana to play this card.")
                  await msg.delete()
              else:
                await ctx.send("That card is no longer in your hand.")
  
            elif reaction.emoji == '3️⃣':
              if count>=3:
                manaCost=int(cards[hand[2]]["ManaCost"])
                rMana=mana-manaCost
                if rMana >= 0:
                  players[userName]["TurnPile"].append(hand[2])
                  players[userName]["Mana"]=str(rMana)
                  await ctx.send(hand[2]+" has been added to your play que.")
                  players[userName]["Hand"].remove(hand[2])
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                else:
                  await ctx.send("You do not have enough mana to play this card.")
                  await msg.delete()
              else:
                await ctx.send("That card is no longer in your hand.")
  
            elif reaction.emoji == '4️⃣':
              if count>=4:
                manaCost=int(cards[hand[3]]["ManaCost"])
                rMana=mana-manaCost
                if rMana >= 0:
                  players[userName]["TurnPile"].append(hand[3])
                  players[userName]["Mana"]=str(rMana)
                  await ctx.send(hand[3]+" has been added to your play que.")
                  players[userName]["Hand"].remove(hand[3])
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                else:
                  await ctx.send("You do not have enough mana to play this card.")
                  await msg.delete()
              else:
                await ctx.send("That card is no longer in your hand.")
  
            elif reaction.emoji == '5️⃣':
              if count>=5:
                manaCost=int(cards[hand[4]]["ManaCost"])
                rMana=mana-manaCost
                if rMana >= 0:
                  players[userName]["TurnPile"].append(hand[4])
                  players[userName]["Mana"]=str(rMana)
                  await ctx.send(hand[4]+" has been added to your play que.")
                  players[userName]["Hand"].remove(hand[4])
                  await msg.delete()
                  with open("./players.json", "w") as j:
                    json.dump(players, j, indent = 4)
                else:
                  await ctx.send("You do not have enough mana to play this card.")
                  await msg.delete()
              else:
                await ctx.send("That card is no longer in your hand.")
  
            else:
              await ctx.send("You did not select a valid option. Please try again.")
              await msg.delete()
            
        

@client.command()
async def endturn(ctx):
  userName=str(ctx.author.name)+"#"+str(ctx.author.discriminator)
  if players[userName]["Battle"]=="Null":
    await ctx.send("You are not currently in a battle. Use the startbattle command to start one.")
  else:
    if players[userName]["TurnEnded"]=="True":
      await ctx.send("You've already ended you turn. Please wait for you opponent to end their turn.")
    else:
      enemy=players[userName]["Battle"]
      if players[enemy]["TurnEnded"]=="True":
        ##Battle actions
        players[userName]["Hand"].clear()
        p1Damage=0
        p1Healing=0
        p2Damage=0
        p2Healing=0
        fogPlayed=False
        
        ##User

        ##TODO not removing last card in TurnPile
        print(players[userName]["TurnPile"])
        while len(players[userName]["TurnPile"])>0 and len(players[userName]["TurnPile"])>0:
          for card in players[userName]["TurnPile"]:
  
            print("card: "+card+"user: "+ userName)
            
            papercutsPlayed=False
            dmgMult=int(players[userName]["DamageMult"])
            players[userName]["DiscardPile"].append(card)
            players[userName]["TurnPile"].remove(card)
            p1Damage+=int(cards[card]["Damage"])
            p1Healing+=int(cards[card]["Healing"])
  
            if card == "Fog":
              fogPlayed=True
              continue
            elif card == "Bulk Up":
              dmgMult+=0.1
              continue
            elif card == "Papercuts":
              papercutsPlayed=True
              continue

          for card in players[enemy]["TurnPile"]:
  
            print("card: "+card+"user: "+ enemy)
            
            papercutsPlayed=False
            dmgMult=int(players[enemy]["DamageMult"])
            players[enemy]["DiscardPile"].append(card)
            players[enemy]["TurnPile"].remove(card)
            p2Damage+=int(cards[card]["Damage"])
            p2Healing+=int(cards[card]["Healing"])
  
            if card == "Fog":
              fogPlayed=True
              continue
            elif card == "Bulk Up":
              dmgMult+=0.1
              continue
            elif card == "Papercuts":
              papercutsPlayed=True
              continue

        players[userName]["DamageMult"]=str(dmgMult)
        p1Damage=round(p1Damage*dmgMult)
        
        players[enemy]["DamageMult"]=str(dmgMult)
        p2Damage=round(p2Damage*dmgMult)

        await asyncio.sleep(3)

        ##2 damage, 3x
        ##TODO add attack count to all cards AND fix bulk up

        ##Calculate

        if fogPlayed:
          p1Damage=0
          p2Damage=0
          
        p1Health=int(players[userName]["Health"])
        p2Health=int(players[enemy]["Health"])

        p1Health=p1Health-p2Damage+p1Healing
        p2Health=p2Health-p1Damage+p2Healing

  ##adding to datafile
        ##Health
        players[userName]["Health"]=str(p1Health)
        players[enemy]["Health"]=str(p2Health)

        ##Turn
        players[userName]["TurnEnded"]="False"
        players[enemy]["TurnEnded"]="False"
        players[userName]["StartedTurn"]="False"
        players[enemy]["StartedTurn"]="False"

        if p1Health <=0 and p2Health <=0:
          await ctx.send("This battle has resulted in a draw. Both players fell to or below zero health.")
          enemyTC=client.get_channel(int(players[enemy]["ActionCh"]))
          await enemyTC.send("This battle has resulted in a draw. Both players fell to or below zero health.")

          ##P1
          players[userName]["Battle"]="Null"
          players[userName]["Deck"].clear()
          players[userName]["DiscardPile"].clear()
          players[userName]["TurnPile"].clear()
          players[userName]["DamageMult"]="1"
          players[userName]["StartedTurn"]="False"

          ##P2
          players[enemy]["Battle"]="Null"
          players[enemy]["Deck"].clear()
          players[enemy]["DiscardPile"].clear()
          players[enemy]["TurnPile"].clear()
          players[enemy]["DamageMult"]="1"
          players[enemy]["StartedTurn"]="False"

        elif p1Health <=0:

          ##Awarded Gold
          awardPerc=round(p2Health*0.15)
          loserGold=int(players[userName]["Gold"])
          goldAward=loserGold*(awardPerc/100)
          if goldAward < 1:
            goldAward =1

          p1Gold= int(players[userName]["Gold"])
          p2Gold= int(players[enemy]["Gold"])

          await ctx.send(f"You fell to or below 0 health so you have lost this battle. Better luck next time. You have lost {goldAward} gold from this battle.")
          enemyTC=client.get_channel(int(players[enemy]["ActionCh"]))
          await enemyTC.send(f"You have won this battle! Your opponent fell to or below 0 health. Good job! You have earned {goldAward} gold from this battle")
            
          ##P1
          players[userName]["Battle"]="Null"
          players[userName]["Deck"].clear()
          players[userName]["DiscardPile"].clear()
          players[userName]["TurnPile"].clear()
          players[userName]["DamageMult"]="1"
          players[userName]["StartedTurn"]="False"
          players[userName]["Gold"]=str(p1Gold-loserGold)

          ##P2
          players[enemy]["Battle"]="Null"
          players[enemy]["Deck"].clear()
          players[enemy]["DiscardPile"].clear()
          players[enemy]["TurnPile"].clear()
          players[enemy]["DamageMult"]="1"
          players[enemy]["StartedTurn"]="False"
          players[enemy]["Gold"]=str(p2Gold+loserGold)

        
        elif p2Health <=0:

          ##Awarded Gold
          awardPerc=round(p1Health*0.15)
          loserGold=int(players[enemy]["Gold"])
          goldAward=loserGold*(awardPerc/100)
          if goldAward < 1:
            goldAward =1

          p1Gold= int(players[userName]["Gold"])
          p2Gold= int(players[enemy]["Gold"])

          await ctx.send(f"You have won this battle! Your opponent fell to or below 0 health. Good job! You have earned {goldAward} gold from this battle")
          enemyTC=client.get_channel(int(players[enemy]["ActionCh"]))
          await enemyTC.send(f"You fell to or below 0 health so you have lost this battle. Better luck next time. You have lost {goldAward} gold from this battle.")
            
          ##P1
          players[userName]["Battle"]="Null"
          players[userName]["Deck"].clear()
          players[userName]["DiscardPile"].clear()
          players[userName]["TurnPile"].clear()
          players[userName]["DamageMult"]="1"
          players[userName]["StartedTurn"]="False"
          players[userName]["Gold"]=str(p1Gold+loserGold)

          ##P2
          players[enemy]["Battle"]="Null"
          players[enemy]["Deck"].clear()
          players[enemy]["DiscardPile"].clear()
          players[enemy]["TurnPile"].clear()
          players[enemy]["DamageMult"]="1"
          players[enemy]["StartedTurn"]="False"
          players[enemy]["Gold"]=str(p2Gold-loserGold)

        else:
          enemyTC=client.get_channel(int(players[enemy]["ActionCh"]))
          await enemyTC.send(f"Your enemy has ended thier turn. You have {p2Health} health remaining, and your opponent has {p1Health} health remaining. You can start your next turn now.")
          await ctx.send(f"Your turn has ended. You have {p1Health} health remaining, and your opponent has {p2Health} health remaining. You can start your next turn now.")
          with open("./players.json", "w") as j:
            json.dump(players, j, indent = 4)

      else:
          ##TODO add wait for enemy to end turn, if not, use AI to play for enemy
        enemyTC=client.get_channel(int(players[enemy]["ActionCh"]))
        await enemyTC.send("Your enemy has ended thier turn. You have 3 hours to end your turn or the bots AI will play your turn for you. If the AI plays 2 of your turns it will take over for the rest of this battle.")
        await ctx.send("You have ended your turn. Your enemy has 3 hours to end thier turn. If they do not in time, then the AI will take over for them.")
        players[userName]["TurnEnded"]="True"
        players[userName]["Hand"].clear()
        with open("./players.json", "w") as j:
          json.dump(players, j, indent = 4)
          ##3 hours = 10800 seconds
        await asyncio.sleep(10800)
        if players[enemy]["TurnEnded"]=="True":
          return
        else:
          if players[enemy]["StartedTurn"]=="True":
            mana = int(players[enemy]["Mana"])
            hand= players[enemy]["Hand"]
            for card in hand:
              if int(cards[card]["ManaCost"])<=mana:
                mana=mana-int(cards[card]["ManaCost"])
                players[enemy]["TurnPile"].append(card)
                players[enemy]["Hand"].remove(card)
              else:
                continue
            with open("./players.json", "w") as j:
              json.dump(players, j, indent = 4)
          else:
            hand = players[enemy]["Deck"][:5]
            players[enemy]["StartedTurn"]="True"
            players[enemy]["Mana"]="3"
            players[enemy]["Hand"]=hand
            mana = int(players[enemy]["Mana"])
        
            for card in hand:
              players[userName]["Deck"].remove(card)
              if int(cards[card]["ManaCost"])<=mana:
                mana=mana-int(cards[card]["ManaCost"])
                players[enemy]["TurnPile"].append(card)
                players[enemy]["Hand"].remove(card)
              else:
                continue

            ##Pasted here###########################
          players[enemy]["Hand"].clear()
          p1Damage=0
          p1Healing=0
          p2Damage=0
          p2Healing=0
          fogPlayed=False
          
          ##User
  
          ##TODO not removing last card in TurnPile
          for card in players[userName]["TurnPile"]:
            
            papercutsPlayed=False
            dmgMult=int(players[userName]["DamageMult"])
            players[userName]["DiscardPile"].append(card)
            players[userName]["TurnPile"].remove(card)
            p1Damage+=int(cards[card]["Damage"])
            p1Healing+=int(cards[card]["Healing"])
  
            if card == "Fog":
              fogPlayed=True
              continue
            elif card == "Bulk Up":
              dmgMult+=0.1
              continue
            elif card == "Papercuts":
              papercutsPlayed=True
              continue
  
          players[userName]["DamageMult"]=str(dmgMult)
          p1Damage=round(p1Damage*dmgMult)
          
          if papercutsPlayed:
            return
  
          ##Enemy
          for card in players[enemy]["TurnPile"]:
            
            papercutsPlayed=False
            dmgMult=int(players[enemy]["DamageMult"])
            players[enemy]["DiscardPile"].append(card)
            players[enemy]["TurnPile"].remove(card)
            p2Damage+=int(cards[card]["Damage"])
            p2Healing+=int(cards[card]["Healing"])
  
            if card == "Fog":
              fogPlayed=True
              continue
            elif card == "Bulk Up":
              dmgMult+=0.1
              continue
            elif card == "Papercuts":
              papercutsPlayed=True
              continue
  
          players[enemy]["DamageMult"]=str(dmgMult)
          p2Damage=round(p2Damage*dmgMult)
  
  
          ##2 damage, 3x
          ##TODO add attack count to all cards AND fix bulk up
          if papercutsPlayed:
            return
  
          ##Calculate
  
          if fogPlayed:
            p1Damage=0
            p2Damage=0
            
          p1Health=int(players[userName]["Health"])
          p2Health=int(players[enemy]["Health"])
  
          p1Health=p1Health-p2Damage+p1Healing
          p2Health=p2Health-p1Damage+p2Healing
  
    ##adding to datafile
          ##Health
          players[userName]["Health"]=str(p1Health)
          players[enemy]["Health"]=str(p2Health)
  
          ##Turn
          players[userName]["TurnEnded"]="False"
          players[enemy]["TurnEnded"]="False"
          players[userName]["StartedTurn"]="False"
          players[enemy]["StartedTurn"]="False"
  
          if p1Health <=0 and p2Health <=0:
            await ctx.send("This battle has resulted in a draw. Both players fell to or below zero health.")
            enemyTC=client.get_channel(int(players[enemy]["ActionCh"]))
            await enemyTC.send("This battle has resulted in a draw. Both players fell to or below zero health.")
  
            ##P1
            players[userName]["Battle"]="Null"
            players[userName]["Deck"].clear()
            players[userName]["DiscardPile"].clear()
            players[userName]["TurnPile"].clear()
            players[userName]["DamageMult"]="1"
            players[userName]["StartedTurn"]="False"
  
            ##P2
            players[enemy]["Battle"]="Null"
            players[enemy]["Deck"].clear()
            players[enemy]["DiscardPile"].clear()
            players[enemy]["TurnPile"].clear()
            players[enemy]["DamageMult"]="1"
            players[enemy]["StartedTurn"]="False"
  
          elif p1Health <=0:
  
            ##Awarded Gold
            awardPerc=round(p2Health*0.15)
            loserGold=int(players[userName]["Gold"])
            goldAward=loserGold*(awardPerc/100)
            if goldAward < 1:
              goldAward =1
  
            p1Gold= int(players[userName]["Gold"])
            p2Gold= int(players[enemy]["Gold"])
  
            await ctx.send(f"You fell to or below 0 health so you have lost this battle. Better luck next time. You have lost {goldAward} gold from this battle.")
            enemyTC=client.get_channel(int(players[enemy]["ActionCh"]))
            await enemyTC.send(f"You have won this battle! Your opponent fell to or below 0 health. Good job! You have earned {goldAward} gold from this battle")
              
            ##P1
            players[userName]["Battle"]="Null"
            players[userName]["Deck"].clear()
            players[userName]["DiscardPile"].clear()
            players[userName]["TurnPile"].clear()
            players[userName]["DamageMult"]="1"
            players[userName]["StartedTurn"]="False"
            players[userName]["Gold"]=str(p1Gold-loserGold)
  
            ##P2
            players[enemy]["Battle"]="Null"
            players[enemy]["Deck"].clear()
            players[enemy]["DiscardPile"].clear()
            players[enemy]["TurnPile"].clear()
            players[enemy]["DamageMult"]="1"
            players[enemy]["StartedTurn"]="False"
            players[enemy]["Gold"]=str(p2Gold+loserGold)
  
          
          elif p2Health <=0:
  
            ##Awarded Gold
            awardPerc=round(p1Health*0.15)
            loserGold=int(players[enemy]["Gold"])
            goldAward=loserGold*(awardPerc/100)
            if goldAward < 1:
              goldAward =1
  
            p1Gold= int(players[userName]["Gold"])
            p2Gold= int(players[enemy]["Gold"])
  
            await ctx.send(f"You have won this battle! Your opponent fell to or below 0 health. Good job! You have earned {goldAward} gold from this battle")
            enemyTC=client.get_channel(int(players[enemy]["ActionCh"]))
            await enemyTC.send(f"You fell to or below 0 health so you have lost this battle. Better luck next time. You have lost {goldAward} gold from this battle.")
              
            ##P1
            players[userName]["Battle"]="Null"
            players[userName]["Deck"].clear()
            players[userName]["DiscardPile"].clear()
            players[userName]["TurnPile"].clear()
            players[userName]["DamageMult"]="1"
            players[userName]["StartedTurn"]="False"
            players[userName]["Gold"]=str(p1Gold+loserGold)
  
            ##P2
            players[enemy]["Battle"]="Null"
            players[enemy]["Deck"].clear()
            players[enemy]["DiscardPile"].clear()
            players[enemy]["TurnPile"].clear()
            players[enemy]["DamageMult"]="1"
            players[enemy]["StartedTurn"]="False"
            players[enemy]["Gold"]=str(p2Gold-loserGold)
  
          else:
            enemyTC=client.get_channel(int(players[enemy]["ActionCh"]))
            await enemyTC.send(f"You took too long so the AI played for you. You have {p2Health} health remaining, and your opponent has {p1Health} health remaining. You can start your next turn now.")
            await ctx.send(f"Your enemy took to long, the AI played for them. You have {p1Health} health remaining, and your opponent has {p2Health} health remaining. You can start your next turn now.")
            with open("./players.json", "w") as j:
              json.dump(players, j, indent = 4)

            ##To here###########################     
        
  

####################################################################################################
################################      ADMIN      COMMANDS      #####################################
####################################################################################################

@client.command()
async def clearbattle(ctx):
  user=ctx.author
  if discord.utils.get(user.roles, name="Moderator") is None:
    await ctx.send('You don\'t have Admin roles')
  else:
    msg = await ctx.send("Who's battle do you want to clear?\nJust say one of the users in the proper format\nIE: PlayerName#0000")
    def check(m):
      return m.channel == ctx.channel and m.author == ctx.author
    
    try:
      reply= await client.wait_for("message",timeout=60.0,check=check)
  
    except asyncio.TimeoutError:
      await msg.delete()
      await ctx.send("Sorry you took too long.")
      
    else:
      found=False
      for k, v in players.items():
        if k == reply.content:
          found = True
          break
        else:
          found = False
      if found:
        op= players[reply.content]["Battle"]
        players[reply.content]["Battle"]="Null"
        players[reply.content]["Battle"]="Null"
        players[reply.content]["Deck"].clear()
        players[reply.content]["Hand"].clear()
        players[reply.content]["DiscardPile"].clear()
        players[reply.content]["TurnPile"].clear()
        players[reply.content]["DamageMult"]="1"
        players[reply.content]["StartedTurn"]="False"

        
        players[op]["Battle"]="Null"
        players[op]["Deck"].clear()
        players[op]["Hand"].clear()
        players[op]["DiscardPile"].clear()
        players[op]["TurnPile"].clear()
        players[op]["DamageMult"]="1"
        players[op]["StartedTurn"]="False"
        await ctx.send(f"Battle status has been cleared for:\n\n{reply.content}\n{op}")

        with open("./players.json", "w") as j:
          json.dump(players, j, indent = 4)
      else:
        await ctx.send("Sorry I could not find that user.")


@client.command()
async def givecard(ctx):
  user=ctx.author
  if discord.utils.get(user.roles, name="Moderator") is None:
    await ctx.send('You don\'t have Admin roles')
  else:
    msg = await ctx.send("Who would you like to give a card to?\nJust say one of the users in the proper format\nIE: PlayerName#0000")
    def check(m):
      return m.channel == ctx.channel and m.author == ctx.author
    
    try:
      reply= await client.wait_for("message",timeout=60.0,check=check)
  
    except asyncio.TimeoutError:
      await msg.delete()
      await ctx.send("Sorry you took too long.")
      
    else:
      found=False
      for k, v in players.items():
        if k == reply.content:
          player=reply.content
          found = True
          break
        else:
          found = False
      if found:
        cardList = []
        for k,v in cards.items():
          cardList.append(k)
        msg = await ctx.send("What card would you like to give\n"+"\n".join(cardList)+"\n\nBe sure to type the card name exactly as it appears")
        def check(m):
          return m.channel == ctx.channel and m.author == ctx.author
        
        try:
          reply= await client.wait_for("message",timeout=60.0,check=check)
      
        except asyncio.TimeoutError:
          await msg.delete()
          await ctx.send("Sorry you took too long.")
          
        else:
          found=False
          for c in cardList:
            if c == reply.content:
              card = reply.content
              found=True
              break
            else:
              found=False
          if found:
            players[player]["Inventory"].append(card)
            await ctx.send(card+" has been added to "+player+" inventory")
          else:
            await ctx.send("Sorry I could not find that card.")
      else:
        await ctx.send("Sorry I could not find that user.")
      
      
@client.command()
async def takecard(ctx):
  user=ctx.author
  if discord.utils.get(user.roles, name="Moderator") is None:
    await ctx.send('You don\'t have Admin roles')
  else:
    msg = await ctx.send("Who would you like to take a card from?\nJust say one of the users in the proper format\nIE: PlayerName#0000")
    def check(m):
      return m.channel == ctx.channel and m.author == ctx.author
    
    try:
      reply= await client.wait_for("message",timeout=60.0,check=check)
  
    except asyncio.TimeoutError:
      await msg.delete()
      await ctx.send("Sorry you took too long.")
      
    else:
      found=False
      for k, v in players.items():
        if k == reply.content:
          player=reply.content
          found = True
          break
        else:
          found = False
      if found:
        cardList = []
        for c in players[player]["Inventory"]:
          cardList.append(c)
        msg = await ctx.send("What card would you like to take\n"+"\n".join(cardList)+"\n\nBe sure to type the card name exactly as it appears")
        def check(m):
          return m.channel == ctx.channel and m.author == ctx.author
        
        try:
          reply= await client.wait_for("message",timeout=60.0,check=check)
      
        except asyncio.TimeoutError:
          await msg.delete()
          await ctx.send("Sorry you took too long.")
          
        else:
          found=False
          for c in cardList:
            if c == reply.content:
              card = reply.content
              found=True
              break
            else:
              found=False
          if found:
            players[player]["Inventory"].remove(card)
            await ctx.send(card+" has been removed from "+player+" inventory")
          else:
            await ctx.send("Sorry I could not find that card.")
      else:
        await ctx.send("Sorry I could not find that user.")

@client.command()
async def givegold(ctx):
  user=ctx.author
  if discord.utils.get(user.roles, name="Moderator") is None:
    await ctx.send('You don\'t have Admin roles')
  else:
    msg = await ctx.send("Who would you like to give gold to?\nJust say one of the users in the proper format\nIE: PlayerName#0000")
    def check(m):
      return m.channel == ctx.channel and m.author == ctx.author
    
    try:
      reply= await client.wait_for("message",timeout=60.0,check=check)
  
    except asyncio.TimeoutError:
      await msg.delete()
      await ctx.send("Sorry you took too long.")
      
    else:
      found=False
      for k, v in players.items():
        if k == reply.content:
          player=reply.content
          found = True
          break
        else:
          found = False
      if found:
        msg = await ctx.send("How much gold would you like to give?\nPlease enter a whole number ammount above 0.")
        def check(m):
          return m.channel == ctx.channel and m.author == ctx.author
        
        try:
          reply= await client.wait_for("message",timeout=60.0,check=check)
      
        except asyncio.TimeoutError:
          await msg.delete()
          await ctx.send("Sorry you took too long.")
          
        else:
          pGold=players[player]["Gold"]
          if int(reply.content) > 0:
            players[player]["Gold"]=str(int(pGold)+int(reply.content))
            await ctx.send(reply.content+" has been added to "+player+" gold\n"+player+" balance is now "+players[player]["Gold"])
          else:
            await ctx.send("Sorry, you entered an invalid amount")
      else:
        await ctx.send("Sorry I could not find that user.")

@client.command()
async def takegold(ctx):
  user=ctx.author
  if discord.utils.get(user.roles, name="Moderator") is None:
    await ctx.send('You don\'t have Admin roles')
  else:
    msg = await ctx.send("Who would you like to take gold from?\nJust say one of the users in the proper format\nIE: PlayerName#0000")
    def check(m):
      return m.channel == ctx.channel and m.author == ctx.author
    
    try:
      reply= await client.wait_for("message",timeout=60.0,check=check)
  
    except asyncio.TimeoutError:
      await msg.delete()
      await ctx.send("Sorry you took too long.")
      
    else:
      found=False
      for k, v in players.items():
        if k == reply.content:
          player=reply.content
          found = True
          break
        else:
          found = False
      if found:
        msg = await ctx.send("How much gold would you like to take?\nPlease enter a whole number ammount above 0.")
        def check(m):
          return m.channel == ctx.channel and m.author == ctx.author
        
        try:
          reply= await client.wait_for("message",timeout=60.0,check=check)
      
        except asyncio.TimeoutError:
          await msg.delete()
          await ctx.send("Sorry you took too long.")
          
        else:
          pGold=players[player]["Gold"]
          if int(reply.content) > 0:
            players[player]["Gold"]=str(int(pGold)-int(reply.content))
            await ctx.send(reply.content+" has been removed from "+player+" gold\n"+player+" balance is now "+players[player]["Gold"])
          else:
            await ctx.send("Sorry, you entered an invalid amount")
      else:
        await ctx.send("Sorry I could not find that user.")



@client.group(invoke_without_command = True) # for this main command (.help)
async def help(ctx):
    await ctx.send("For help please select a category:\nAdmin\nShop\nBattle\nProfile \nBe sure to type your answer as it appears here\n\nExample: !s help Battle")

@help.command()   #For this command (.help Admin)
async def Admin(ctx):
  user=ctx.author
  if discord.utils.get(user.roles, name="Moderator") is None:
    await ctx.send('You don\'t have Admin roles')
  else:
    await ctx.send("Admin commands:\nclearbattle - use to clear the battle status of a player and their enemy.\ngivecard - use to add a specific card to a players inventory\ntakecard - use to remove a specific card to a players inventory \ngivegold- use to give a specific amount of gold to a player\ntakegold - use to take a specific amount of gold from a player")

@help.command()   #And for this command (.help Utils)
async def Shop(ctx):
    await ctx.send("Shop commands:\nsetupshop - use to initially setup your shop. \nshop - use to browse all shops that you are whitelisted for \nshopadd - use to add a card form your inventory to your shop \nshopremove - use to remove a card from your shop and move it to your inventory \nshoplist - use to add a player to your shops whitelist, this is the only way people will be allowed to view your shop \ncheckshop - use to display all the details of your shop")

@help.command()   #And lastly this command (.help Fun)
async def Battle(ctx): 
    await ctx.send("Battle commands:\nstartbattle - use then command and tag a player to start battling them\n      Example: !s startbattle @Player1 \nstartturn - use to initiate your turn \nplaycard - use to play a card \nendturn use to end your turn")

@help.command()   #And lastly this command (.help Fun)
async def Profile(ctx): 
    await ctx.send("Profile commands: \nsetup - use to initially setup your profile \ncheckprofile - use to check all your profile stats \nbalance - use to check your balance specifically")

my_secret = os.environ['TOKEN']
client.run(my_secret)