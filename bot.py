import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View, UserSelect, Select
import random
import asyncio
from datetime import datetime, timedelta
import json
import os

intents = discord.Intents.all()

TOKEN = ''

def check_inventory_file():
    try:
        with open("obsdata.json", "r") as file:
            pass
    except FileNotFoundError:
        with open("obsdata.json", "w") as file:
            json.dump({}, file, ensure_ascii=False)

def load_data():
    with open("obsdata.json", "r") as file:
        return json.load(file)
    
def save_data(data):
    with open("obsdata.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    

def check_item(user, item):
    user_id = str(user.name)
    data = load_data()
    if user_id in data and item in data[user_id]["items"]:
        return True
    else:
        return False

def number_item(user, item):
    user_id = str(user.name)
    data = load_data()
    counter = 0
    if user_id in data:
        for dataitem in data[user_id]["items"]:
            if dataitem == item:
                counter+=1
    return counter
    
      
def manage_item(user, item, action):
    user_id = str(user.name)
    data = load_data()
    if user_id not in data:
        data[user_id] = {"items": [], "SP": 50}
    match action:
        case 'add':
            data[user_id]["items"].append(item)
        case 'remove':
            data[user_id]["items"].remove(item)
    save_data(data)

def check_SP(user):
    user_id = str(user.name)
    data = load_data()
    if user_id not in data:
        data[user_id] = {"items": [], "SP": 50}
    SP = data.get(user_id, {}).get("SP", 0)
    return SP

def set_SP(user, amount):
    user_id = str(user.name)
    data = load_data()
    if user_id not in data:
        data[user_id] = {"items": [], "SP": 50}
    data[user_id]["SP"] = amount
    save_data(data)

# ЦВЕТА
red = 0xff0000
yellow = 0xFEE75C
green = 0x287e29
discordcolor = 0x7289da

moderator_list = ['sweetyhake']

peace = False

placeholder = discord.Embed(title='Placeholder',description='',color=yellow)

# РОЛИ
ROLE0ID = 526308268260458496 # МАСТЕР
ROLE1ID = 1174039269065625610 # АСПЕКТ
ROLE2ID = 1186637073369804891 # БЕХОЛДЕР
ROLE3ID = 1186637174234435664 # ИЛЛИТИД
ROLE4ID = 1174038780492136508 # РЫЦАРЬ
ROLE5ID = 1174038673914875946 # ГРИФОН
ROLE6ID = 1174037749683191849 # АВАНТЮРИСТ
ROLE7ID = 1186637285446393886 # ЖЕЛАТИНОВЫЙ КУБ
ROLE8ID = 1174036560707080213 # ГОБЛИН


async def shop (interaction):
        embed = discord.Embed(title='Seventh Shop',description='Покупайте предметы, а затем используйте их из инвентаря.',color=discordcolor)
        embed.add_field(name=f'', inline=False, value=f'📃 **Кусочек тетради смерти**\nПозволяет записать одного пользователя на кусочек тетради смерти.\nСтоимость: 200 SP.')
        embed.add_field(name=f'', inline=False, value=f'🤫 **Немота**.\nПозволяет замутить одного пользователя.\nСтоимость: 20 SP.')
        embed.add_field(name=f'', inline=False, value=f'🗣️ **Слово пацана**.\nПозволяет размутить одного пользователя (в том числе и себя).\nСтоимость: 10 SP.')
        embed.add_field(name=f'', inline=False, value=f'🛡️ **Щит**.\nПассивно: защищает от одного следующего опасного предмета.\nСтоимость: 50 SP.')
        embed.add_field(name=f'', inline=False, value=f'⚔️ **Парирование**.\nПассивно: отражает следующий опасный предмет в использовавшего его.\nСтоимость: 100 SP.')
        embed.add_field(name=f'', inline=False, value=f'🕊️ **Перемирие**.\nПозволяет отключить использование опасных предметов на час.\nСтоимость: 400 SP.')
        
        buttonmanager = View(timeout=None)
        DeathNote = Button(label='', emoji='📃',style=discord.ButtonStyle.secondary)
        Silence = Button(label='', emoji='🤫',style=discord.ButtonStyle.secondary)
        Lev = Button(label='', emoji='🗣️',style=discord.ButtonStyle.secondary)
        Shield = Button(label='', emoji='🛡️',style=discord.ButtonStyle.secondary)
        Parry = Button(label='', emoji='⚔️',style=discord.ButtonStyle.secondary)
        Peace = Button(label='', emoji='🕊️',style=discord.ButtonStyle.secondary)

        async def buttonbuy(interaction, item, price):
            if check_SP(interaction.user) >= price:
                set_SP(interaction.user, check_SP(interaction.user) - price )
                manage_item(interaction.user, item, 'add')
                embed = discord.Embed(title='Seventh Shop',description=f'Вы успешно приобрели {item}.',color=green)
                await interaction.response.send_message(embed=embed, ephemeral = True)
            else:
                embed = discord.Embed(title='Seventh Shop',description=f'У вас недостаточно SP для приобретения {item}.',color=red)
                await interaction.response.send_message(embed=embed, ephemeral = True)
        async def DeathNoteCallback(interaction:discord.Interaction):
            await buttonbuy(interaction, 'Кусочек тетради смерти', 200)
        async def SilenceCallback(interaction:discord.Interaction):
            await buttonbuy(interaction, 'Немота', 20)
        async def LevCallback(interaction:discord.Interaction):
            await buttonbuy(interaction, 'Слово пацана', 10)
        async def ShieldCallback(interaction:discord.Interaction):
            await buttonbuy(interaction, 'Щит', 50)
        async def ParryCallback(interaction:discord.Interaction):
            await buttonbuy(interaction, 'Парирование', 100)
        async def PeaceCallback(interaction:discord.Interaction):
            await buttonbuy(interaction, 'Перемирие', 400)


        DeathNote.callback = DeathNoteCallback
        Silence.callback = SilenceCallback
        Lev.callback = LevCallback
        Shield.callback = ShieldCallback
        Parry.callback = ParryCallback
        Peace.callback = PeaceCallback

        buttonmanager.add_item(DeathNote)
        buttonmanager.add_item(Silence)
        buttonmanager.add_item(Lev)
        buttonmanager.add_item(Shield)
        buttonmanager.add_item(Parry)
        buttonmanager.add_item(Peace)

        await interaction.response.send_message(embed=embed,view=buttonmanager, ephemeral=True)

async def inventory(interaction):
        embed = discord.Embed(title='Инвентарь',description='Используйте предметы, купленные в магазине.',color=discordcolor)
        embed.add_field(name=f'', inline=False, value=f'📃 **Кусочек тетради смерти**\nПозволяет записать одного пользователя на кусочек тетради смерти.\nУ вас: {number_item(interaction.user, 'Кусочек тетради смерти')}.')
        embed.add_field(name=f'', inline=False, value=f'🤫 **Немота**.\nПозволяет замутить одного пользователя.\nУ вас: {number_item(interaction.user, 'Немота')}.')
        embed.add_field(name=f'', inline=False, value=f'🗣️ **Слово пацана**.\nПозволяет размутить одного пользователя (в том числе и себя).\nУ вас: {number_item(interaction.user, 'Слово пацана')}.')
        embed.add_field(name=f'', inline=False, value=f'🛡️ **Щит**.\nПассивно: защищает от одного следующего опасного предмета.\nУ вас: {number_item(interaction.user, 'Щит')}.')
        embed.add_field(name=f'', inline=False, value=f'⚔️ **Парирование**.\nПассивно: отражает следующий опасный предмет в использовавшего его.\nУ вас: {number_item(interaction.user, 'Парирование')}.')
        embed.add_field(name=f'', inline=False, value=f'🕊️ **Перемирие**.\nПозволяет отключить использование опасных предметов на час.\nУ вас: {number_item(interaction.user, 'Перемирие')}.')
        
        embedfalse = discord.Embed(title='Инвентарь',description=f'У вас нет этого предмета.',color=red)
        peaceembed = discord.Embed(title='Перемирие',description=f'На данный момент на сервере объявлено перемирие.',color=green)
        buttonmanager = View(timeout=None)
        DeathNote = Button(label='', emoji='📃',style=discord.ButtonStyle.primary)
        Silence = Button(label='', emoji='🤫',style=discord.ButtonStyle.primary)
        Lev = Button(label='', emoji='🗣️',style=discord.ButtonStyle.primary)
        Shield = Button(label='', emoji='🛡️',style=discord.ButtonStyle.secondary)
        Parry = Button(label='', emoji='⚔️',style=discord.ButtonStyle.secondary)
        Peace = Button(label='', emoji='🕊️',style=discord.ButtonStyle.primary)
        mute_role = interaction.guild.get_role(1174411093670637660)
        async def DeathNoteCallback(interaction:discord.Interaction):
            if peace != True:
                if check_item(interaction.user, 'Кусочек тетради смерти'):
                    await interaction.response.send_modal(DeathNoteModal())
                else: await interaction.response.send_message(embed=embedfalse, ephemeral=True, delete_after=5)
            else: await interaction.response.send_message(embed=peaceembed, ephemeral=True)
        async def SilenceCallback(interaction:discord.Interaction):
            if peace != True:
                if check_item(interaction.user, 'Немота'):
                    select = discord.ui.UserSelect(
                        placeholder='Выберите пользователя',
                    )
                    async def select_callback(interaction: discord.Interaction):
                        for user in select.values:
                                tuser = user
                        if mute_role not in tuser.roles:
                            if check_item(tuser, 'Щит') or check_item(tuser, 'Парирование'):
                                if check_item(tuser, 'Парирование'):
                                    try:
                                        await interaction.user.add_roles(mute_role)
                                        current_channel = interaction.user.voice.channel
                                        afk_channel = bot.get_channel(776022980202987520)
                                        await interaction.user.move_to(afk_channel)
                                        await interaction.user.move_to(current_channel)    
                                    except Exception: pass
                                    manage_item(tuser, 'Парирование', 'remove')
                                else:
                                    manage_item(tuser, 'Щит', 'remove')
                            else:
                                try:
                                    await tuser.add_roles(mute_role)
                                    current_channel = tuser.voice.channel
                                    afk_channel = bot.get_channel(776022980202987520)
                                    await tuser.move_to(afk_channel)
                                    await tuser.move_to(current_channel)    
                                except Exception: pass
                            manage_item(interaction.user, 'Немота', 'remove')
                            embed = discord.Embed(title='Немота',description=f'Вы успешно наложили немоту на {tuser.display_name}.',color=green)
                        else:
                            embed = discord.Embed(title='Немота',description=f'{tuser.display_name} уже находится под действием немоты.',color=red)
                        await interaction.response.edit_message(embed=embed, view=None)
                    viewmanager = View()
                    select.callback = select_callback
                    viewmanager.add_item(select)
                    await interaction.response.send_message('', view=viewmanager, ephemeral=True)
                else: 
                    await interaction.response.send_message(embed=embedfalse, ephemeral=True)
            else: await interaction.response.send_message(embed=embedfalse, ephemeral=True)
        async def LevCallback(interaction:discord.Interaction):
            if peace != True:
                if check_item(interaction.user, 'Слово пацана'):
                    select = discord.ui.UserSelect(
                        placeholder='Выберите пользователя',
                    )
                    async def select_callback(interaction: discord.Interaction):
                        for user in select.values:
                            tuser = user
                        if mute_role in tuser.roles:
                            try:
                                await tuser.remove_roles(mute_role)
                                current_channel = tuser.voice.channel
                                afk_channel = bot.get_channel(776022980202987520)
                                await tuser.move_to(afk_channel)
                                await tuser.move_to(current_channel)    
                            except Exception: pass
                            embed = discord.Embed(title='Слово пацана',description=f'Вы успешно сняли немоту с {tuser.display_name}.',color=green)
                            manage_item(interaction.user, 'Слово пацана', 'remove')
                        else: 
                            embed = discord.Embed(title='Слово пацана',description=f'На {tuser.display_name} нет немоты.', color=red)
                        await interaction.response.edit_message(embed=embed, view=None)
                    viewmanager = View()
                    select.callback = select_callback
                    viewmanager.add_item(select)
                    await interaction.response.send_message('', view=viewmanager, ephemeral=True)
                else:  await interaction.response.send_message(embed=embedfalse)
            else: await interaction.response.send_message(embed=peaceembed, ephemeral=True)
        async def ShieldCallback(interaction:discord.Interaction):
            passive = discord.Embed(title='Щит', description='Этот предмет работает пассивно.', color=yellow)
            await interaction.response.send_message(embed=passive, ephemeral=True)
        async def ParryCallback(interaction:discord.Interaction):
            passive = discord.Embed(title='Парирование', description='Этот предмет работает пассивно.', color=yellow)
            await interaction.response.send_message(embed=passive, ephemeral=True)
        async def PeaceCallback(interaction:discord.Interaction):                   
            if peace != True:
                if check_item(interaction.user, 'Перемирие'):
                    peace = True
                    manage_item(interaction.user, 'Перемирие', 'remove')
                    embed = discord.Embed(title='Перемирие', description='Вы объявили перемирие на 1 час.', color=green)
                    await interaction.response.send_message(embed=embed)
                else: await interaction.response.send_message(embed=embedfalse, ephemeral=True)
            else:
                    embed = discord.Embed(title='Перемирие', description='Перемирие уже объявлено.', color=red)
                    await interaction.response.send_message(embed=embed)


        DeathNote.callback = DeathNoteCallback
        Silence.callback = SilenceCallback
        Lev.callback = LevCallback
        Shield.callback = ShieldCallback
        Parry.callback = ParryCallback
        Peace.callback = PeaceCallback

        buttonmanager.add_item(DeathNote)
        buttonmanager.add_item(Silence)
        buttonmanager.add_item(Lev)
        buttonmanager.add_item(Shield)
        buttonmanager.add_item(Parry)
        buttonmanager.add_item(Peace)

        await interaction.response.send_message(embed=embed,view=buttonmanager, ephemeral=True)
class Cf(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label='Правила',emoji='📑',style=discord.ButtonStyle.primary, custom_id='rules')
    async def rules(self, interaction:discord.Interaction, Button: discord.ui.Button):
        embed = discord.Embed(title='Правила',description='',color=discordcolor)
        embed.add_field(name='Общие положения', inline=False, value='Все участники сервера несут одинаковую ответственность за нарушение описанных ниже пунктов вне зависимости от их роли на сервере.\nЗапрещено публичное и слишком жестокое оскорбление других пользователей (степень определяется голосованием).\nЗапрещены любые виды флуда.\nПредставителям модерации (роли Аспект и Бехолдер) запрещено злоупотреблять своими правами и заниматься самоуправством.')
        embed.add_field(name='Голосовые каналы', inline=False,value='Запрещено включать музыку через микрофон (используйте бота или Youtube Together).\nЗапрещено злоупотребление громкими звуками через микрофон (крики, неприятные звуки и т.д.).\nПри наличии посторонних шумов крайне рекомендуется использовать функцию шумоподавления или функцию Push-to-Talk.')
        embed.add_field(name='Профиль пользователя', inline=False,value='Администратор вправе требовать изменение ника и картинки, если считает, что они оскорбляют кого-либо.')
        embed.add_field(name='Голосования', inline=False, value='Во избежание недопониманий все спорные ситуации следует решать через голосования.\nПри начале голосования требуется объективная причина, отражающая смысл голосования.')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    @discord.ui.button(label='Цвет',style=discord.ButtonStyle.primary, emoji='🎨',custom_id='color')
    async def pcolor(self, interaction:discord.Interaction, Button: discord.ui.Button):
        await color(interaction=interaction)
    @discord.ui.button(label='Иконка',style=discord.ButtonStyle.primary, emoji='🥸' , custom_id='icon')
    async def picon(self, interaction:discord.Interaction, Button: discord.ui.Button):
        await icon(interaction=interaction)
    @discord.ui.button(label='Команды',emoji='❓',style=discord.ButtonStyle.primary, custom_id='commands')
    async def commandlist(self, interaction:discord.Interaction, Button: discord.ui.Button):
        embed = discord.Embed(title='Команды',description='',color=discordcolor)
        embed.add_field(name='/комната', inline=False, value='Позволяет создать временный голосовой канал. Используйте команду **/пригласить**, чтобы дать доступ к приватным каналам своим друзьям. Канал уничтожается, когда все пользователи покидают его.')
        embed.add_field(name='/кость', inline=False,value='Позволяет бросить игральную кость различных чисел.')
        embed.add_field(name='/голосование', inline=False,value='Позволяет инициировать голосование в канале #голосования. Используется для повышений/понижений, мута, тайм-аута и даже кика с баном.')
        embed.add_field(name='/русскаярулетка', inline=False, value='Сыграйте в смертельную игру один, или со своими друзьями. Проигравших ждёт наказание, выбранное при создании игры.')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    @discord.ui.button(label='Роли',emoji='📶',style=discord.ButtonStyle.primary, custom_id='roles')
    async def roleslist(self, interaction:discord.Interaction, Button: discord.ui.Button):
        Мастер = interaction.guild.get_role(ROLE0ID)
        Аспект = interaction.guild.get_role(ROLE1ID)
        Бехолдер = interaction.guild.get_role(ROLE2ID)
        Иллитид = interaction.guild.get_role(ROLE3ID)
        Рыцарь = interaction.guild.get_role(ROLE4ID)
        Грифон = interaction.guild.get_role(ROLE5ID)
        Авантюрист = interaction.guild.get_role(ROLE6ID)
        ЖКуб = interaction.guild.get_role(ROLE7ID)
        Гоблин = interaction.guild.get_role(ROLE8ID)

        embed = discord.Embed(title='Доступные роли',description='Роли расположены в порядке уменьшения сверху вниз. Перемещение между ними происходит с помощью голосования.',color=discordcolor)

        embed.add_field(name=f'', inline=False, value=f'{Мастер.mention}\nВысшая роль, обладающая правами администратора. Доступна лишь одному человеку на сервере, и, как я слышал, он еще никогда не менялся.')
        embed.add_field(name=f'', inline=False, value=f'{Аспект.mention}\nРоль, практически достигшая божественности и получившая некоторые админские силы. Обладание такой силой не менее большая ответственность.')
        embed.add_field(name=f'', inline=False,value=f'{Бехолдер.mention}\nВы близки к верхушке. Внутри вас начинают проявляться админские силы.')
        embed.add_field(name=f'', inline=False,value=f'{Иллитид.mention}\nВы особая личность. Как метафорически, так и физически.')
        embed.add_field(name=f'', inline=False, value=f'{Рыцарь.mention}\nВы проявили себя достойным членом общества. Вас уважают даже те, кто стоит над вами.')
        embed.add_field(name=f'', inline=False, value=f'{Грифон.mention}\nНебольшой шаг по карьерной лестнице, но ваши права все еще уступают вышестоящим.')
        embed.add_field(name=f'', inline=False, value=f'{Авантюрист.mention}\nСтартовая роль любого пользователя.')
        embed.add_field(name=f'', inline=False, value=f'{ЖКуб.mention}\nВидимо существования в облике человека вам наскучило, поэтому вы решили стать опасным монстром. Не ожидайте, что к вам будут относиться также, как и раньше.')
        embed.add_field(name=f'', inline=False, value=f'{Гоблин.mention}\nPathetic.')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    @discord.ui.button(label='Баланс',style=discord.ButtonStyle.primary, emoji='ℹ️', custom_id='balance' )
    async def balance(self, interaction:discord.Interaction, Button:discord.ui.Button):
        embed = discord.Embed(title='Seventh Bank',description=f'Ваш баланс: {check_SP(interaction.user)} Seventh Points.',color=discordcolor)
        await interaction.response.send_message('', embed=embed, ephemeral=True)
    @discord.ui.button(label='Магазин',style=discord.ButtonStyle.primary, emoji='🛒', custom_id='shop' )
    async def shopcall(self, interaction:discord.Interaction, Button:discord.ui.Button):
        await shop(interaction)
    @discord.ui.button(label='Инвентарь',style=discord.ButtonStyle.primary, emoji='🧰', custom_id='inventory' )
    async def inventorycall(self, interaction:discord.Interaction, Button:discord.ui.Button):
        await inventory(interaction)
    @discord.ui.button(label='Рулетка',style=discord.ButtonStyle.primary, emoji='🎰', custom_id='spin' )
    async def spin(self, interaction:discord.Interaction, Button:discord.ui.Button):
        embed = discord.Embed(title='В разработке',description='',color=red)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    @discord.ui.button(label='Донат',style=discord.ButtonStyle.red, emoji='💲', custom_id='donation', disabled=True )
    async def donation(self, interaction:discord.Interaction, Button:discord.ui.Button):
        return
    
class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix=commands.when_mentioned_or('!'),intents=intents)
    async def setup_hook(self) -> None:
        self.add_view(Cf())

bot = PersistentViewBot()

@bot.tree.command(name="предмет", description='Предметы')
@app_commands.choices(действие=[
    app_commands.Choice(name="Выдать", value='add'),
    app_commands.Choice(name="Проверить", value='check'),
    app_commands.Choice(name="Удалить", value='remove'),
    ])
async def items(interaction:discord.Interaction, действие: app_commands.Choice[str], item_name: str):
    if interaction.user.guild_permissions.administrator or interaction.user.name in moderator_list:
      match действие.value:
        case 'add':
            manage_item(interaction.user, item_name, 'add')
            await interaction.response.send_message(f"{item_name} добавлен в инвентарь.", ephemeral=True)
        case 'check':
            if check_item(interaction.user, item_name) == True:
                await interaction.response.send_message(f"{item_name} есть у вас в инвентаре.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{item_name} нет у вас в инвентаре.", ephemeral=True)
        case 'remove':
            manage_item(interaction.user, item_name, 'remove')
            await interaction.response.send_message(f"{item_name} убран из инвентаря.", ephemeral=True)
    else: await interaction.response.send_message(f"Недостаточно прав для выполнения этой команды.", ephemeral=True)

class DeathNoteModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Кусочек тетради смерти")
        today = datetime.today()

        self.name = discord.ui.TextInput(
            label="Имя [В дискорде, а не на сервере]",
            placeholder=f"scowpio",
            style=discord.TextStyle.short,
        )
        self.date = discord.ui.TextInput(
            label="Дата смерти [Как в примере / Необязательно]",
            placeholder=f"{today.day}.{today.month}.{today.year} {today.hour}:{today.minute+1}",
            style=discord.TextStyle.short,
            required=False,
        )
        self.reason = discord.ui.TextInput(
            label="Причина смерти [Необязательно]",
            placeholder="Разорвало жопу от горохового супа",
            style=discord.TextStyle.long,       
            required=False,     
        )

        self.add_item(self.name)
        self.add_item(self.date)
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):
        # Обработка введенных данных
        manage_item(interaction.user, 'Кусочек тетради смерти', 'remove')
        datetext = self.date.value
        if self.reason.value == '': reason = 'Остановка сердца'
        else: reason = self.reason.value
        try:
            date = datetime.strptime(datetext, "%d.%m.%Y %H:%M")
            datevalue = int(date.timestamp())
            temp = datetime.now()
            temp = int(temp.timestamp())
            
        except Exception:
            date = datetime.now() + timedelta(seconds=40)
            datevalue = int(date.timestamp())
            temp = datetime.now()
            temp = int(temp.timestamp())

        embed = discord.Embed(title='Кусочек тетради смерти',description=f"Вы записали {self.name.value} в тетрадь смерти. Дата смерти: {date}, причина смерти: {reason}.",color=green)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        for member in interaction.guild.members:
            if member.name == self.name.value:
                target = member
                break
        
        await asyncio.sleep(datevalue - temp)

        if check_item(target, 'Щит') or check_item(target, 'Парирование'):
            if check_item(target, 'Парирование'):
                try:
                    manage_item(interaction.user, 'Парирование', 'remove')
                    await interaction.user.timeout(timedelta(seconds=60), reason=reason)
                    print (f"{interaction.user.name} убил сам себя, пытаясь убить {target.display_name}. Дата смерти: {date}, причина смерти: {reason}. Причина: Парировал атаку.")
                except Exception: pass
            else: 
                manage_item(interaction.user, 'Щит', 'remove')
                print (f"{target.display_name} не был убит {interaction.user.name}, который записал его в тетрадь смерти. Причина: Защитился щитом.")

        else:
            try: 
                await target.timeout(timedelta(seconds=60), reason=reason)
                print (f"{target.display_name} был убит {interaction.user.name}, который записал его в тетрадь смерти. Дата смерти: {date}, причина смерти: {reason}.")
            except Exception: print (f"{target.display_name} не был убит {interaction.user.name}, который записал его в тетрадь смерти. Причина: Ошибка.")

@bot.tree.command(name="sp", description='Seventh Points')
@app_commands.choices(действие=[
    app_commands.Choice(name="выдать", value='add'),
    app_commands.Choice(name="баланс", value='check'),
    app_commands.Choice(name="убрать", value='remove'),
    app_commands.Choice(name="установить", value='set')
    ])
async def SP(interaction:discord.Interaction, tuser: discord.User, действие: app_commands.Choice[str], value: int = 0):
    match действие.value:
        case 'add':
            set_SP(tuser, check_SP(tuser) + value)
            await interaction.response.send_message(f"На счет {tuser.display_name} было начислено {value} SP.", ephemeral=True)
        case 'check':
            await interaction.response.send_message(f"Баланс {tuser.display_name}: {check_SP(tuser)} SP.", ephemeral=True)
        case 'remove':
            set_SP(tuser, check_SP(tuser) - value)
            await interaction.response.send_message(f"С счета {tuser.display_name} было списано {value} SP.", ephemeral=True)

@bot.tree.command(name='test')
async def cf(interaction:discord.Interaction):
    if interaction.user.name == 'sweetyhake':
        embed = discord.Embed(title='Меню',description='Ознакомьтесь с правилами серверами, с доступными командами, а также поменяйте цвет своего никнейма или иконку перед ним. ',color=discordcolor)
        channel = await interaction.guild.fetch_channel(1004019014030348318)
        message = await channel.fetch_message(1221106464509263912)
        await message.delete()
        # await channel.send(content='', embed=embed, view=Cf(), silent=True)

# Создаем словарь для хранения голосов
votes = {}
roulette = {}
excluded_role_id = 1174107082044215366
votes_channel = 1174092147079778305
afk_channel = 1006141707705929870

# ТРЕШХОЛДЫ НАСТРОЙКИ
thresholds = {
    'мут': 1,
    'бан': 8,
    'кик': 7,
    'тайм-аут': 3,
    'повыс': 4,
    'пониж': 4
}

# МАССИВ ВРЕМЕННЫХ КАНАЛОВ
tempchannels = []


# ЗАЩИТА РОЛЕЙ
defence = {
 526308268260458496 : 5, 
 1174039269065625610 : 2.25, 
 1186637073369804891 : 2, 
 1186637174234435664 : 1.75, 
 1174038780492136508 : 1.5, 
 1174038673914875946 : 1.25, 
 1174037749683191849 : 1, 
 1186637285446393886 : 0.75, 
 1174036560707080213 : 0.5
}

roles = [526308268260458496, # 0
         1174039269065625610, # 1
         1186637073369804891, # 2
         1186637174234435664, # 3
         1174038780492136508, # 4
         1174038673914875946, # 5
         1174037749683191849, # 6
         1186637285446393886 , # 7
         1174036560707080213  # 8
         ]



@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    synced = len(synced)
    print(f'Ненавижу стрелять врагам в спину... {bot.user.name} в сети. Активировано {synced} команд.')
    check_inventory_file()

@bot.tree.command(name="кость", description='Позволяет совершить бросок игральной кости.')
@app_commands.choices(кость=[
    app_commands.Choice(name="D4", value=4),
    app_commands.Choice(name="D6", value=6),
    app_commands.Choice(name="D8", value=8),
    app_commands.Choice(name="D10", value=10),
    app_commands.Choice(name="D12", value=12),
    app_commands.Choice(name="D20", value=20),
    app_commands.Choice(name="D100", value=100),
    ])
@app_commands.describe(кость='Кость.' )
async def dice(interaction:discord.Interaction, кость: app_commands.Choice[int]):
    result = random.randint(1,кость.value)
    title = 'Выпавшее значение: **{}**.'.format(result)
    match result:
        case 1: 
            embed = discord.Embed(title=title,description='',color=red)
        case кость.value: 
            embed = discord.Embed(title=title,description='',color=green)
        case _: 
            embed = discord.Embed(title=title,description='',color=discordcolor)
    match кость.value:
        case 4: embed.set_thumbnail(url='https://images.vexels.com/media/users/3/232406/isolated/preview/6c9c601abfe8aad6bb82455ff6cbce10-d4-rpg-dice-stroke.png')
        case 6: embed.set_thumbnail(url='https://images.vexels.com/media/users/3/232403/isolated/preview/ee0a1d4d0c3eafaaf9e1ebc052000311-d6-rpg-dice-stroke.png')
        case 8: embed.set_thumbnail(url='https://images.vexels.com/media/users/3/232404/isolated/preview/fda92d8391e57c3b0ac16b9d9adc14d9-d8-rpg-dice-stroke.png')
        case 10: embed.set_thumbnail(url='https://images.vexels.me/media/users/3/232408/isolated/preview/ef74c25cdf596b2a0825d6810297c18a-d10-rpg-dice-stroke.png')
        case 12: embed.set_thumbnail(url='https://images.vexels.com/media/users/3/232405/isolated/preview/2756b6ed4ab2b4e7e2c070a061876b8b-d12-rpg-dice-stroke.png') 
        case 20: embed.set_thumbnail(url='https://images.vexels.com/media/users/3/232402/isolated/preview/577188470e86ba1944f70149d08ea858-d20-rpg-dice-stroke.png')
        case 100: embed.set_thumbnail(url='https://static.wikia.nocookie.net/bindingofisaacre_gamepedia/images/2/29/D100_giantbook.png/revision/latest?cb=20230111001913')
    embed.set_author(name=f'{interaction.user.display_name} совершает бросок {кость.name}.',icon_url=interaction.user.avatar)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="голосование", description='Позволяет провести голосование.')
@app_commands.choices(действие=[
    app_commands.Choice(name="Мут/Размут", value="мут"),
    app_commands.Choice(name="Кик", value="кик"),
    app_commands.Choice(name="Бан", value="бан"),
    app_commands.Choice(name="Таум-аут", value="тайм-аут"),
    app_commands.Choice(name="Повысить", value="повыс"),
    app_commands.Choice(name="Понизить", value="пониж"),
    ])
@app_commands.describe(действие='Действие.' )
@app_commands.describe(пользователь='@Пользователь.' )
@app_commands.choices(анонимность=[
    app_commands.Choice(name="Включить анонимность", value=1),
    app_commands.Choice(name="Выключить анонимность", value=0),
    ])
@app_commands.describe(анонимность='Включить/выключить анонимность.' )
@app_commands.describe(причина = 'Причина.')
@app_commands.describe(длительность = 'Длительность голосования.')
async def vote(interaction:discord.Interaction, действие: app_commands.Choice[str], пользователь: discord.User, причина: str, анонимность: app_commands.Choice[int] = 0, длительность: int = 0):
        error = False

        try:
            анонимность = анонимность.value
        except Exception: анонимность = анонимность

        match действие.value:
                    case 'мут':
                        длительность = limit(длительность, 1, 30)
                    case 'бан':
                        длительность = limit(длительность, 20, 1440)
                    case 'кик':
                        длительность = limit(длительность, 15, 1440)
                    case 'тайм-аут':
                        длительность = limit (длительность, 5, 30)
                    case 'повыс':
                        длительность = limit (длительность, 5, 1440)
                    case 'пониж':
                        длительность = limit (длительность, 5, 1440)


        userdefence = defence[roles[getroleID(interaction.guild, пользователь)]]

        threshold = round(thresholds[действие.value] * userdefence)

        match действие.value:
            case 'бан': title='Голосование: Забанить {}'.format(пользователь.display_name)
            case 'тайм-аут': title='Голосование: Отправить в тайм-аут {}'.format(пользователь.display_name)
            case 'кик': title='Голосование: Изгнать {}'.format(пользователь.display_name)
            case 'мут':
                mute_role = interaction.guild.get_role(1174411093670637660)
                if mute_role in пользователь.roles: title='Голосование: Размутить {}'.format(пользователь.display_name)
                else: title='Голосование: Замутить {}'.format(пользователь.display_name)
            case 'повыс': title='Голосование: Повысить {}'.format(пользователь.display_name)
            case 'пониж': title='Голосование: Понизить {}'.format(пользователь.display_name)
        
        description='Причина: {}\nГолосование продлится {} мин.\n\nИспользуйте кнопки **👍** и **👎**, чтобы голосовать.'.format(причина,длительность)

        embed = discord.Embed(title=title,description=description,color=discordcolor)
        embed.set_author(name=f'Голосование начал {interaction.user.display_name}.', icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=пользователь.avatar)




        VoteYes = Button(label='', emoji='👍',style=discord.ButtonStyle.green)
        VoteNo = Button(label='', emoji='👎', style=discord.ButtonStyle.red)
        VoteInfo = Button(label='Информация', style=discord.ButtonStyle.primary)
        VoteEnd = Button(label='Завершить', style=discord.ButtonStyle.secondary)

        buttonManager = View(timeout = None)

        async def YesCallback(interaction: discord.Interaction):
            if interaction.user.name not in votes[msg.id]['VotersYES']:
                if interaction.user.name in votes[msg.id]['VotersNO']:
                    votes[msg.id]['VotersNO'].remove(interaction.user.name)
                    text = 'Вы изменили свой голос с ПРОТИВ на ЗА.'
                else:
                    text = 'Вы проголосовали ЗА.'
                votes[msg.id]['VotersYES'].append(interaction.user.name)
                await interaction.response.send_message (text, ephemeral=True, delete_after=5)
            else: await interaction.response.send_message ('Вы уже проголосовали ЗА.', ephemeral=True, delete_after=5)
        
        async def NoCallback(interaction: discord.Interaction):
            if interaction.user.name not in votes[msg.id]['VotersNO']:
                if interaction.user.name in votes[msg.id]['VotersYES']:
                    votes[msg.id]['VotersYES'].remove(interaction.user.name)
                    text = 'Вы изменили свой голос с ЗА на ПРОТИВ.'
                else:
                    text = 'Вы проголосовали ПРОТИВ.'
                votes[msg.id]['VotersNO'].append(interaction.user.name)
                await interaction.response.send_message (text, ephemeral=True, delete_after=5)
            else: await interaction.response.send_message ('Вы уже проголосовали ПРОТИВ.', ephemeral=True, delete_after=5)

        async def InfoCallback(interaction: discord.Interaction):

            match анонимность:
                case 1: desc = 'Количество проголосовавших:\n\n**ЗА:** {}.\n**ПРОТИВ**: {}.\n\nТребуемая разница между голосами: {} / {}.'.format(len(votes[msg.id]['VotersYES']), len(votes[msg.id]['VotersNO']), limit(len(votes[msg.id]['VotersYES']) - len(votes[msg.id]['VotersNO']), 0, threshold), threshold)
                case _:
                    VotersYes = ', '.join(votes[msg.id]['VotersYES'])
                    VotersNo = ', '.join(votes[msg.id]['VotersNO'])
                    desc = 'Списки проголосовавших:\n\n**ЗА:** {} ({}).\n**ПРОТИВ**: {} ({}).\n\nТребуемая разница между голосами: {} / {}.'.format(VotersYes, len(votes[msg.id]['VotersYES']), VotersNo, len(votes[msg.id]['VotersNO']), limit(len(votes[msg.id]['VotersYES']) - len(votes[msg.id]['VotersNO']), 0, threshold), threshold)
            
            embed = discord.Embed(title=title,description=desc,color=discordcolor)
            embed.set_author(name=f'Голосование начал {interaction.user.display_name}.', icon_url=interaction.user.avatar)
            embed.set_footer(text=f'Время до конца: {votes[msg.id]['длительность']//60} минут(ы), {votes[msg.id]['длительность']%60} секунд(ы).')
            embed.set_thumbnail(url=пользователь.avatar) 
            await interaction.response.send_message (embed=embed, ephemeral=True, delete_after=10)

        async def EndCallback(interaction: discord.Interaction):
            if interaction.user.guild_permissions.administrator or interaction.user.name == 'sweetyhake':
                votes[msg.id]['длительность'] = 0
                await interaction.response.send_message ('Голосование завершено досрочно.', ephemeral=True, delete_after=5)
            else:
                await interaction.response.send_message ('Досрочно завершить голосование может только администратор.', ephemeral=True, delete_after=5)
            
        VoteYes.callback = YesCallback
        VoteNo.callback = NoCallback
        VoteInfo.callback = InfoCallback
        VoteEnd.callback = EndCallback

        buttonManager.add_item(VoteYes)
        buttonManager.add_item(VoteNo)
        buttonManager.add_item(VoteInfo)
        buttonManager.add_item(VoteEnd)

        vote_channel = bot.get_channel(votes_channel)
        msg = await vote_channel.send(embed=embed, view = buttonManager)
        await interaction.response.send_message(f'Голосование начато в канале {vote_channel.mention}.', ephemeral=True)

        votes[msg.id] = {'VotersYES': [], 'VotersNO': [], 'длительность': длительность*60}

        while votes[msg.id]['длительность'] > 0:
            votes[msg.id]['длительность'] -= 1
            await asyncio.sleep(1)
        
        result = False
        if len(votes[msg.id]['VotersYES']) - len(votes[msg.id]['VotersNO']) >= threshold: result = True

        Vote = f'по результатам голосования {len(votes[msg.id]['VotersYES'])} ЗА vs {len(votes[msg.id]['VotersNO'])} ПРОТИВ.'
        match действие.value:
            case 'мут':
                mute_role = interaction.guild.get_role(1174411093670637660)
                
                if mute_role in пользователь.roles:
                    match result:
                        case True:
                            description='{} был размучен по результатам голосования.'.format(пользователь.display_name)
                            try: 
                                await пользователь.remove_roles(mute_role)
                                current_channel = interaction.user.voice.channel
                                afk_channel = bot.get_channel(776022980202987520)
                                await interaction.user.move_to(afk_channel)
                                await interaction.user.move_to(current_channel)                                
                            except Exception:
                                error = True   
                            
                        case False:
                            description='{} не был размучен по результатам голосования.'.format(пользователь.display_name)
                else:   
                    match result:
                        case True:
                            description='{} был замучен по результатам голосования.'.format(пользователь.display_name)
                            try: 
                                await пользователь.add_roles(mute_role)
                                current_channel = interaction.user.voice.channel
                                afk_channel = bot.get_channel(776022980202987520)
                                await interaction.user.move_to(afk_channel)
                                await interaction.user.move_to(current_channel)                                
                            except Exception:
                                error = True                    

                        case False:
                            description='{} не был замучен по результатам голосования.'.format(пользователь.display_name)
            case 'кик':
                match result:
                    case True:
                        description='{} был изгнан по результатам голосования.'.format(пользователь.display_name)
                        try:
                            await пользователь.kick(причина = Vote)
                        except Exception:
                            error = True
                    case False:
                        description='{} не был изгнан по результатам голосования.'.format(пользователь.display_name)
            case 'бан':
                match result:
                    case True:
                        description='{} был забанен по результатам голосования.'.format(пользователь.display_name)
                        try:
                            await пользователь.ban(причина = Vote)
                        except Exception:
                            error = True
                    case False:
                        description='{} не был забанен по результатам голосования.'.format(пользователь.display_name)
            case 'повыс':
                match result:
                    case True: 
                        role = getroleID(interaction.guild, пользователь)
                        try:
                            await пользователь.remove_roles(interaction.guild.get_role(roles[role]))
                            await пользователь.add_roles(interaction.guild.get_role(roles[role-1]))
                        except Exception:
                            error = True
                        description='{} был повышен по результатам голосования.'.format(пользователь.display_name)
                    case False:
                        description='{} не был повышен по результатам голосования.'.format(пользователь.display_name)
            case 'пониж':
                match result:
                    case True:
                        role = getroleID(interaction.guild, пользователь)
                        try:
                            await пользователь.remove_roles(interaction.guild.get_role(roles[role]))
                            await пользователь.add_roles(interaction.guild.get_role(roles[role+1]))
                        except Exception:
                            error = True
                        description='{} был понижен по результатам голосования.'.format(пользователь.display_name)
                    case False:
                        description='{} не был понижен по результатам голосования.'.format(пользователь.display_name)
            case 'тайм-аут':
                match result:
                    case True:
                        description='{} был отправлен в тайм-аут по результатам голосования.'.format(пользователь.display_name)
                        try:
                            await пользователь.timeout(timedelta(seconds=1200), reason=Vote)
                        except Exception:
                            error = True
                    case False:
                        description='{} не был отправлен в тайм-аут по результатам голосования.'.format(пользователь.display_name)

        match анонимность:
            case 1:
                extrainfo = 'Количество проголосовавших:\n\n**ЗА:** {}.\n**ПРОТИВ**: {}.\n\nТребуемая разница между голосами: {} / {}.'.format(len(votes[msg.id]['VotersYES']), len(votes[msg.id]['VotersNO']), limit(len(votes[msg.id]['VotersYES']) - len(votes[msg.id]['VotersNO']), 0, threshold), threshold)
            case _:
                VotersYes = ', '.join(votes[msg.id]['VotersYES'])
                VotersNo = ', '.join(votes[msg.id]['VotersNO'])
                extrainfo = 'Списки проголосовавших:\n\n**ЗА:** {} ({}).\n**ПРОТИВ**: {} ({}).\n\nТребуемая разница между голосами: {} / {}.'.format(VotersYes, len(votes[msg.id]['VotersYES']), VotersNo, len(votes[msg.id]['VotersNO']), limit(len(votes[msg.id]['VotersYES']) - len(votes[msg.id]['VotersNO']), 0, threshold), threshold)

        if error == True:
            extrainfo = 'Во время выполнения операции возникла ошибка. Просьба связаться с богом, только он разбереться в этом дерьме...'
            embed = discord.Embed(title=description,description=extrainfo,color=yellow)
        else:
            match result:
                case True: embed = discord.Embed(title=description,description=extrainfo,color=green)
                case False: embed = discord.Embed(title=description,description=extrainfo,color=red)

        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=пользователь.avatar)

        await msg.edit(embed=embed, view=None)


@bot.tree.command(name="цвет", description='Позволяет выбрать цвет вашего никнейма.')
async def colorcommand(interaction: discord.Interaction):
    await color(interaction=interaction)

async def color(interaction):
    embed = discord.Embed(title='Выбор цвета',description='Нажмите на иконку цвета, чтобы выбрать его.\n\nКроме того, нажмите ❌, чтобы убрать цвет.',color=discordcolor)
    embed.set_author(name='Цветовыбиралка v3 Lite')

    red = interaction.guild.get_role(1136001363734691970)
    yellow = interaction.guild.get_role(1136001365815078962)
    green = interaction.guild.get_role(1132760058124578926)
    blue = interaction.guild.get_role(1136001356650532874)
    white = interaction.guild.get_role(1136004517117317310)
    purple = interaction.guild.get_role(1136001372190408885)
    pink = interaction.guild.get_role(1188642076414459984)
    orange = interaction.guild.get_role(1136001389798113521)
    black = interaction.guild.get_role(1136004568333963406)

    colors = [
        interaction.guild.get_role(1136001363734691970), 
        interaction.guild.get_role(1136001365815078962), 
        interaction.guild.get_role(1132760058124578926), 
        interaction.guild.get_role(1136001356650532874),
        interaction.guild.get_role(1136004517117317310),
        interaction.guild.get_role(1136001372190408885),
        interaction.guild.get_role(1188642076414459984),
        interaction.guild.get_role(1136001389798113521),
        interaction.guild.get_role(1136004568333963406)
    ]

    buttonManager = View(timeout=None)
    ColorReset = Button(label='', emoji='❌',style=discord.ButtonStyle.primary)
    ColorRed = Button(label='', emoji='❤️',style=discord.ButtonStyle.secondary)
    ColorYellow = Button(label='', emoji='💛',style=discord.ButtonStyle.secondary)
    ColorGreen = Button(label='', emoji='💚',style=discord.ButtonStyle.secondary)
    ColorBlue = Button(label='', emoji='💙',style=discord.ButtonStyle.secondary)
    ColorWhite = Button(label='', emoji='🤍',style=discord.ButtonStyle.secondary)
    ColorPurple = Button(label='', emoji='💜',style=discord.ButtonStyle.secondary)
    ColorPink = Button(label='', emoji='🩷',style=discord.ButtonStyle.secondary)
    ColorOrange = Button(label='', emoji='🧡',style=discord.ButtonStyle.secondary)
    ColorBlack = Button(label='', emoji='🖤',style=discord.ButtonStyle.secondary)


    async def select_color(interaction: discord.Interaction, color: str = None):

        for role in colors:
            if role in interaction.user.roles: await interaction.user.remove_roles(role)

        match color:
            case None: await interaction.response.send_message('Цвет успешно убран.',ephemeral=True, delete_after=180)
            case _: 
                await interaction.user.add_roles(color)
                await interaction.response.send_message('Цвет успешно выбран.',ephemeral=True, delete_after=180)

    async def RedCallback(interaction: discord.Interaction):
        await select_color(interaction, red)

    async def YellowCallback(interaction: discord.Interaction):
        await select_color(interaction, yellow)

    async def GreenCallback(interaction: discord.Interaction):
        await select_color(interaction, green)

    async def BlueCallback(interaction: discord.Interaction):
        await select_color(interaction, blue)

    async def WhiteCallback(interaction: discord.Interaction):
        await select_color(interaction, white)

    async def PurpleCallback(interaction: discord.Interaction):
        await select_color(interaction, purple)

    async def PinkCallback(interaction: discord.Interaction):
        await select_color(interaction, pink)

    async def OrangeCallback(interaction: discord.Interaction):
        await select_color(interaction, orange)

    async def BlackCallback(interaction: discord.Interaction):
        await select_color(interaction, black)

    
    ColorReset.callback = select_color
    ColorRed.callback = RedCallback
    ColorYellow.callback = YellowCallback
    ColorGreen.callback = GreenCallback
    ColorBlue.callback = BlueCallback
    ColorWhite.callback = WhiteCallback
    ColorPurple.callback = PurpleCallback
    ColorPink.callback = PinkCallback
    ColorOrange.callback = OrangeCallback
    ColorBlack.callback = BlackCallback
    
    buttonManager.add_item(ColorReset)
    buttonManager.add_item(ColorRed)
    buttonManager.add_item(ColorPink)
    buttonManager.add_item(ColorOrange)
    buttonManager.add_item(ColorYellow)
    buttonManager.add_item(ColorGreen)
    buttonManager.add_item(ColorBlue)
    buttonManager.add_item(ColorPurple)
    buttonManager.add_item(ColorWhite)
    buttonManager.add_item(ColorBlack)
    
    await interaction.response.send_message(embed=embed,view=buttonManager,ephemeral=True)

@bot.tree.command(name="иконка", description='Позволяет выбрать иконку перед вашим никнеймом.')
async def iconcommand(interaction:discord.Interaction):
    await icon(interaction=interaction)

async def icon(interaction): 
    
    mainembed = discord.Embed(title='Выбор иконки',description='Нажмите ❌, чтобы убрать иконку.\n\n🍕 - иконки еды.\n\n🐷 - иконки животных.\n\n🤡 - другие иконки.',color=discordcolor)
    mainembed.set_author(name='Иконковыбиралка v1')

    icons = [
        # ЕДА
        interaction.guild.get_role(1218875100842164317), # tomato
        interaction.guild.get_role(1218875781422383175), # eggplant
        interaction.guild.get_role(1218875808362270760), # banana
        interaction.guild.get_role(1218875829237448774), # peach
        interaction.guild.get_role(1218875847445053442), # pepper
        interaction.guild.get_role(1218875944606109746), # beer
        interaction.guild.get_role(1218875881288630344), # cookie
        interaction.guild.get_role(1218875994308345956), # burger
        interaction.guild.get_role(1218876017758830662), # pizza

        # ЖИВОТНЫЕ 
        interaction.guild.get_role(1218876044032086066), # pig
        interaction.guild.get_role(1218876071685128303), # cow
        interaction.guild.get_role(1218876088453955704), # mouse
        interaction.guild.get_role(1218876118686236805), # panda
        interaction.guild.get_role(1218876112533454858), # hamster
        interaction.guild.get_role(1218876160079954021), # boar
        interaction.guild.get_role(1218876186550210651), # octopus
        interaction.guild.get_role(1218876207337308180), # bear
        interaction.guild.get_role(1218876249833869412), # monkey

        # ОСТАЛЬНОЕ 

        interaction.guild.get_role(1218876270985740398), # dice
        interaction.guild.get_role(1218876296323665991), # clown
        interaction.guild.get_role(1218876320076005396), # skelet
        interaction.guild.get_role(1218876347162824774), # devil
        interaction.guild.get_role(1218876369598156881), # bomb
        interaction.guild.get_role(1218876404544831550), # halloween
        interaction.guild.get_role(1218876440649666610), # alien
        interaction.guild.get_role(1218876465735798865), # cowboy
        interaction.guild.get_role(1218876491119726642), # poop
    ]

    buttonManager = View(timeout=None)

    IconReset = Button(label='', emoji='❌',style=discord.ButtonStyle.primary)
    FoodIcon = Button(label='ЕДА', emoji='🍕',style=discord.ButtonStyle.secondary)
    AnimalsIcon = Button(label='ЖИВОТНЫЕ', emoji='🐷',style=discord.ButtonStyle.secondary)
    OtherIcon = Button(label='ДРУГИЕ', emoji='🤡',style=discord.ButtonStyle.secondary)

    async def ReturnCallback(interaction: discord.Interaction):
            await interaction.response.edit_message(embed=mainembed,view=buttonManager)

    
    async def select_icon(interaction: discord.Interaction, icon: str = None):

        for role in icons:
            if role in interaction.user.roles:  await interaction.user.remove_roles(role)

        match icon:
            case None: 
                await interaction.response.send_message('Иконка успешно убрана.',ephemeral=True, delete_after=180)
            case _:
                await interaction.user.add_roles(icons[icon])
                await interaction.response.send_message('Иконка успешно выбрана.',ephemeral=True, delete_after=180)

    async def FoodCallback(interaction: discord.Interaction):
            embed = discord.Embed(title='Иконки: Еда',description='Нажмите на иконку, чтобы выбрать её.',color=discordcolor)
            embed.set_author(name='Иконковыбиралка v1')
            buttonManagerFood = View(timeout = None)

            IconReturn = Button(label='', emoji='↩️',style=discord.ButtonStyle.primary)
            IconTomato = Button(label='', emoji='🍅',style=discord.ButtonStyle.secondary)
            IconEggplant = Button(label='', emoji='🍆',style=discord.ButtonStyle.secondary)
            IconBanana = Button(label='', emoji='🍌',style=discord.ButtonStyle.secondary)
            IconPeach = Button(label='', emoji='🍑',style=discord.ButtonStyle.secondary)
            IconPepper = Button(label='', emoji='🌶️',style=discord.ButtonStyle.secondary)
            IconBeer = Button(label='', emoji='🍺',style=discord.ButtonStyle.secondary)
            IconCookie = Button(label='', emoji='🍪',style=discord.ButtonStyle.secondary)
            IconBurger = Button(label='', emoji='🍔',style=discord.ButtonStyle.secondary)
            IconPizza = Button(label='', emoji='🍕',style=discord.ButtonStyle.secondary)

            async def TomatoCallback(interaction: discord.Interaction):
                await select_icon(interaction, 0)
            async def EggplantCallback(interaction: discord.Interaction):
                await select_icon(interaction, 1)
            async def BananaCallback(interaction: discord.Interaction):
                await select_icon(interaction, 2)            
            async def PeachCallback(interaction: discord.Interaction):
                await select_icon(interaction, 3)            
            async def PepperCallback(interaction: discord.Interaction):
                await select_icon(interaction, 4)            
            async def BeerCallback(interaction: discord.Interaction):
                await select_icon(interaction, 5)            
            async def CookieCallback(interaction: discord.Interaction):
                await select_icon(interaction, 6)   
            async def BurgerCallback(interaction: discord.Interaction):
                await select_icon(interaction, 7)
            async def PizzaCallback(interaction: discord.Interaction):
                await select_icon(interaction, 8)  

            IconReturn.callback = ReturnCallback
            IconTomato.callback = TomatoCallback
            IconEggplant.callback = EggplantCallback
            IconBanana.callback = BananaCallback
            IconPeach.callback = PeachCallback
            IconPepper.callback = PepperCallback
            IconBeer.callback = BeerCallback
            IconCookie.callback = CookieCallback
            IconBurger.callback = BurgerCallback
            IconPizza.callback = PizzaCallback
    
            buttonManagerFood.add_item(IconReturn)
            buttonManagerFood.add_item(IconTomato)
            buttonManagerFood.add_item(IconEggplant)
            buttonManagerFood.add_item(IconBanana)
            buttonManagerFood.add_item(IconPeach)
            buttonManagerFood.add_item(IconPepper)
            buttonManagerFood.add_item(IconBeer)
            buttonManagerFood.add_item(IconCookie)
            buttonManagerFood.add_item(IconBurger)
            buttonManagerFood.add_item(IconPizza)

            await interaction.response.edit_message(embed=embed,view=buttonManagerFood)

    async def AnimalsCallback(interaction: discord.Interaction):
            embed = discord.Embed(title='Иконки: Животные',description='Нажмите на иконку, чтобы выбрать её.',color=discordcolor)
            embed.set_author(name='Иконковыбиралка v1')
            buttonManagerFood = View(timeout = None)

            IconReturn = Button(label='', emoji='↩️',style=discord.ButtonStyle.primary)
            Icon1 = Button(label='', emoji='🐷',style=discord.ButtonStyle.secondary)
            Icon2 = Button(label='', emoji='🐮',style=discord.ButtonStyle.secondary)
            Icon3 = Button(label='', emoji='🐭',style=discord.ButtonStyle.secondary)
            Icon4 = Button(label='', emoji='🐼',style=discord.ButtonStyle.secondary)
            Icon5 = Button(label='', emoji='🐹',style=discord.ButtonStyle.secondary)
            Icon6 = Button(label='', emoji='🐗',style=discord.ButtonStyle.secondary)
            Icon7 = Button(label='', emoji='🐙',style=discord.ButtonStyle.secondary)
            Icon8 = Button(label='', emoji='🐻',style=discord.ButtonStyle.secondary)
            Icon9 = Button(label='', emoji='🐵',style=discord.ButtonStyle.secondary)

            async def Callback1(interaction: discord.Interaction):
                await select_icon(interaction, 0+8+1)
            async def Callback2(interaction: discord.Interaction):
                await select_icon(interaction, 1+8+1)
            async def Callback3(interaction: discord.Interaction):
                await select_icon(interaction, 2+8+1)            
            async def Callback4(interaction: discord.Interaction):
                await select_icon(interaction, 3+8+1)            
            async def Callback5(interaction: discord.Interaction):
                await select_icon(interaction, 4+8+1)            
            async def Callback6(interaction: discord.Interaction):
                await select_icon(interaction, 5+8+1)            
            async def Callback7(interaction: discord.Interaction):
                await select_icon(interaction, 6+8+1)   
            async def Callback8(interaction: discord.Interaction):
                await select_icon(interaction, 7+8+1)
            async def Callback9(interaction: discord.Interaction):
                await select_icon(interaction, 8+8+1)  

            IconReturn.callback = ReturnCallback
            Icon1.callback = Callback1
            Icon2.callback = Callback2
            Icon3.callback = Callback3
            Icon4.callback = Callback4
            Icon5.callback = Callback5
            Icon6.callback = Callback6
            Icon7.callback = Callback7
            Icon8.callback = Callback8
            Icon9.callback = Callback9
    
            buttonManagerFood.add_item(IconReturn)
            buttonManagerFood.add_item(Icon1)
            buttonManagerFood.add_item(Icon2)
            buttonManagerFood.add_item(Icon3)
            buttonManagerFood.add_item(Icon4)
            buttonManagerFood.add_item(Icon5)
            buttonManagerFood.add_item(Icon6)
            buttonManagerFood.add_item(Icon7)
            buttonManagerFood.add_item(Icon8)
            buttonManagerFood.add_item(Icon9)

            await interaction.response.edit_message(embed=embed,view=buttonManagerFood)       

    async def OtherCallback(interaction: discord.Interaction):
            embed = discord.Embed(title='Иконки: Другие',description='Нажмите на иконку, чтобы выбрать её.',color=discordcolor)
            embed.set_author(name='Иконковыбиралка v1')
            buttonManagerFood = View(timeout = None)

            IconReturn = Button(label='', emoji='↩️',style=discord.ButtonStyle.primary)
            Icon1 = Button(label='', emoji='🎲',style=discord.ButtonStyle.secondary)
            Icon2 = Button(label='', emoji='🤡',style=discord.ButtonStyle.secondary)
            Icon3 = Button(label='', emoji='💀',style=discord.ButtonStyle.secondary)
            Icon4 = Button(label='', emoji='😈',style=discord.ButtonStyle.secondary)
            Icon5 = Button(label='', emoji='💣',style=discord.ButtonStyle.secondary)
            Icon6 = Button(label='', emoji='🎃',style=discord.ButtonStyle.secondary)
            Icon7 = Button(label='', emoji='👽',style=discord.ButtonStyle.secondary)
            Icon8 = Button(label='', emoji='🤠',style=discord.ButtonStyle.secondary)
            Icon9 = Button(label='', emoji='💩',style=discord.ButtonStyle.secondary)

            async def Callback1(interaction: discord.Interaction):
                await select_icon(interaction, 0+16+2)
            async def Callback2(interaction: discord.Interaction):
                await select_icon(interaction, 1+8+8+2)
            async def Callback3(interaction: discord.Interaction):
                await select_icon(interaction, 2+8+8+2)            
            async def Callback4(interaction: discord.Interaction):
                await select_icon(interaction, 3+8+8+2)            
            async def Callback5(interaction: discord.Interaction):
                await select_icon(interaction, 4+8+8+2)            
            async def Callback6(interaction: discord.Interaction):
                await select_icon(interaction, 5+8+8+2)            
            async def Callback7(interaction: discord.Interaction):
                await select_icon(interaction, 6+8+8+2)   
            async def Callback8(interaction: discord.Interaction):
                await select_icon(interaction, 7+8+8+2)
            async def Callback9(interaction: discord.Interaction):
                await select_icon(interaction, 8+8+8+2)  

            IconReturn.callback = ReturnCallback
            Icon1.callback = Callback1
            Icon2.callback = Callback2
            Icon3.callback = Callback3
            Icon4.callback = Callback4
            Icon5.callback = Callback5
            Icon6.callback = Callback6
            Icon7.callback = Callback7
            Icon8.callback = Callback8
            Icon9.callback = Callback9
    
            buttonManagerFood.add_item(IconReturn)
            buttonManagerFood.add_item(Icon1)
            buttonManagerFood.add_item(Icon2)
            buttonManagerFood.add_item(Icon3)
            buttonManagerFood.add_item(Icon4)
            buttonManagerFood.add_item(Icon5)
            buttonManagerFood.add_item(Icon6)
            buttonManagerFood.add_item(Icon7)
            buttonManagerFood.add_item(Icon8)
            buttonManagerFood.add_item(Icon9)

            await interaction.response.edit_message(embed=embed,view=buttonManagerFood)      
    
    IconReset.callback = select_icon
    FoodIcon.callback = FoodCallback
    AnimalsIcon.callback = AnimalsCallback
    OtherIcon.callback = OtherCallback

    
    
    buttonManager.add_item(FoodIcon)
    buttonManager.add_item(AnimalsIcon)
    buttonManager.add_item(OtherIcon)
    buttonManager.add_item(IconReset)

    
    await interaction.response.send_message(embed=mainembed,view=buttonManager,ephemeral=True)

def limit (number, minim, maxim):
     if number <= minim: return minim
     elif number >= maxim: return maxim
     else: return number


def getroleID (guild, user):
    if guild.get_role(ROLE0ID) in user.roles: return 0
    elif guild.get_role(ROLE1ID) in user.roles: return 1
    elif guild.get_role(ROLE2ID) in user.roles: return 2
    elif guild.get_role(ROLE3ID) in user.roles: return 3
    elif guild.get_role(ROLE4ID) in user.roles: return 4
    elif guild.get_role(ROLE5ID) in user.roles: return 5
    elif guild.get_role(ROLE6ID) in user.roles: return 6
    elif guild.get_role(ROLE7ID) in user.roles: return 7
    elif guild.get_role(ROLE8ID) in user.roles: return 8
    else: return 6



@bot.tree.command(name='комната', description='Позволяет создать временный голосовой канал.')
@app_commands.describe(name='Количество сообщений.' )
@app_commands.describe(limit = 'Причина.')
@app_commands.choices(private=[
    app_commands.Choice(name="Приватный канал.", value=False),
    app_commands.Choice(name="Общедоступный канал.", value=True),
    ])
@app_commands.describe(private='Приватность канала.' )
@app_commands.choices(hidden=[
    app_commands.Choice(name="Скрытый канал.", value=False),
    app_commands.Choice(name="Видимый канал.", value=True),
    ])
@app_commands.describe(hidden='Видимость канала.' )
async def createchannel(interaction: discord.Interaction, name: str = None, limit: int = 0, private: app_commands.Choice[int] = True, hidden: app_commands.Choice[int] = True):
    match name: 
        case None: name = f'Домен {interaction.user.display_name}'

    everyone = discord.PermissionOverwrite()
    if private == True: everyone.connect = True
    else: everyone.connect = False
    if hidden == True: everyone.view_channel = True
    else: everyone.view_channel = False
    userr = discord.PermissionOverwrite()
    userr.manage_channels = True
    userr.manage_permissions = True
    userr.connect = True
    userr.view_channel = True
    voice = await interaction.guild.create_voice_channel(category=interaction.guild.get_channel(798113553210146837),user_limit=limit,name=name, overwrites={interaction.guild.default_role: everyone, interaction.user: userr})
    try: await interaction.user.move_to(channel=voice)
    except Exception: pass
    await interaction.response.send_message(f'Голосовой канал {voice} успешно создан.', ephemeral=True, delete_after=5)
    await asyncio.sleep(10)
    tempchannels.append(voice)
    if len(voice.members) == 0:
        try: 
            await voice.delete()
            print (f'Голосовой канал {voice} был удалён.')
        except Exception: pass

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel in tempchannels:
        if after.channel is not before:
            if len(before.channel.members) == 0:
                await asyncio.sleep(3)
                if len(before.channel.members) == 0:
                    try: 
                        await before.channel.delete()
                        print (f'Голосовой канал {before.channel} был удалён.')
                    except Exception: pass
                
@bot.tree.command(name='русскаярулетка', description='Сыграйте в эту смертельную игру с друзьями.')
@app_commands.choices(bullet=[
    app_commands.Choice(name="1 патрон", value=1),
    app_commands.Choice(name="2 патрона", value=2),
    app_commands.Choice(name="3 патрона", value=3),
    app_commands.Choice(name="4 патрона", value=4),
    app_commands.Choice(name="5 патронов", value=5),
    ])
@app_commands.describe(bullet='Зарядить в револьвер...' )
@app_commands.choices(penalty=[
    app_commands.Choice(name="Перманентный мут.", value='мут'),
    app_commands.Choice(name="Тайм-аут на 10 минут.", value='тайм-аут'),
    app_commands.Choice(name="Понижение.", value='пониж'),
    app_commands.Choice(name="Изгнание с сервера.", value='мут'),
    ])
@app_commands.describe(penalty='Наказание за смерть.' )
async def russianroulette(interaction:discord.Interaction, bullet: app_commands.Choice[int], penalty: app_commands.Choice[str]):

    JoinButton = Button(label='ПРИСОЕДЕНИТЬСЯ',style=discord.ButtonStyle.primary)
    LeaveButton = Button(label='ПОКИНУТЬ',style=discord.ButtonStyle.secondary)
    StartButton = Button(label='НАЧАТЬ',style=discord.ButtonStyle.green)

    buttonManagerMenu = View(timeout=None)

    penalty_name = penalty.name
    penalty_value = penalty.value

    owner = interaction.user

    async def JoinCallback(interaction: discord.Interaction):
        if  interaction.user not in roulette[msg.id]['alive']:
            roulette[msg.id]['alive'].append(interaction.user)
            await interaction.response.send_message('Вы вступили в игру.',ephemeral=True)
            players = []
            for player in roulette[msg.id]['alive']:
                players.append(player.display_name)
            players = ', '.join(players)
            description = 'Присоеденитесь к игре, нажав кнопку **[ПРИСОЕДЕНИТЬСЯ]** ниже.\n\nТекущие игроки: {}\n\nСоздатель комнаты должен нажать **[НАЧАТЬ]**, когда все будут готовы.'.format(players)
            embed = discord.Embed(title=f'{owner.display_name} приглашает поиграть в русскую рулетку.',description=description,color=discordcolor)
            embed.set_author(name='Русская рулетка v0.3')
            embed.set_footer(text=f'Наказание: {penalty_name}')
            embed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/512/10/10967.png')
            await interaction.followup.edit_message(message_id=msg.id, embed=embed, view=buttonManagerMenu)
        else:
            await interaction.response.send_message('Вы уже в игре.',ephemeral=True)

    async def LeaveCallback(interaction: discord.Interaction):
        if interaction.user in roulette[msg.id]['alive']:
            roulette[msg.id]['alive'].remove(interaction.user)
            await interaction.response.send_message('Вы покинули игру, трусишка.',ephemeral=True)
            players = []
            for player in roulette[msg.id]['alive']:
                players.append(player.display_name)
            players = ', '.join(players)
            description = 'Присоеденитесь к игре, нажав кнопку **[ПРИСОЕДЕНИТЬСЯ]** ниже.\n\nТекущие игроки: {}\n\nСоздатель комнаты должен нажать **[НАЧАТЬ]**, когда все будут готовы.'.format(players)
            embed = discord.Embed(title=f'{owner.display_name} приглашает поиграть в русскую рулетку.',description=description,color=discordcolor)
            embed.set_author(name='Русская рулетка v0.3')
            embed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/512/10/10967.png')
            await interaction.followup.edit_message(message_id=msg.id, embed=embed, view=buttonManagerMenu)
        else:
            await interaction.response.send_message('Вы не в списке участников.',ephemeral=True)

    async def StartCallback(interaction: discord.Interaction):
      if interaction.user == owner:
        if len(roulette[msg.id]['alive']) > 0:
            ShootButton = Button(label='СТРЕЛЯТЬ', emoji='❤️',style=discord.ButtonStyle.primary)
            SpinButton = Button(label='КРУТИТЬ БАРАБАН', emoji='❤️',style=discord.ButtonStyle.secondary)
            async def ShootCallback(interaction: discord.Interaction):
              if interaction.user == roulette[msg.id]['currentplayer']:
                SpinButton.disabled = False
                title = 'Ход {}.'.format(roulette[msg.id]['currentplayer'].display_name)
                players = []
                currentplayer = roulette[msg.id]['currentplayer']
                if roulette[msg.id]['currentbullet'] in roulette[msg.id]['deathbullets']:
                    roulette[msg.id]['currentplayer'] = roulette[msg.id]['alive'][cycle(roulette[msg.id]['alive'].index(currentplayer)+1,0,len(roulette[msg.id]['alive'])-1)] 
                    roulette[msg.id]['dead'].append(interaction.user)
                    roulette[msg.id]['alive'].remove(interaction.user)
                    for player in roulette[msg.id]['alive']:
                        players.append(player.display_name)
                    players = ', '.join(players)
                    roulette[msg.id]['deathbullets'].remove(roulette[msg.id]['currentbullet'])
                    roulette[msg.id]['lastaction'] = f'{interaction.user.display_name} выстреливает... В СЕБЯ!'
                    description = 'Последнее действие: {}\n\nОстались в живых: {}\n\n{}, стреляй или крути барабан.'.format(roulette[msg.id]['lastaction'],players, roulette[msg.id]['currentplayer'].display_name)
                    embed = discord.Embed(title=title,description=description,color=red)
                    try:
                        match penalty_value:
                            case 'кик':
                                role = getroleID(interaction.guild, interaction.user)
                                try:
                                    if interaction.guild.get_role(roles[role]) >= 3:
                                        await interaction.user.remove_roles(interaction.guild.get_role(roles[role]))
                                        await interaction.user.add_roles(interaction.guild.get_role(roles[7]))
                                    else:
                                        await interaction.user.kick(reason='Проиграл в русскую рулетку.')
                                except Exception: pass
                            case 'мут':
                                mute_role = interaction.guild.get_role(1174411093670637660)
                                if mute_role not in interaction.user.roles: await interaction.user.add_roles(mute_role)
                                try: 
                                    current_channel = interaction.user.voice.channel
                                    afk_channel = bot.get_channel(776022980202987520)
                                    await interaction.user.move_to(afk_channel)
                                    await interaction.user.move_to(current_channel)
                                except Exception: pass
                            case 'тайм-аут':
                                try: await interaction.user.timeout(timedelta(seconds=60), reason='Проиграл в русскую рулетку.')
                                except Exception: pass
                            case 'пониж':
                                try:
                                    role = getroleID(interaction.guild, interaction.user)
                                    await interaction.user.remove_roles(interaction.guild.get_role(roles[role]))
                                    await interaction.user.add_roles(interaction.guild.get_role(roles[role+1]))
                                except Exception: pass
                            
                    except Exception: pass
                else:
                    roulette[msg.id]['lastaction'] = f'{interaction.user.display_name} выстреливает... холостой.'
                    roulette[msg.id]['currentplayer'] = roulette[msg.id]['alive'][cycle(roulette[msg.id]['alive'].index(currentplayer)+1,0,len(roulette[msg.id]['alive'])-1)] 
                    for player in roulette[msg.id]['alive']:
                        players.append(player.display_name)
                    players = ', '.join(players)
                    description = 'Последнее действие: {}\n\nОстались в живых: {}\n\n{}, стреляй или крути барабан.'.format(roulette[msg.id]['lastaction'],players, roulette[msg.id]['currentplayer'].display_name)
                    embed = discord.Embed(title=title,description=description,color=green)
                embed.set_footer(text=f'Наказание: {penalty_name}')
                roulette[msg.id]['currentbullet'] = cycle(roulette[msg.id]['currentbullet']+1, 1, 6)
                embed.set_author(name='Русская рулетка v0.3')
                embed.set_thumbnail(url=roulette[msg.id]['currentplayer'].avatar)
                SpinButton.disabled = True
                ShootButton.disabled = True
                await interaction.response.edit_message(embed=embed, view=buttonManagerGame) 

                if len(roulette[msg.id]['alive']) == 0:
                    await asyncio.sleep(8)
                    players = []
                    for player in roulette[msg.id]['dead']:
                        players.append(player.display_name)
                    players = ', '.join(players)
                    embed = discord.Embed(title='Все игроки мертвы.',description=f'Список мертвых: {players}.',color=red)
                    embed.set_author(name='Русская рулетка v0.3')
                    embed.set_footer(text=f'Наказание: {penalty_name}')
                    embed.set_thumbnail(url='https://media.forgecdn.net/avatars/496/695/637811735967861165.png')
                    await interaction.followup.edit_message(message_id=msg.id,embed=embed, view=None) 
                else:
                    if len(roulette[msg.id]['deathbullets']) == 0:
                        await asyncio.sleep(6)
                        players = []
                        for player in roulette[msg.id]['alive']:
                            players.append(player.display_name)
                        players = ', '.join(players)
                        deads = []
                        for dead in roulette[msg.id]['dead']:
                            deads.append(dead.display_name)
                        deads = ', '.join(deads)
                        embed = discord.Embed(title='Патроны в револьвере закончились.',description=f'Список выживших: {players}.\n\nСписок мертвых: {deads}', color=yellow)
                        embed.set_thumbnail(url='https://www.pngall.com/wp-content/uploads/14/Happy-Emoji-Transparent.png')
                        embed.set_author(name='Русская рулетка v0.3')
                        embed.set_footer(text=f'Наказание: {penalty_name}')
                        await interaction.followup.edit_message(message_id=msg.id,embed=embed, view=None) 
                    else:
                        await asyncio.sleep(2)
                        SpinButton.disabled = False
                        ShootButton.disabled = False
                        title = 'Ход {}.'.format(roulette[msg.id]['currentplayer'].display_name)
                        embed = discord.Embed(title=title,description=description,color=green)
                        embed.set_thumbnail(url=roulette[msg.id]['currentplayer'].avatar)
                        embed.set_author(name='Русская рулетка v0.3')
                        embed.set_footer(text=f'Наказание: {penalty_name}')
                        await interaction.followup.edit_message(message_id=msg.id,embed=embed, view=buttonManagerGame) 
              else:
                  await interaction.response.send_message('Сейчас не ваш ход.', ephemeral=True,delete_after=5)
            async def SpinCallback(interaction: discord.Interaction):
                if interaction.user == roulette[msg.id]['currentplayer']:
                    roulette[msg.id]['currentbullet'] = random.randint(1,6)
                    roulette[msg.id]['lastaction'] = f'{interaction.user.display_name} крутит барабан.'
                    title = 'Ход {}.'.format(roulette[msg.id]['currentplayer'].display_name)
                    description = 'Последнее действие: {}\n\nОстались в живых: {}\n\n{}, стреляй. Бежать некуда.'.format(roulette[msg.id]['lastaction'],players, roulette[msg.id]['currentplayer'].display_name)
                    embed = discord.Embed(title=title,description=description,color=yellow)
                    embed.set_author(name='Русская рулетка v0.3')
                    embed.set_thumbnail(url=roulette[msg.id]['currentplayer'].avatar)
                    embed.set_footer(text=f'Наказание: {penalty_name}')
                    SpinButton.disabled = True
                    await interaction.response.edit_message(embed=embed, view=buttonManagerGame)  
                else:
                    await interaction.response.send_message('Сейчас не ваш ход.', ephemeral=True,delete_after=5)

            ShootButton.callback = ShootCallback
            SpinButton.callback = SpinCallback

            buttonManagerGame = View(timeout=None)

            buttonManagerGame.add_item(ShootButton)
            buttonManagerGame.add_item(SpinButton)

            roulette[msg.id]['currentbullet'] = random.randint(1,6)
            players = []
            for player in roulette[msg.id]['alive']:
                players.append(player.display_name)
            players = ', '.join(players)
            roulette[msg.id]['currentplayer'] = roulette[msg.id]['alive'][random.randint(0,len(roulette[msg.id]['alive'])-1)]
            title = 'Ход {}.'.format(roulette[msg.id]['currentplayer'].display_name)
            description = 'Последнее действие: {}\n\nОстались в живых: {}\n\n{}, стреляй или крути барабан.'.format(roulette[msg.id]['lastaction'],players, roulette[msg.id]['currentplayer'].display_name)
            embed = discord.Embed(title=title,description=description,color=green)
            embed.set_author(name='Русская рулетка v0.3')
            embed.set_thumbnail(url=roulette[msg.id]['currentplayer'].avatar)
            embed.set_footer(text=f'Наказание: {penalty_name}')
            await interaction.response.edit_message(embed=embed, view=buttonManagerGame)   
        else:
            await interaction.response.send_message('Недостаточно игроков.', ephemeral=True, delete_after=5)
      else:
          await interaction.response.send_message('Вы не создатель комнаты.', ephemeral=True, delete_after=5)
    JoinButton.callback = JoinCallback
    LeaveButton.callback = LeaveCallback
    StartButton.callback = StartCallback
    
    buttonManagerMenu.add_item(JoinButton)
    buttonManagerMenu.add_item(LeaveButton)
    buttonManagerMenu.add_item(StartButton)

    alive = []
    alive.append(interaction.user)
    deathbullets = []
    maxbullet = bullet.value
    while maxbullet > 0:
        tempbullet = random.randint(1,6)
        if tempbullet not in deathbullets:
            deathbullets.append(tempbullet)
            maxbullet= maxbullet - 1


    players =  f'{interaction.user.display_name}'
    description = 'Присоеденитесь к игре, нажав кнопку **[ПРИСОЕДЕНИТЬСЯ]** ниже.\n\nТекущие игроки: {}\n\nСоздатель комнаты должен нажать **[НАЧАТЬ]**, когда все будут готовы.'.format(players)
    embed = discord.Embed(title=f'{owner.display_name} приглашает поиграть в русскую рулетку.',description=description,color=discordcolor)
    embed.set_author(name='Русская рулетка v0.3')
    embed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/512/10/10967.png')
    embed.set_footer(text=f'Наказание: {penalty.name}')

    await interaction.response.send_message(embed=embed, view=buttonManagerMenu)
    msg = await interaction.original_response()
    roulette[msg.id] = {'dead' : [], 'alive': alive, 'deathbullets' : deathbullets, 'currentbullet' : 1, 'currentplayer': None, 'lastaction': ''}

    

@bot.tree.command(name='пригласить', description='Позволяет пригласить человека в свой приватный/скрытый голосовой канал.')
@app_commands.describe(target_user = 'Пользователь.' )
async def invitetochannel(interaction: discord.Interaction, target_user: discord.User):
    
    if interaction.user.voice.channel in tempchannels:
        voice_channel = interaction.user.voice.channel
        permissions = voice_channel.permissions_for(interaction.user)
        if permissions.manage_channels:
            await voice_channel.set_permissions(target_user, view_channel= True, connect = True)
            await interaction.response.send_message(f'{target_user.display_name} был приглашен в ваш голосовой канал.', ephemeral=True, delete_after=5)
        else:
            await interaction.response.send_message(f'Это не ваш голосовой канал.', ephemeral=True, delete_after=5)
    else: await interaction.response.send_message('Вы не находитесь в голосовом канале.', ephemeral=True, delete_after=5)

@bot.tree.command(name='стирание', description='НЕ ИСПОЛЬЗОВАТЬ БЕЗ ВЕСОМЫХ ПРИЧИН!')
async def reset(interaction: discord.Interaction):
    if interaction.user.name in moderator_list:
        if os.path.exists("obsdata.json"):
            # Удаляем файл
            os.remove("obsdata.json")
            print(f'Файл {"obsdata.json"} успешно удален.')
        else:
            print(f'Файл {"obsdata.json"} не найден.')
        check_inventory_file()
        await interaction.response.send_message('ФАЙЛ С ДАННЫМИ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ УСПЕШНО УНИЧТОЖЕН.', ephemeral=True)
        os.remove("inventory.json")
    else: await interaction.response.send_message('Иди нахуй', ephemeral=True,delete_after=1)

@bot.tree.command(name='датацентр')
@app_commands.describe(newdata='Оставить пустым, если не хочешь ничего сломать.')
async def datasend(interaction: discord.Interaction, newdata: str = ''):
    if interaction.user.name in moderator_list:
        if newdata == '':
            data = str(load_data())
            data = data.replace("'", '"')
            print(data)
            await interaction.response.send_message(data, ephemeral=True)
        else:
            newdata = newdata.replace("'", '"')
            with open("obsdata.json", "w") as file:
                file.write(str(newdata))
            await interaction.response.send_message(newdata, ephemeral=True)


@bot.event
async def on_message(message):
    if message.channel.id == votes_channel and not message.author.bot:
        await message.delete()

@bot.tree.command(name='очистка', description='Удалить сообщения. Доступно только администраторам.')
@app_commands.describe(amount='Количество сообщений.' )
async def clear_messages(interaction: discord.Interaction, amount: int = 1):
        try: await interaction.response.send_message('Сообщения успешно удалены.',ephemeral=True, delete_after=5 )  
        except Exception: pass
        await interaction.channel.purge(limit=amount)  

@bot.event
async def on_member_join(member):
    await member.add_roles(member.guild.get_role(ROLE6ID))
    print(f'{member.name} зашел на сервер.')

def cycle(number, minim, maxim):
    if number > maxim: return minim
    elif number < minim: return maxim
    else: return number
# Запустить бота с вашим токеном
bot.run(TOKEN)
