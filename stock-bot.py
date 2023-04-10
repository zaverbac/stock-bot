import discord
from discord.ext import commands

 # $ is the prefix for the bot
stockbot = commands.Bot(command_prefix='$')

@stockbot.event
async def on_ready():
    print("Stock Bot is ready!")
    
@stockbot.command(name='getstock')
async def getstock(ctx, stock):
    await ctx.send("Getting info for " + stock)
    