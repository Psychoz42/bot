import discord
import requests
import json
from discord.ext import commands

logFileName = 'logs.txt'

config = {
    'token': str(input('Enter bot token: ')),
    'prefix': '%',
}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

temperature = 0.3
haveRole = 0
role = ''
message = ''

url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Api-Key AQVN3GWCoJiQ5pIapxWFsNoYfxaZFG_7hMixqjOj"
}

@bot.command()
async def repl(ctx, *args):
    await ctx.reply(' '.join([i for i in args]))

@bot.command()
async def instruction(ctx):
    await ctx.reply(("Все команды:\n"
               "repl - просто копирует сообщение в ответе\n"
               "tempSet - устанавливает температуру для GPT (от 0 до 1 с точкой а не запятой (делитель между целой и дробной частью))\n"
               "tempGet - выводит температуру\n"
               "haveRoleSet - выставляет использование роли GPT (0- не используется, 1 - используется)\n"
               "haveRoleGet - выводит текущее использование роли GPT (0- не используется, 1 - используется)\n"
               "roleSet - выставляет роль GPT\n"
               "roleGet - выдаёт роль GPT\n"
               "GPTStatus - выдаёт все параметры GPT\n"
               "setDefaultSettings - устанавливает все настройки в базовое состояние\n"
               "ask - сам запрос к нейросети"))

@bot.command()
async def tempSet(ctx, temp):
    global temperature
    temperature = float(temp)
    await ctx.reply('Выполнено')

@bot.command()
async def tempGet(ctx):
    await ctx.reply(temperature)

@bot.command()
async def haveRoleSet(ctx, val):
    try:
        if int(val) == 0 or int(val) == 1:
             global haveRole
             haveRole = int(val)
             await ctx.reply('Выполнено')
        else:
            await ctx.reply('Ошибка, доступные значения только 0 и 1')
    except:
        await ctx.reply('Ошибка, доступные значения только 0 и 1')

@bot.command()
async def haveRoleGet(ctx):
    await ctx.reply(haveRole)

@bot.command()
async def roleSet(ctx, *args):
    global role
    role = ' '.join(args)
    await ctx.reply('Выполнено')

@bot.command()
async def roleGet(ctx):
    await ctx.reply(role)

@bot.command()
async def GPTStatus(ctx):
    await ctx.reply(f'Have role: {haveRole} \nRole: {role} \nTemperature: {temperature}')

@bot.command()
async def setDefaultSettings(ctx):
    global temperature
    global haveRole
    global  role
    temperature = 0.3
    haveRole = 0
    role = ''
    await ctx.reply('Выполнено')

@bot.command()
async def ask(ctx, *args):
    global message
    global temperature
    global role
    global haveRole
    message = ' '.join(args)

    if haveRole == 1:
        prompt = {
            "modelUri": "gpt://b1g6tp8knm159fqb0l8m/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": temperature,
                "maxTokens": "1000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": role
                },
                {
                    "role": "user",
                    "text": message
                }
            ]
        }
    else:
        prompt = {
            "modelUri": "gpt://b1g6tp8knm159fqb0l8m/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": temperature,
                "maxTokens": "1000"
            },
            "messages": [
                {
                    "role": "user",
                    "text": message
                }
            ]
        }
    response = requests.post(url, headers=headers, json=prompt)
    result = json.loads(response.text).get('result').get('alternatives')[0].get('message').get('text')
    with open(logFileName, 'a') as logFile:
        logFile.write(f"--------------------\npromt = {message}\ntemp = {temperature}\nhave role = {haveRole}\nrole = {role}\nuser = {ctx.author}\nresult = {result}\n")
    await ctx.reply(result)

bot.run(config['token'])