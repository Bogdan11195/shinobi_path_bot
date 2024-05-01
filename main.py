#import keep_alive
import discord
import json
from discord.ext import commands
import random
import re
import openai
import asyncio
import datetime

file = open('config.json', 'r')
config = json.load(file)

intents = discord.Intents.all()  # Создаем объект intents с нужными значениями
bot = commands.Bot(config['prefix'],
                   intents=intents)  # Передаем intents в конструктор бота

bot.remove_command('help')
@bot.command(name='help')
async def ping(ctx):
  await ctx.send(f"{ctx.author.mention} \n **!try** - определить успех действия.\n\
**!roll AdB**(+C)(-D) - бросить кубик в диапазоне от 'A' до 'B', с возможными дополнительными параметрами '+', '-' по желанию.\n \n\
  А также ежедневное обновление погодных условий в <#1087032104438743180>, на базе искусственного интеллекта!")


@bot.command(name='try')
async def try1(ctx):
  # Генерируем случайное число от 0 до 1
  chance = random.randint(0, 1)
  # Если число равно 0, то отправляем сообщение "Удача"
  if chance == 0:
    await ctx.send(f'{ctx.author.mention}, **Неудача** !')
  # Если число равно 1, то отправляем сообщение "Неудача"
  else:
    await ctx.send(f'{ctx.author.mention}, **Удача** !')


@bot.command(name='roll')
async def roll(ctx, arg=None):
  if arg is None:
    arg = '1d100'
  match = re.match(r'(\d+)d(\d+)(.*)', arg)
  if match:
    start = int(match.group(1))
    end = int(match.group(2))
    modifiers = match.group(3)
    result = random.randint(start, end)
    total = result
    for modifier in re.findall(r'[\+\-]\d+', modifiers):
      if modifier[0] == '+':
        result += int(modifier[1:])
      else:
        result -= int(modifier[1:])
    await ctx.send(
      f"{ctx.author.mention} Запрос: `[{arg}]` | Чистый: `[{total}]` | Результат: **`{result}`**"
    )
  else:
    await ctx.send(
      "Неверный формат команды. Пожалуйста, используйте формат !roll AdB(+C)(-D)."
    )


# ID канала, в который будут отправляться сообщения
CHANNEL_ID = 1092664966919753748

openai.api_key = config['token_openai']

async def generate_weather_description():
  # Запрос на генерацию описания погоды с помощью GPT-3 API
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=
    'Сгенерируй разное описание текущей погоды в Стране Огня и Стране Воды из вселенной Наруто. Взаимоисключающие варианты: ясная погода/дождь/снег/гроза/туман. \n Форма:\n **Страна Огня:**\n **Страна Воды:**',
    temperature=0.8,
    max_tokens=512,
    top_p=0.6,
    frequency_penalty=0.2,
    presence_penalty=0.3,
    stop=["\"\"\""])

  # Отправка сгенерированного текста в текстовый канал Discord
  description = response.choices[0].text.strip()
  channel = bot.get_channel(CHANNEL_ID)

  embed = discord.Embed(color=0x7dff8a, title="Текущие погодные условия!")
  # Добавляем описание
  embed.description = f'{description}\n \n**Зависимость баффов/дебаффов от погоды:**\n Ясная погода: ничего.\n\
Дождь: +5 к Суитону.\n\
Снег: +5 к Хьетону.\n\
Гроза: +5 к Райтону, +5 к Суитону. -5 на использование коммуникатора (вызов подмоги).\n\
Песчаная буря: +5 к Фуутону.\n\
Туман: +5 к Футтону, +5 к побегу.'

  # Добавляем изображение
  embed.set_thumbnail(
    url=
    "https://cdn.discordapp.com/attachments/966084292071546952/1092267716636852314/90e9169b-a689-40fe-810d-265b823b1112.png"
  )
  # Отправляем embed сообщение в канал

  last_message = None # Инициализируем переменную для последнего сообщения
  async for message in channel.history(limit=1): # Перебираем сообщения в канале
      last_message = message # Присваиваем последнее сообщение переменной
  if last_message and last_message.author == bot.user: # Если последнее сообщение - сообщение бота
      await last_message.delete() # Удаляем его
  await channel.send(content='', embed=embed) # Отправляем новое сообщение с погодой


@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="!help - by @otto"))
  print('Bot is ready!')

  # Определяем желаемое время отправки сообщения
  send_time = datetime.time(5, 59, 0)  # 09:00:00 UTC

  while True:
    # Определяем текущее время
    current_time = datetime.datetime.utcnow().time()

    # Определяем разницу во времени между желаемым временем отправки сообщения и текущим временем
    time_diff = datetime.datetime.combine(
      datetime.date.today(), send_time) - datetime.datetime.combine(
        datetime.date.today(), current_time)

    # Если текущее время более позднее, чем желаемое время отправки сообщения, то ждем до следующего дня
    if time_diff.days < 0:
      time_diff = datetime.timedelta(days=1) + time_diff

    # Ожидаем до желаемого времени отправки сообщения
    await asyncio.sleep(time_diff.total_seconds())

    # Генерируем описание погоды
    await generate_weather_description()


#keep_alive.keep_alive()
bot.run(config['token'])
