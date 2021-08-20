################################################################################
#################################### IMPORTS ###################################
################################################################################
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

################################################################################
#################################### GLOBALS ###################################
################################################################################
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

################################################################################
################################### FUNCTIONS ##################################
################################################################################

@bot.event
async def on_ready():
    print(f'{bot.user.name} started!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Ma boi, {member.name}! You have entered the kitchen.'
    )

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.command(name='recipe', help='Responds with random recipe from the book')
async def recipe(ctx):
    recipes = [
        'Funghi Crema',
        'Spag Bol',
    ]

    response = random.choice(recipes)
    await ctx.send(response)

bot.run(TOKEN)