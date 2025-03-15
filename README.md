# Custom ROTMG API  
Scrapes the [RealmEye website](https://www.realmeye.com) for most of the important information you could possibly need.  

## API Methods  

### Player Class  

#### `getPlayerInfo(userName: str, log: bool = False) -> dict`  
Retrieves basic player information from RealmEye.  

- `userName`: The player's in-game name.  
- `log`: If `True`, prints debug info.
- Returns: A dictionary containing player stats like rank, fame, and guild.  

#### `getPlayerCharacters(userName: str, log: bool = False) -> dict`  
Fetches character data for the specified player.  

- `userName`: The player's in-game name.  
- `log`: If `True`, prints debug info.
- Returns: A dictionary with character class, level, fame, and other details.  

#### `getPlayerPets(userName: str, log: bool = False) -> dict`  
Gets pet information for a player.  

- `userName`: The player's in-game name.  
- `log`: If `True`, prints debug info.
- Returns: A dictionary containing pet stats, abilities, and rarity.  

### Guild Information  

#### `getGuild(guildName: str, log: bool = False) -> dict`  
Retrieves information about a guild.  

- `guildName`: The name of the guild.  
- `log`: If `True`, prints debug info.
- Returns: A dictionary containing guild fame, members, and rankings.  

### Trading Data  

#### `getOfferCount(item: str, log: bool = False, ssnl: bool = False, offerType: str = "buy") -> int`  
Gets the number of trade offers for an item.  

- `item`: Name of the item.  
- `log`: If `True`, prints debug info.
- `ssnl`: Whether to check seasonal offers.  
- `offerType`: `"buy"` or `"sell"`.  
- Returns: The number of offers available.  

#### `getAllOffers(log: bool = False, ssnl: bool = False, offerType: str = "buy") -> dict`  
Retrieves all buy/sell offers available.  

- `log`: If `True`, prints debug info.
- `ssnl`: Whether to check seasonal offers.  
- `offerType`: `"buy"` or `"sell"`.  
- Returns: A dictionary with items and their respective offer counts.  

#### `convertItemToId(item: str, log: bool = False) -> int`  
Converts an item name to its RealmEye item ID.  

- `item`: Name of the item.  
- `log`: If `True`, prints debug info.
- Returns: The item’s unique ID.  

#### `getItemFromId(id: int) -> str`  
Retrieves an item name from its RealmEye item ID.  

- `id`: Item ID.  
- Returns: The item name.  

#### `getOffersFor(item: str, log: bool = False, ssnl: bool = False, offerType: str = "buy") -> list`  
Fetches a list of trade offers for a specific item.  

- `item`: Name of the item.  
- `log`: If `True`, prints debug info.
- `ssnl`: Whether to check seasonal offers.  
- `offerType`: `"buy"` or `"sell"`.  
- Returns: A list of trade offers.  

## Running the Script  
If run directly, the script provides an interactive menu to fetch player, guild, and trade data.
`python main.py`
Select options from the menu to retrieve information dynamically.