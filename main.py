import discord
import os 
from dotenv import load_dotenv
from discord.ext import commands 
import pdfplumber
from review import getResponse
import ctypes

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents = intents)

@bot.event
async def on_ready():
    pass

@bot.command()
async def review(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.channel.send("No CV/Resume file attached")
        return
    
    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith('.pdf'):
        await ctx.channel.send("Invalid file format. Please upload a pdf")
        return
    
    try: 
        await attachment.save(attachment.filename)
        with pdfplumber.open('{}'.format(attachment.filename)) as doc:
            resumeText = ""
            for page in doc.pages:
                resumeText += page.extract_text()
            #Pass resume text into the chatgpt API model
            await ctx.channel.send(getResponse(resumeText))
        os.remove(attachment.filename)
    except Exception as e:
        print(e)
        await ctx.channel.send("Unable to save file. Please try again")
        return



@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    
    if not message.content.startswith('/review') or not message.content.startswith('/feedback'):
        return 


load_dotenv()
bot.run(os.getenv('TOKEN'))