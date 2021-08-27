################################################################################
#################################### IMPORTS ###################################
################################################################################
import os
import random
import yaml
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
    meals = {"Funghi Crema": ['pasta', 'leek', 'mushroom', 'garlic', 'stock', 'cashew', 'cream',
                'tarragon'],
            "Spag Bol": ['spaghetti', 'carrot', 'mince', 'tomato', 'tomato puree', 'mushroom',
                'pepper', 'onion', 'garlic', 'cheddar', 'cheese', 'stock'],
            "Greens Mac 'n' Cheese": ['leek', 'garlic', 'brocolli', 'butter', 'flour', 'milk', 
                'macaroni', 'parmesan', 'cheddar', 'cheese', 'spinach', 'almonds']}
    # Construct inital list of meals from dictionary keys
    matches = list(meals.keys())

    # Begin with full list of meals, remove if ingredient not in meal
    for key in meals.keys():
        for ingredient in foods:
            if not ingredient.lower() in meals[key]:
                matches.remove(key)

    #matches = list(dict.fromkeys(matches))
    #matches = str(list(dict.fromkeys(matches)))[1:-1]
    return str(matches)[1:-1]

async def lookup_recipe(recipe):
    # for key, value in yaml.load(open('recipes.yaml'))['recipes'].iteritems():
    #     print key, value
    # with open("recipes.yaml", 'r') as stream:
    #     content = yaml.load(stream)
    #     for k,v in content.items():
    #         if recipe in k:
    #             return str(v)[1:-1]

    for k, v in yaml.load(open('recipes.yaml'), yaml.FullLoader)["recipes"]:
        if recipe in k:
            print(str(v["Ingredients"])[1:-1])
            return v["Ingredients"], v["Method"]

@bot.command(name='scran', pass_context=True, help='Responds with matching meals ideas based on supplied ingredients')
async def scran(ctx, *, message):

    # Split message by comman and strip whitespace
    foods =  [x.strip() for x in message.split(',')]
    matched_scran = await lookup_meal(foods)

    response = matched_scran
    if not response:
        response = "There ain't no scran :("
    await ctx.send(response)

@bot.command(name='recipe', pass_context=True, help='Responds with the recipe for the selected meal')
async def recipe(ctx, *, message):

    print(message.strip())
    recipe = await lookup_recipe(message.strip())

    response = "```" + recipe["Ingredients"] + recipe["Method"] + "```"
    if not response:
        response = "We don't do that here >:|"
    await ctx.send(response)

bot.run(TOKEN)