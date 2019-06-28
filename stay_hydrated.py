import discord
import asyncio
import re
import os
from pymongo import MongoClient

greet_re = re.compile(r'(Hello|Hi)(\?)?', re.IGNORECASE)

client = discord.Client()


@client.event
async def on_ready():
    print('Logged on as', client.user)
    await client.change_presence(activity=discord.Game(name="keeps you staying hydrated 💦"))


@client.event
async def on_resumed():
    await client.change_presence(activity=discord.Game(name="keeps you staying hydrated 💦"))


@client.event
async def on_member_update(before, after):
    mongo_client = MongoClient()
    db = mongo_client.stayhydrated

    users = db.users

    if users.find_one({"uuid": before.id}) is not None:
        if before.status is not after.status and after.status == discord.Status.online:
            users.update_one({"uuid": before.id}, {"$set": {"active": True}})

        if before.status is not after.status and after.status == discord.Status.offline:
            users.update_one({"uuid": before.id}, {"$set": {"active": False, "counting": 0}})


@client.event
async def on_message(message):
    help_embed = discord.Embed(title="How to stay hydrated", color=discord.colour.Color.blue(), description="Hello, I am StayHydrated a discord bot developed by Breuxi#6341\nI can help you staying hydrated by sending you timed reminders to drink some water :D But we have to be on at least one Server together :o")
    help_embed.add_field(name="Commands", value="h-register every <Interval> <Minutes|Hours> -> Register for a hydration reminder\nh-unregister -> Unregister from your reminder", inline=False)

    if message.author == client.user:
        return

    # Help Command in every Channel, private and server
    if message.content.lower().startswith("h-help"):
        async with message.channel.typing():
            await message.channel.send(embed=help_embed)

    # User Specific Commands
    if message.channel.type == discord.ChannelType.private:
        if greet_re.match(message.content):
            await message.channel.send(embed=help_embed)

        # h-register every <Interval> <Minutes|Hours> while <online|gaming>
        if message.content.lower().startswith("h-register"):
            if "every" in message.content.lower():
                args = message.content.split(" ")

                interval = 0

                try:
                    interval = int(args[2])
                except Exception:
                    await message.channel.send("Error: Interval must be a number")
                    return

                time_type = args[3]
                while_doing = args[5]

                mongo_client = MongoClient()
                db = mongo_client.stayhydrated

                users = db.users

                member = None
                for guild in client.guilds:
                    member = guild.get_member(message.author.id)
                    if member is not None:
                        break

                if member is None:
                    async with message.channel.typing():
                        await message.channel.send("Error: You have to be at least on one server with me!")

                active = member.status == discord.Status.online

                users.insert_one({"uuid": message.author.id, "interval": interval, "counting": 0, "interval_type": time_type, "while": while_doing, "active": active})

                await message.channel.send("All set! You will receive your reminder every {} {} while {}".format(interval, time_type, while_doing))
            else:
                await message.channel.send("Error, wrong format! Please use h-register every <Interval> <Minutes|Hours>")

        if message.content.lower().startswith("h-unregister"):
            mongo_client = MongoClient()
            db = mongo_client.stayhydrated

            users = db.users

            users.delete_one({"uuid": message.author.id})
            await message.channel.send("All right, I will unregister you from the reminder, stay safe and hydrated! :o")

    # Server Commands
    if message.channel.type == discord.ChannelType.text:
        pass


async def health_task():
    await client.wait_until_ready()
    while not client.is_closed():

        mongo_client = MongoClient()
        db = mongo_client.stayhydrated

        users = db.users

        for user in users.find({"active": True}):
            if str(user['interval_type']).lower() == "minutes":
                if user['counting'] == user['interval']:
                    users.update_one({"uuid": user["uuid"]}, {"$set": {'counting': 0}})
                    discord_user = client.get_user(user["uuid"])

                    async with discord_user.typing():
                        await discord_user.send("Hello, I would like to remind you to drink some water! 💦")

            if str(user['interval_type']).lower() == "hours":
                interval = user['interval'] * 60
                if user['counting'] == interval:
                    users.update_one({"uuid": user["uuid"]}, {"$set": {'counting': 0}})
                    discord_user = client.get_user(user["uuid"])

                    async with discord_user.typing():
                        await discord_user.send("Hello, I would like to remind you to drink some water! 💦")
            users.update_one({"uuid": user["uuid"]}, {"$inc": {'counting': 1}})
        await asyncio.sleep(60) # task runs every 60 seconds


client.loop.create_task(health_task())
client.run(os.environ["discord_token"])
