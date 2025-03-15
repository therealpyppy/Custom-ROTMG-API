import os
from requests import RequestException
from requests_html import HTMLSession
session = HTMLSession()
test = False

def getPlayerInfo(userName: str = "HealthyGuy"):
    url = f"https://www.realmeye.com/player/{userName}"
    try:
        response = session.get(url)
        info = {}
        summary = response.html.find(".summary")[0]

        for i in range(0, summary.text.count("\n")+1, 2):
            category = response.html.find('td')[i].text
            categoryValue = response.html.find('td')[i+1].text
            #print(category, ":", categoryValue)
            info[category] = categoryValue
        return info

    except RequestException as e:
        print(e)
        return None
    
def getPlayerCharacters(userName: str = "HealthyGuy", log: bool = False):
    url = f"https://www.realmeye.com/player/{userName}"
    try:
        response = session.get(url)
        characters = {}
        characterCount = len(response.html.find("#e > tbody > tr"))
        if characterCount == 0:
            return None
        data = response.html.find("#e > tbody > tr > td")
        dataShown = len(data)//characterCount

        for i in range(0,characterCount*dataShown, dataShown):
            if log:
                print("Pet:", data[i].find("abbr, span, a")[0].attrs.get("title", "Pets cannot be found at this time :("))
                print("Class:", data[i+2].text)
                print("Level:", data[i+3].text)
                print("Fame:", data[i+4].text)
                print("Place:", data[i+5].text)
                print("Stats:", data[i+7].text)
                if dataShown > 8:
                    print("Last Seen:", data[i+8].text)
                if dataShown > 9:
                    print("Server:", data[i+9].text)

            if dataShown > 8:
                lastSeen = data[i+8].text
            else:
                lastSeen = None
            if dataShown > 9:
                server = data[i+9].text
            else:
                server = None

            character = {"Pet": data[i].find("abbr, span, a")[0].attrs.get("title", "Pets cannot be found at this time :("),
                            "Class": data[i+2].text,
                            "Level": data[i+3].text,
                            "Fame": data[i+4].text,
                            "Place": data[i+5].text,
                            "Stats": data[i+7].text,
                            "Last Seen": lastSeen,
                            "Server": server}
            characters[i%characterCount] = character
        return characters

    except RequestException as e:
        print(e)
        return None
    
def getPlayerPets(userName: str, log: bool = False):
    url = f"https://www.realmeye.com/pets-of/{userName}"
    try:
        response = session.get(url)
        pets = {}
        for i, v in enumerate(response.html.find("#e > tbody > tr")):
            pet = {}
            Name = v.find("td")[1].text
            Rarity = v.find("td")[2].text
            Family = v.find("td")[3].text
            Place = v.find("td")[4].text
            Ability1 = v.find("td")[5].text
            Ability1Level = v.find("td")[6].text
            Ability2 = v.find("td")[7].text
            Ability2Level = v.find("td")[8].text
            Ability3 = v.find("td")[9].text
            Ability3Level = v.find("td")[10].text
            MaxLevel = v.find("td")[11].text
            pet["Name"] = Name
            pet["Rarity"] = Rarity
            pet["Family"] = Family
            pet["Place"] = Place
            pet["Ability1"] = Ability1
            pet["Ability1Level"] = Ability1Level
            pet["Ability2"] = Ability2
            pet["Ability2Level"] = Ability2Level
            pet["Ability3"] = Ability3 
            pet["Ability3Level"] = Ability3Level
            pet["MaxLevel"] = MaxLevel

            if log:
                print(f"Name : {Name}\nRarity : {Rarity}\nFamily : {Family}\nPlace : {Place}\nAbility 1 : {Ability1}\nAbility 1 Level : {Ability1Level}\nAbility 2 : {Ability2}\nAbility 2 Level : {Ability2Level}\nAbility 3 : {Ability3}\nAbility 3 Level : {Ability3Level}\nMax Level : {MaxLevel}\n")

            pets[i] = pet
        return pets

    except RequestException as e:
        print(e)
        return None
    
def getItemFromId(id: int = 0):
    print()

def getGuild(guildName: str = "Frog Bait", log: bool = False):
    try:
        url = f"https://www.realmeye.com/guild/{guildName.replace(" ", "%20")}"
        response = session.get(url)
        guildInfo = {}
        famePlayer = {}
        fameList = {}

        for info in response.html.find(".summary > tr"):
            info = info.text.split("\n")
            guildInfo[info[0]] = info[1]
        if log:
            print(guildInfo)
        for player in response.html.find("#e > tbody> tr"):
            name = player.find("td")[1].text
            fame = player.find("td")[3].text
            famePlayer[int(fame)] = name
        if log:
            print(famePlayer)
        for i in sorted(famePlayer, reverse=True):
            fameList[famePlayer[i]] = i
        if log:
            print(fameList)
        guildInfo['PlayersByFame'] = fameList
        return guildInfo

    except RequestException as e:
        print(e)
        return None
    
def getOfferCount(item: str = "Potion of Defense", log: bool = False, ssnl = False, offerType = "buy"):
    try:
        if ssnl:
            url = f"https://www.realmeye.com/current-seasonal-offers"
        else:
            url = f"https://www.realmeye.com/current-offers"
        response = session.get(url)
        if offerType == "buy":
            offers = response.html.find(".item-buying")
            stripText = "Offers to buy "
        elif offerType == "sell":
            offers = response.html.find(".item-selling")
            stripText = "Offers to sell "
        for offer in offers:
            if len(offer.attrs["class"]) == 1:
                if item == offer.attrs["title"].lstrip(stripText):
                    if log:
                        print(f"There's {offer.text} {offerType} offer/s for {item}")
                    return offer.text
        if log:
            print(f"There are no offers for a {item}")
        return 0

    except RequestException as e:
        print(e)
        return None

def getAllSelling(log: bool = False):
    try:
        url = f"https://www.realmeye.com/current-offers"
        response = session.get(url)
        sellOffers = response.html.find(".item-selling")
        offers = {}
        for offer in sellOffers:
            if len(offer.attrs["class"]) == 1:
                title = offer.attrs["title"].lstrip("Offers to sell ")
                offers[title] = offer.text

        return offers
    
    except RequestException as e:
        print(e)
        return None

def getAllBuying(log: bool = False):
    try:
        url = f"https://www.realmeye.com/current-offers"
        response = session.get(url)
        sellOffers = response.html.find(".item-buying")
        offers = {}
        for offer in sellOffers:
            if len(offer.attrs["class"]) == 1:
                title = offer.attrs["title"].lstrip("Offers to buy ")
                offers[title] = offer.text

        return offers
    
    except RequestException as e:
        print(e)
        return None

def end():
    print()

def unit():
    failedTests = []
    try: getPlayerInfo()
    except: failedTests.append(1)
    try: getPlayerCharacters()
    except: failedTests.append(2)
    try: getOfferCount()
    except: failedTests.append(3)
    try: getAllBuying()
    except: failedTests.append(4)
    try: getAllSelling()
    except: failedTests.append(5)
    try: getGuild()
    except: failedTests.append(6)
    for i in failedTests:
        print(i)

if __name__ == "__main__":
    if not test:
        while True:
            choice = input("[1] Get player info\n[2] Get player characters\n[3] Get trade offers\n[4] View all BUY offers\n[5] View all SELL offers\n[6] Get guild info\n[e] Exit\n")
            if choice == "1":
                username = input("Player name: ")
                print(getPlayerInfo(username))
                end()
            elif choice == "2":
                username = input("Player name: ")
                print(getPlayerCharacters(username))
                end()
            elif choice == "3":
                tradeType = input("[B]uy or [S]ell? ").upper()
                if tradeType != "B" and tradeType != "S":
                    print("Invalid input.")
                    continue
                if tradeType == "B":
                    tradeType = "buy"
                elif tradeType == "S":
                    tradeType = "sell"

                ssnl = input("Seasonal[y/N]: ").upper().strip()
                if ssnl == "N":
                    ssnl = False
                elif ssnl == "Y":
                    ssnl = True
                else:
                    ssnl = False
                item = input("Item: ")
                print(f"There are {getOfferCount(item, False, ssnl, tradeType)} offers selling {item}/s")
                end()
            elif choice == "4":
                print(getAllBuying())
                end()
            elif choice == "5":
                print(getAllSelling())
                end()
            elif choice == "6":
                guild = input("Guild name: ")
                print(getGuild(guild))
                end()
            elif choice == "e":
                os.close()
            elif choice == "unit":
                unit()
                end()