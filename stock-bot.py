import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.support import expected_conditions as EC
from yahoo_fin.stock_info import get_data

load_dotenv() # Load .env file
TOKEN = os.getenv('DISCORD_TOKEN') # Get token from .env file
intents = discord.Intents.all() # Get all intents
print (TOKEN)
bot = commands.Bot(command_prefix='$',intents=intents) # Set command prefix

# Set up the web driver
driver = webdriver.Chrome('/path/to/chromedriver')

        
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

#Gets stock data from yahoo finance
@bot.command(name='getstock')
async def getstock(ctx, stockSymbol):
    if stockSymbol == None:
        await ctx.send('Please enter a stock symbol')
        return
    
    try:
        await ctx.send('Getting stock data for ' + stockSymbol)
        
        # Navigate to Yahoo Finance
        driver.get('https://finance.yahoo.com/')
        search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'yfin-usr-qry')))
        search_bar.send_keys(stockSymbol)
        search_bar.submit()
        
        # Wait for the stock page to load and get the URL
        stock_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href,"/quote/' + stockSymbol + '")]')))
        stock_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[contains(text(),"' + stockSymbol + '")]')))
        await ctx.send(stock_link.get_attribute('href'))
        
    #     # Get the current stock price
    #     price = stock_page.find_element(By.XPATH, '//span[contains(@data-reactid,"50")]')
    #     price_text = price.text

    #     # Get the stock chart picture
    #     chart = stock_page.find_element(By.XPATH, '//img[contains(@alt,"' + stockSymbol + ' chart")]')
    #     chart_link = chart.get_attribute('src')
    except NoSuchElementException:
        await ctx.send('Stock not found')
    
bot.run(TOKEN) # Run bot