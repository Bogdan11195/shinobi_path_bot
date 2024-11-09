#import keep_alive
import discord
import json
import random
import re
import openai
import asyncio
import datetime
import calendar
from discord.ext import commands

file = open('config.json', 'r')
config = json.load(file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

# Удаляем стандартную команду help
bot.remove_command('help')

@bot.command(name='help')
async def ping(ctx):
    await ctx.send(f"{ctx.author.mention} \n **!try** - определить успех действия.\n\
**!roll AdB**(+-C) — бросок кубика. **A** — мин. число, **B** — макс. число кубика. Можно добавить + или - значение, чтобы скорректировать результат.\n\
        Например, **/roll 1d100**+15-5 — бросает кубик от 1 до 100, добавляет 15 и отнимает 5 от результата.\n\
        Формат **/roll 100**+20-10, без использования '**d**' так же считается корректным.\n \n\
  А также ежедневное обновление погодных условий в <#1046143004366340216>, на базе искусственного интеллекта!")

# Создание слэш-команды для "help"
@bot.tree.command(name="help", description="Что может этот бот?")
async def help_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} \n **/try** - определить успех действия.\n\
**/roll AdB**(+-C) — бросок кубика. **A** — мин. число, **B** — макс. число кубика. Можно добавить + или - значение, чтобы скорректировать результат.\n\
        Например, **/roll 1d100**+15-5 — бросает кубик от 1 до 100, добавляет 15 и отнимает 5 от результата.\n\
        Формат **/roll 100**+20-10, без использования '**d**' так же считается корректным.\n \n\
  А также ежедневное обновление погодных условий в <#1046143004366340216>, на базе искусственного интеллекта!")

@bot.command(name='try')
async def try1(ctx):
    chance = random.randint(0, 1)
    if chance == 0:
        await ctx.send(f'{ctx.author.mention}, **Неудача** !')
    else:
        await ctx.send(f'{ctx.author.mention}, **Удача** !')


# Создание слэш-команды для "try"
@bot.tree.command(name="try", description="Определить успех действия")
async def try_slash(interaction: discord.Interaction):
    chance = random.randint(0, 1)
    result = "Неудача" if chance == 0 else "Удача"
    await interaction.response.send_message(f'{interaction.user.mention}, **{result}**!')


@bot.command(name='roll')
async def roll(ctx, arg=None):
    if arg is None:
        arg = '1d100'
    
    # Проверяем, если аргумент — это просто число с возможными модификаторами
    match = re.match(r'^(\d+)([\+\-]\d+)*$', arg)
    if match:
        start = 1
        end = int(match.group(1))
        modifiers = arg[len(match.group(1)):]  # Извлекаем модификаторы после числа
        result = random.randint(start, end)
        total = result
        
        # Применяем модификаторы
        for modifier in re.findall(r'[\+\-]\d+', modifiers):
            if modifier[0] == '+':
                result += int(modifier[1:])
            else:
                result -= int(modifier[1:])
        
        await ctx.send(
            f"{ctx.author.mention} Запрос: `[1d{end}{modifiers}]` | Чистый: `[{total}]` | Результат: **`{result}`**"
        )
    else:
        # Если аргумент в формате AdB(+/-X)
        match = re.match(r'(\d+)d(\d+)(.*)', arg)
        if match:
            start = int(match.group(1))
            end = int(match.group(2))
            modifiers = match.group(3)
            result = random.randint(start, end)
            total = result
            
            # Применяем модификаторы
            for modifier in re.findall(r'[\+\-]\d+', modifiers):
                if modifier[0] == '+':
                    result += int(modifier[1:])
                else:
                    result -= int(modifier[1:])
            
            await ctx.send(
                f"{ctx.author.mention} Запрос: `[{arg}]` | Чистый: `[{total}]` | Результат: **`{result}`**"
            )
        else:
            await ctx.send("Неверный формат команды. Пожалуйста, используйте формат описанный в ***!help***.")


# Создание слэш-команды для "roll"
@bot.tree.command(name="roll", description="1d100+15-5 — число от 1 до 100, +15 и -5 от результата. Значения можно изменять. 'd' - не обязателен")
async def roll_slash(interaction: discord.Interaction, message: str):
    # Проверяем, если аргумент — это просто число с возможными модификаторами
    match = re.match(r'^(\d+)([\+\-]\d+)*$', message)
    if match:
        start = 1
        end = int(match.group(1))
        modifiers = message[len(match.group(1)):]  # Извлекаем модификаторы после числа
        result = random.randint(start, end)
        total = result
        
        # Применяем модификаторы
        for modifier in re.findall(r'[\+\-]\d+', modifiers):
            if modifier[0] == '+':
                result += int(modifier[1:])
            else:
                result -= int(modifier[1:])
        
        await interaction.response.send_message(
            f"{interaction.user.mention} Запрос: `[1d{end}{modifiers}]` | Чистый: `[{total}]` | Результат: **`{result}`**"
        )
    else:
        # Если аргумент в формате AdB(+/-X)
        match = re.match(r'(\d+)d(\d+)(.*)', message)
        if match:
            start = int(match.group(1))
            end = int(match.group(2))
            modifiers = match.group(3)
            result = random.randint(start, end)
            total = result
            
            # Применяем модификаторы
            for modifier in re.findall(r'[\+\-]\d+', modifiers):
                if modifier[0] == '+':
                    result += int(modifier[1:])
                else:
                    result -= int(modifier[1:])
            
            await interaction.response.send_message(
                f"{interaction.user.mention} Запрос: `[{message}]` | Чистый: `[{total}]` | Результат: **`{result}`**"
            )
        else:
            await interaction.response.send_message("Неверный формат команды. Пожалуйста, используйте формат описанный в ***/help***.")



# ID канала, в который будут отправляться сообщения
CHANNEL_ID = 1046143004366340216

openai.api_key = config['token_openai']

async def generate_weather_description():
    # Получаем текущий месяц и преобразуем его в название на русском языке
    current_month = datetime.datetime.now().month
    current_month_ru = calendar.month_name[current_month]
  
    # Запрос на генерацию описания погоды с помощью GPT-4 API
    response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": f"Для каждой локации случайно выбери только один погодный статус(ясная погода, дождь, снег, гроза, туман, песчаная буря). Учитывай сезонные особенности текущего месяца - {current_month_ru}. Сгенерируй красочное описание текущей погоды в Стране Огня, Стране Воды, Стране Ветра и Нейтральных локаций, для вселенной Наруто. Иногда случайность погоды важнее логики. Форма:\n **Страна Огня:** <Статус>. <Описание погоды>.\n **Страна Воды:** <Статус>. <Описание погоды>.\n **Страна Ветра:** <Статус>. <Описание погоды>.\n **Нейтральные локации:** <Статус>. <Описание погоды>."
        }
    ],
    temperature=0.8,
    top_p=1.0,
    max_tokens=370,
    frequency_penalty=0.2,
    presence_penalty=0.3)

    # Отправка сгенерированного текста в текстовый канал Discord
    description = response.choices[0].message.content.strip()
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
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="/help - by Oi Nagasaki!"))
    print('Bot is ready!')

    # Определяем желаемое время отправки сообщения
    send_time = datetime.time(3, 0, 0)  # 09:00:00 UTC

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
        
        # Синхронизация команд на сервере при запуске
        await bot.tree.sync()


#keep_alive.keep_alive()
bot.run(config['token'])
