import discord, sqlite3, json, time
from utils import check_wallet
from utils import send_fweb3

with open("config/config.json", "r+", encoding="utf-8") as configfile:
    config = json.load(configfile)

# ========= CONFIG ================
TOKEN = config["bot_token"]
AMOUNT = config["amount_to_send"]
PUBLIC_KEY = config["faucet_public_key"]
PRIVATE_KEY = config["faucet_private_key"]
# =================================

cord = discord.Client()

@cord.event
async def on_ready():
    print("""
               __
             <(o )___
              ( ._> /
               `---'
        """)
    print(f'* Successfully Logged in as: {cord.user}')

@cord.event
async def on_message(message):

    # ignoring private messages to prevent abuse
    if message.channel.type is discord.ChannelType.private: 
        return

    # ignoring bot's own messages
    requester = message.author
    if message.author == cord.user:
        return

    if message.content.startswith("!faucet") and message.channel.name in "faucet":
        channel = message.channel
        requester_address = str(message.content).replace("!faucet", "").replace(" ", "").lower()
        
        # discord account must be 30 days old or newer to prevent abuse
        
        if time.time() - requester.created_at.timestamp() < 2492000:
            await channel.send(f"🚫 {requester.mention}, your account must be 30 days or older to use this faucet.")
            return
            
        connection = sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (requester.id,))
        if item := cursor.fetchone():
            await channel.send(f"🚫 {requester.mention}, you have already used the faucet!")
            return
        else:
            pass
            
        
        # checking if the provided wallet is valid
        if check_wallet(requester_address):
            
            
            # adding user's unique id to our db
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            rows = [('claimed', requester.id)]
            cursor.executemany('insert into users values (?,?)', rows)
            connection.commit()
            
            # sending fweb3 tokens
            #
            await channel.send(f"✅ {requester.mention}, https://polygonscan.com/tx/{send_fweb3(AMOUNT, PUBLIC_KEY, PRIVATE_KEY, requester_address)}")
        else:
            await channel.send(f"🚫 {requester.mention}, invalid wallet was provided. **Usage**: !faucet YOUR_WALLET")
            
            
cord.run(TOKEN)