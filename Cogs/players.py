import discord
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import json
import random
import asyncio


class Item:
    def __init__(self, name, cost, description):
        self.name = name
        self.cost = cost
        self.description = description


class Pet:
    def __init__(self, name, Type):
        self.name = name
        self.type = Type


async def saveMoney(ctx, players):
    for Players, value in players.items():
        items = []
        for item, amount in value.items.items():
            items.append([item.name, getPrice(item.name), item.description, amount])
        players[str(Players)] = [int(value['money']), items, value.pet]
    with open("../Bots/servers.json", "r") as f:
        storage = json.load(f)
    storage["players"] = players
    with open("../Bots/servers.json", "w") as f:
        json.dump(storage, f, indent=4)


def getPrice(items):
    price = ""
    storage = json.load(open("../Bots/servers.json"))
    players = storage["players"]
    for value in players.values():
        for item in value.items:
            if str(item.name).lower() == items.lower():
                price = item.cost
        break
    return price


def refreshBalance():
    with open("../Bots/servers.json", "r") as f:
        storage = json.load(f)
    players = storage["players"]
    for key, value in players.items():
        items = {}
        item = value[1]
        for i in item:
            items[Item(i[0], i[1], i[2])] = i[3]
        players[key] = Player(value[0], items, value[2])
    return players


def addItem():
    newItems = {
        Item("Airpods", getPrice("airpods"),
             "flex on all the poor people with this symbol being able to waste money."): 0,
        Item("iPhone", getPrice("iphone"),
             "A genuinely good phone, but also for flexing on the poor people."): 0,
        Item("Pencil", getPrice("pencil"),
             "I don't even know what this is for anymore... something called writing? Anyways, it's pretty much useless now."): 0,
        Item("Pokemon card", getPrice("pokemon card"),
             "A relic from an ancient time, when these were traded and collected."): 0,
        Item("Bumper Sticker", getPrice("bumper sticker"),
             "You can put it on your car and show off your style... or so you say. In reality, it will end up lying forgotten on the kitchen counter for all of time."): 0,
        Item("Hangman", getPrice("hangman"), "Play hangman against Hurb! Not just an item, but a whole game!"): 0,
        Item("Autodoggo", getPrice("autocatto"),
             "Just like the `%doggo` command, but shows you a new doggo every 7 seconds!"): 0,
        Item("Autocatto", getPrice("autocatto"),
             "Just like the `%catto` command, but shows you a new catto every 7 seconds!"): 0
    }
    storage = json.load(open("../Bots/servers.json"))
    players = storage["players"]
    for player, value in players.items():
        for item in player.items:
            if item in newItems.keys():
                pass


class Player(commands.Cog):
    def __init__(self, money, items, pet):
        self.money = money
        self.itemStartList = {
            Item("Airpods", 10000, "flex on all the poor people with this symbol being able to waste money."): 0,
            Item("iPhone", 100000, "A genuinely good phone, but also for flexing on the poor people."): 0,
            Item("Pencil", 300,
                 "I don't even know what this is for anymore... something called writing? Anyways, it's pretty much useless now."): 0,
            Item("Pokemon card", 500, "A relic from an ancient time, when these were traded and collected."): 0,
            Item("Bumper Sticker", 400,
                 "You can put it on your car and show off your style... or so you say. In reality, it will end up lying forgotten on the kitchen counter for all of time."): 0,
            Item("Hangman", 20000, "Play hangman against Hurb! Not just an item, but a whole game!"): 0,
            Item("Autodoggo", 10000, "Just like the `%doggo` command, but shows you a new doggo every 7 seconds!"): 0,
            Item("Autocatto", 10000, "Just like the `%catto` command, but shows you a new catto every 7 seconds!"): 0
        }
        self.pet = pet
        self.items = items

    @commands.command()
    async def start(self, ctx):
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]
        if str(ctx.author.id) in players.keys():
            await ctx.send(
                embed=discord.Embed(description=f"You already have an account with this bot {ctx.author.mention}!"))
        else:
            money = random.randint(500, 2000)
            if players != {}:
                players[str(ctx.author.id)] = Player(money, {
                    Item("Airpods", getPrice("airpods"),
                         "flex on all the poor people with this symbol being able to waste money."): 0,
                    Item("iPhone", getPrice("iphone"),
                         "A genuinely good phone, but also for flexing on the poor people."): 0,
                    Item("Pencil", getPrice("pencil"),
                         "I don't even know what this is for anymore... something called writing? Anyways, it's pretty much useless now."): 0,
                    Item("Pokemon card", getPrice("pokemon card"),
                         "A relic from an ancient time, when these were traded and collected."): 0,
                    Item("Bumper Sticker", getPrice("bumper sticker"),
                         "You can put it on your car and show off your style... or so you say. In reality, it will end up lying forgotten on the kitchen counter for all of time."): 0,
                    Item("Hangman", getPrice("hangman"),
                         "Play hangman against Hurb! Not just an item, but a whole game!"): 0,
                    Item("Autodoggo", getPrice("autocatto"),
                         "Just like the `%doggo` command, but shows you a new doggo every 7 seconds!"): 0,
                    Item("Autocatto", getPrice("autocatto"),
                         "Just like the `%catto` command, but shows you a new catto every 7 seconds!"): 0
                }, "")
            else:
                players[str(ctx.author.id)] = Player(money, self.itemStartList, "")
            embed = discord.Embed(
                description=f"Ok {ctx.author.mention}, I've started an account for you with ${money} in it! Use the `%help economy` command to see what games you can play and what stuff you can buy!",
                color=discord.Color.green())
            await ctx.send(embed=embed)
            storage["players"] = players
            json.dump(storage, open("../Bots/servers.json", "w"), indent=4)

    @commands.command()
    @commands.cooldown(1, 3600, BucketType.user)
    async def hourly(self, ctx):
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]

        players[str(ctx.author.id)]['money'] += 100
        await ctx.send(embed=discord.Embed(description=f"Hourly claimed {ctx.author.mention}. You gained $100!"))
        storage["players"] = players
        json.dump(storage, open("../Bots/servers.json", "w"), indent=4)

    @commands.command()
    @commands.cooldown(1, 86400, BucketType.user)
    async def daily(self, ctx):
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]

        players[str(ctx.author.id)]['money'] += 500
        await ctx.send(embed=discord.Embed(description=f"Daily claimed {ctx.author.mention}. You gained $500!"))
        storage["players"] = players
        json.dump(storage, open("../Bots/servers.json", "w"), indent=4)

    @commands.command(aliases=["b", "B", "Balance", "BALANCE", "bal", "Bal", "BAL"])
    async def balance(self, ctx, member: discord.Member = None):
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]
        if member is None:
            await ctx.send(embed=discord.Embed(
                description=f"Your balance, {ctx.author.mention}, is ${players[str(ctx.author.id)]['money']}."))
        else:
            if str(member.id) in players.keys():
                await ctx.send(embed=discord.Embed(
                    description=f"{member.display_name} has ${players[str(member.id)]['money']} in their account."))
            else:
                await ctx.send(embed=discord.Embed(
                    description=f"I could not find an account for {member.display_name}, {ctx.author.mention}."))

    @commands.command(aliases=["Items", "ITEMS", "inv", "INV", "Inv", "inventory", "Inventory", "INVENTORY"])
    async def items(self, ctx):
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]

        embed = discord.Embed(color=discord.Color.teal())
        embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.author.display_name}'s items:")
        for item, value in player.items.items():
            if value != "none" and value != 0 and value != "0":
                embed.add_field(name=f"{item.name}", value=f"{value} owned.")
        await ctx.send(embed=embed)

    @commands.command()
    async def shop(self, ctx):
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]

        embed = discord.Embed(color=discord.Color.teal())
        embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.author.display_name}'s items:")
        for item, value in player.items.items():
            if isinstance(item.cost, float) or isinstance(item.cost, int):
                embed.add_field(name=f"{item.name}", value=f"Price: ${int(item.cost)}\nAmount owned: {value}")
            else:
                embed.add_field(name=f"{item.name}", value=f"Price: Unbuyable\nAmount owned: {value}")
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, *, Items):
        Items = Items.lower()
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]

        for item in player.items.keys():
            if item.name.lower() == Items:
                if item.cost == "none":
                    await ctx.send(embed=discord.Embed(description=f"You cannot buy this item {ctx.author.mention}!",
                                                       color=discord.Color.red()))
                else:
                    if float(players[str(ctx.author.id)]['money']) >= float(item.cost):
                        player.items[item] += 1
                        item.cost = float(item.cost)
                        players[str(ctx.author.id)]['money'] -= item.cost
                        item.cost *= 1.1
                        await ctx.send(
                            embed=discord.Embed(description=f"You have purchased a {item.name} {ctx.author.mention}!",
                                                color=discord.Color.green()))
                    else:
                        await ctx.send(embed=discord.Embed(
                            description=f"You cannot afford to buy this item {ctx.author.mention}! You need ${item.cost}, and you only have ${players[str(ctx.author.id)]['money']}!",
                            color=discord.Color.red()))
        storage["players"] = players
        json.dump(storage, open("../Bots/servers.json", "w"), indent=4)

    @commands.command(aliases=["Rob", "ROB", "steal", "Steal", "STEAL"])
    @commands.cooldown(1, 120, BucketType.user)
    async def rob(self, ctx, Member: discord.Member):
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]
        if str(Member.id) in players.keys():
            robber = players[str(ctx.author.id)]
            victim = players[str(Member.id)]
            if victim['money'] >= 200:
                if robber['money'] >= 200:
                    if robber['money'] <= victim['money']:
                        stolen = random.choice(
                            ["success", "failure", "failure", "failure", "failure", "success", "success"])
                        amount_stolen = random.randint(1, int(victim['money'] / 5))
                        if stolen == "success":
                            victim['money'] -= amount_stolen
                            robber['money'] += amount_stolen
                            await ctx.send(embed=discord.Embed(
                                description=f"You stole ${amount_stolen}! Good work, you nasty little thief."))
                        elif stolen == "failure":
                            if robber['money'] <= amount_stolen:
                                victim['money'] += robber['money']
                                robber['money'] = 0
                                players[str(ctx.author.id)] = robber
                                players[str(Member.id)] = victim
                                await ctx.send(embed=discord.Embed(description=random.choice([
                                                                                                 f"You didn't realize that they were actually a cop in disguise, and they forced you to give them all your money.",
                                                                                                 f"You dropped their wallet as you were stealing it, and became so flustered that you dropped your own as well."])))
                            else:
                                robber['money'] -= amount_stolen
                                victim['money'] += amount_stolen
                                players[str(ctx.author.id)] = robber
                                players[str(Member.id)] = victim
                                await ctx.send(embed=discord.Embed(description=random.choice([
                                                                                                 f"You didn't realize that they were actually a cop in disguise, and they forced you to pay them a fine of ${amount_stolen}.",
                                                                                                 f"You dropped their wallet as you were stealing it, and became so flustered that you dropped ${amount_stolen}."])))
                    else:
                        await ctx.send(embed=discord.Embed(
                            description=f"Cmon man, you got more money than {Member.mention}. Give them a break, will ya?"))
                else:
                    await ctx.send(embed=discord.Embed(description=f"You need to have at least $200 to rob someone."))
            else:
                await ctx.send(
                    embed=discord.Embed(description=f"{Member.mention} doesn't even have $200, it's not worth it."))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{Member.mention} does not have an account with this bot yet {ctx.author.mention}!"))
        storage["players"] = players
        json.dump(storage, open("../Bots/servers.json", "w"), indent=4)

    @commands.command(aliases=["dep", "Deposit", "Dep", "DEP", "DEPOSIT"])
    @commands.cooldown(1, 120, BucketType.user)
    async def deposit(self, ctx, amount):
        storage = json.load(open("../Bots/servers.json"))
        player = storage["players"][str(ctx.author.id)]
        if amount.lower() == "all" or amount.lower() == "max":
            amount = int(player["money"]*0.3)
            player["bank"] += amount
            player["money"] -= amount
            await ctx.send(f"You have deposited {amount} into your bank.")
            storage["players"][str(ctx.author.id)] = player
            json.dump(storage, open("../Bots/servers.json", "w"), indent=4)
        elif amount.isnumeric():
            amount = int(amount)
            if amount > int(player["money"]):
                await ctx.send(f"You can't deposit more than you have {ctx.author.mention}!")
            elif amount > int(player["money"] * 0.3):
                amount = int(player["money"]*0.3)
            player["bank"] += amount
            player["money"] -= amount
            await ctx.send(f"You have deposited {amount} into your bank.")
            storage["players"][str(ctx.author.id)] = player
            json.dump(storage, open("../Bots/servers.json", "w"), indent=4)
        else:
            await ctx.send(f"Please enter a valid amount to deposit.")

    @commands.command(aliases=["With", "with", "WITH", "Withdraw", "WITHDRAW"])
    @commands.cooldown(1, 30, BucketType.user)
    async def withdraw(self, ctx, amount):
        storage = json.load(open("../Bots/servers.json"))
        player = storage["players"][str(ctx.author.id)]
        if amount.lower() == "all" or amount.lower() == "max":
            player["money"] += int(player["bank"])
            player["bank"] = 0
            storage["players"][str(ctx.author.id)] = player
            json.dump(storage, open("../Bots/servers.json", "w"), indent=4)
        elif amount.isnumeric():
            amount = int(amount)
            if amount > int(player["bank"]):
                await ctx.send(f"You can't withdraw more than you have.")
            else:
                player["money"] += amount
                player["bank"] -= amount
                await ctx.send(f"You have withdrawn {amount} from your bank.")
                storage["players"][str(ctx.author.id)] = player
                json.dump(storage, open("../Bots/servers.json", "w"), indent=4)
        else:
            await ctx.send(f"Please enter a valid amount to withdraw.")

    @commands.command()
    async def give(self, ctx, member: discord.Member, amount):
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]
        donor = players[str(ctx.author.id)]
        Member = players[str(member.id)]
        if donor['money'] >= int(amount) >= 0:
            Member['money'] += int(amount)
            donor['money'] -= int(amount)
            await ctx.send(
                embed=discord.Embed(description=f"{ctx.author.mention} has given ${amount} to {member.mention}.",
                                    color=discord.Color.green()))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{ctx.author.mention} you do not have enough money to give ${amount}!"))
        storage["players"] = players
        json.dump(storage, open("../Bots/servers.json", "w"), indent=4)

    @commands.command()
    async def addmoney(self, ctx, member: discord.Member, amount):
        if ctx.author.id == 670493561921208320:
            storage = json.load(open("../Bots/servers.json"))
            players = storage["players"]
            Member = players[str(member.id)]
            Member['money'] += int(amount)
            await ctx.send(
                embed=discord.Embed(description=f"{ctx.author.mention} has added ${amount} to {member.mention}.",
                                    color=discord.Color.green()))
            storage["players"] = players
            json.dump(storage, open("../Bots/servers.json", "w"), indent=4)
        else:
            await ctx.send("NOPE")


def setup(bot):
    bot.add_cog(Player("none", "none", "none"))
