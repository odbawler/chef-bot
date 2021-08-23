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

async def lookup_meal(foods):
    # TODO: Move this outside of code
    meals = {'Funghi Crema': ['pasta', 'leek', 'mushroom', 'garlic', 'stock', 'cashew', 'cream',
                'tarragon'],
        'Spag Bol': ['spaghetti', 'carrot', 'mince', 'tomato', 'tomato puree', 'mushroom',
            'pepper', 'onion', 'garlic', 'cheddar', 'cheese', 'stock']}
    # Construct inital list of meals from dictionary keys
    matches = list(meals.keys())

    # Begin with full list of meals, remove if ingredient not in meal
    for key in meals.keys():
        for ingredient in foods:
            if not ingredient.lower() in meals[key]:
                matches.remove(key)

    #matches = list(dict.fromkeys(matches))
    #matches = str(list(dict.fromkeys(matches)))[1:-1]
    return matches

@bot.command(name='scran', pass_context=True, help='Responds with random recipe from the book')
async def scran(ctx, *, message):

    # Split message by comman and strip whitespace
    foods =  [x.strip() for x in message.split(',')]
    matched_scran = await lookup_meal(foods)

    response = matched_scran
    if not response:
        response = "There ain't no scran :("
    await ctx.send(response)

bot.run(TOKEN)