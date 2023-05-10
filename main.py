import discord
from discord.ext import commands
from discord import app_commands 
from constants import TOKEN
from experience import Experience
import random 
import requests 

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print("Synced")
    except:
        pass 

experience = Experience()

@bot.tree.command(name="cute-cat")
async def cute_cat(interaction: discord.Interaction):
    with open("tmp.gif", "wb+") as f:
        f.write(requests.get("https://cataas.com/cat/cute").content)
        f.close()
    with open("tmp.gif", "rb") as f:
        file = discord.File(f)
        f.close()
    await interaction.response.send_message(file=file)    

@bot.tree.command(name="purge")
@app_commands.describe(amount="Amount to purge")
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if not experience.user_exists(message.author.id):
        experience.add_user_to_db(message.author.id, 1 * 12, experience.level_for_xp(1 * 12), 1)
    else:
        experience.add_experience(message.author.id, random.randint(10,12))
        level = experience.level_up(message.author.id)
        if level != False:
            await message.channel.send(f"{message.author.mention} is a fat neek and leveled up to level **{level}**")


bot.run(TOKEN)