from requests import RequestException
import requests_html
session = requests_html.HTMLSession()
test = False

class Player:
    def __init__(self, userName):
        self.userName = userName

    def getPlayerInfo(self, userName: str = "HealthyGuy", log: bool = False):
        url = f"https://www.realmeye.com/player/{userName}"
        try:
            response = session.get(url)
            info = {}
            summary = response.html.find(".summary")[0]

            for i in range(0, summary.text.count("\n")+1, 2):
                category = response.html.find('td')[i].text
                categoryValue = response.html.find('td')[i+1].text
                if log:
                    print(category, ":", categoryValue)
                info[category] = categoryValue
            return info

        except RequestException as e:
            print(e)
            return None

    def getPlayerCharacters(self, userName: str = "HealthyGuy", log: bool = False):
        url = f"https://www.realmeye.com/player/{userName}"
        try:
            response = session.get(url)
            characters = {}
            charTable = response.html.find("#e > tbody > tr")
            characterCount = len(charTable)
            if characterCount == 0:
                return None

            for i, v in enumerate(charTable):
                data = v.find("td")
                dataShown = len(data)
                if dataShown > 8:
                    lastSeen = data[8].text
                else:
                    lastSeen = None
                if dataShown > 9:
                    server = data[9].text
                else:
                    server = None

                if log:
                    print("Pet:", data[0].find("abbr, span, a")[0].attrs.get("title", "Pets cannot be found at this time :("))
                    print("Class:", data[2].text)
                    print("Level:", data[3].text)
                    print("Fame:", data[4].text)
                    print("Place:", data[5].text)
                    print("Stats:", data[7].text)

                character = {"Class": str(data[2].text),
                             "Level": int(data[3].text),
                             "Fame": int(data[4].text),
                             "Place": int(data[5].text),
                             "Stats": str(data[7].text),
                             "Last Seen": str(lastSeen),
                             "Server": str(server)}
                characters[i%characterCount] = character
            return characters

        except RequestException as e:
            print(e)
            return None

    def getPlayerPets(self, userName: str = "HealthyGuy", log: bool = False):
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
        allOffers = response.html.find(".item-"+offerType+"ing")
        stripText = "Offers to "+offerType+" "

        for offer in allOffers:
            if len(offer.attrs["class"]) == 1:
                if item == offer.attrs["title"].lstrip(stripText):
                    if log:
                        print(f"There's {offer.text} {offerType} offer/s for {item}")
                    return int(offer.text)
        if log:
            print(f"There are no offers for a {item}")
        return 0

    except RequestException as e:
        print(e)
        return -1

def getAllOffers(log: bool = False, ssnl = False,  offerType = "buy"):
    try:
        if ssnl:
            url = f"https://www.realmeye.com/current-seasonal-offers"
        else:
            url = f"https://www.realmeye.com/current-offers"
        response = session.get(url)
        offerClass = ".item-buying"
        stripText = "Offers to buy "
        if offerType == "buy":
            offerClass = ".item-buying"
            stripText = "Offers to buy "
        elif offerType == "sell":
            offerClass = ".item-selling"
            stripText = "Offers to sell "

        allOffers = response.html.find(offerClass)
        offers = {}
        for offer in allOffers:
            if len(offer.attrs["class"]) == 1:
                title = offer.attrs["title"].lstrip(stripText)
                offers[title] = offer.text

        return offers

    except RequestException as e:
        print(e)
        return None

def getItemToId(item: str = "Potion of Defense", log: bool = False):
    try:
        url = "https://www.realmeye.com/current-offers"
        response = session.get(url)

        allOffers = response.html.find(".item-buying")
        for offer in allOffers:
            if len(offer.attrs["class"]) == 1:
                if item == offer.attrs["title"].lstrip("Offers to buy "):
                    return int(offer.attrs["href"].lstrip("/offers-to/buy/"))

    except RequestException as e:
        print(e)
        return None

def getItemFromId(id: int = 2592):
    try:
        url = f"https://www.realmeye.com/offers-to/buy/{id}"
        response = session.get(url)
        item = response.html.find("p > strong")[-1].text
        return item

    except RequestException as e:
        print(e)
        return None

def getOffersFor(item: str = "Potion of Defense", log: bool = False, ssnl = False, offerType = "buy"):
    try:
        url = f"https://www.realmeye.com/offers-to/{offerType}/{convertItemToId(item)}"
        if ssnl:
            url+="?seasonal"
        response = session.get(url)
        table = response.html.find("tbody > tr")
        return [row.find("td") for row in table]

    except RequestException as e:
        print(e)
        return []

if __name__ == "__main__":
    if not test:
        while True:
            choice = input("[1] Get player info\n[2] Get player characters\n[3] Get player pets\n[4] Get trade offers\n[5] View all offers\n[6] Get guild info\n[e] Exit\n")
            match choice:
                case "1":
                    player = Player(input("Player name: "))
                    print(player.getPlayerInfo(player.userName, False))
                case "2":
                    player = Player(input("Player name: "))
                    print(player.getPlayerCharacters(player.userName, True))
                case "3":
                    player = Player(userName = input("Player name: "))
                    print(player.getPlayerPets(player.userName, False))
                case "4":
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
                    choice = input(f"There are {getOfferCount(item, False, ssnl, tradeType)} offers selling {item}/s.\nWould you like to see them?[Y/n]").strip().upper()
                    if choice == "Y" or choice == "":
                        data = getOffersFor(item, False, ssnl, tradeType)
                        for i in data:
                            itemOffering = getItemFromId(i[0].find("span")[1].attrs['data-item'])

                            itemReturn = getItemFromId(i[1].find("span")[1].attrs['data-item'])
                            offer = f"{i[5].text} is offering {i[0].text.lstrip("×")} {itemOffering} for {i[1].text.lstrip("×")} {itemReturn} (x{i[2].text})"
                            print(offer)
                case "5":
                    tradeType = input("[B]uy or [S]ell? ").upper()
                    ssnl = input("Seasonal[y/N]: ").upper().strip()
                    if ssnl == "Y":
                        ssnl = True
                    else:
                        ssnl = False
                    if tradeType != "B" and tradeType != "S":
                        print("Invalid input.")
                        continue
                    if tradeType == "B":
                        tradeType = "buy"
                    elif tradeType == "S":
                        tradeType = "sell"
                    print(getAllOffers(False, ssnl, tradeType))
                case "6":
                    guild = input("Guild name: ")
                    print(getGuild(guild))
                case "e":
                    break
                case "E":
                    break
            print("\n")
