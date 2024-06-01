import discord
from discord.ext import tasks
import chat_window
import asyncio
import sys

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

def bot_wrapper():
    # Read in the token from the meta/TOKEN.txt file.
    with open("./TOKEN.txt", "r") as important:
        TOKEN = important.readline().strip()
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{name}'s messages"))
        print(f"{client.user} is now running!")

    # Watch for reactions
    @client.event
    async def on_raw_reaction_add(payload):
        
        # Get data from the payload
        server = await client.fetch_guild(payload.guild_id)
        channel = await client.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        message_author = message.author
        user = await client.fetch_user(int(payload.user_id))
        emoji = str(payload.emoji)
        username = user.name
        
        # Print to console
        print(f"{username} reacted to \"{message.content}\" (by {message_author}) \
    with {emoji} in #{channel} in {server}")

    # Watch for messages
    @client.event
    async def on_message(message):
        # Don't respond to our own messages
        if message.author == client.user:
            return

        # Get data from the message
        username = str(message.author)
        nick = str(message.author.nick)
        user_message = str(message.content)
        channel = message.channel
        server = message.guild

        # Print to console
        print(f"{nick} ({username}) said {user_message} in #{channel} in {server}")

    async def run_bot():
        # single worst line of code i have ever written
        globals()["name"] = input("Enter a username: ")
        discord.utils.setup_logging(root=False)
        await asyncio.gather(
            client.start(TOKEN),
            chat_window.run_console(client)
        )
    asyncio.run(run_bot())

def readme():
    with open("./README.md", "r+") as readme:
        lines = [line.strip("\n") for line in readme.readlines()]
        if len(lines) == 0:
            print("Error reading README")
        if lines[0] != "read:false":
            return
        readme.seek(0)
        lines[0] = "read:true "
        for idx in range(0, len(lines)):
            if (idx == 0):
                readme.write(lines[0])
            if (idx > 1):
                print(lines[idx])
        sys.exit(0)


if __name__ == "__main__":
    readme()
    bot_wrapper()