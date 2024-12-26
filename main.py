import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import requests
import json
import datetime
from colorama import Fore, Back, Style, init

init(autoreset=True)

load_dotenv()

ASCII_ART = f"""{Fore.RED + Style.BRIGHT}
___________________________________________________
 _______         __   ___      ______         __   
|     __|.-----.|  |.'  _|    |   __ \.-----.|  |_ 
|__     ||  -__||  ||   _|    |   __ <|  _  ||   _|
|_______||_____||__||__|      |______/|_____||____|  
___________________________________________________                                         
{Style.RESET_ALL}"""

class SelfBot(commands.Bot):
    async def start(self, *args, **kwargs):
        await super().start(os.getenv('TOKEN'), bot=False)

bot = SelfBot(command_prefix='+', self_bot=True)

@bot.event
async def on_ready():
    print(ASCII_ART)
    print(f'{Fore.RED + Style.BRIGHT}SelfBot connecté en tant que {bot.user.name}{Style.RESET_ALL}')

@bot.command()
async def aide(ctx):
    help_text = f"""
    {Fore.GREEN + Style.BRIGHT}**Commandes disponibles:**{Style.RESET_ALL}
    +aide - Affiche cette aide
    +ping - Vérifie la latence du bot
    +avatar [utilisateur] - Affiche l'avatar d'un utilisateur
    +userinfo [utilisateur] - Affiche les informations d'un utilisateur
    +serveurinfo - Affiche les informations du serveur
    +clear [nombre] - Supprime un nombre spécifié de messages
    +meteo [ville] - Affiche la météo d'une ville
    +roll [max] - Lance un dé avec un maximum spécifié
    +status [type] [texte] - Change le statut du bot (type: game/watching/listening/stream)
    """
    await ctx.send(help_text)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'{Fore.BLUE + Style.BRIGHT}Pong! Latence: {latency}ms{Style.RESET_ALL}')

@bot.command()
async def avatar(ctx, *, user: discord.User = None):
    user = user or ctx.author
    await ctx.send(user.avatar_url)

@bot.command()
async def userinfo(ctx, *, user: discord.User = None):
    user = user or ctx.author
    embed = discord.Embed(title=f"{Fore.YELLOW + Style.BRIGHT}Info de {user.name}{Style.RESET_ALL}", color=discord.Color.blue())
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Nom", value=user.name)
    embed.add_field(name="Discriminateur", value=user.discriminator)
    embed.add_field(name="Compte créé le", value=user.created_at.strftime("%d/%m/%Y"))
    await ctx.send(embed=embed)

@bot.command()
async def serveurinfo(ctx):
    if not ctx.guild:
        await ctx.send("Cette commande doit être utilisée dans un serveur!")
        return
        
    guild = ctx.guild
    embed = discord.Embed(title=f"{Fore.YELLOW + Style.BRIGHT}Info du serveur {guild.name}{Style.RESET_ALL}", color=discord.Color.blue())
    embed.add_field(name="ID", value=guild.id)
    embed.add_field(name="Propriétaire", value=str(guild.owner))
    embed.add_field(name="Membres", value=guild.member_count)
    embed.add_field(name="Salons", value=len(guild.channels))
    embed.add_field(name="Rôles", value=len(guild.roles))
    embed.add_field(name="Créé le", value=guild.created_at.strftime("%d/%m/%Y"))
    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx, amount: int = None):
    if amount is None:
        await ctx.send("Veuillez spécifier un nombre de messages à supprimer.")
        return
    if amount < 1:
        await ctx.send("Le nombre doit être supérieur à 0.")
        return
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'{Fore.GREEN + Style.BRIGHT}{amount} messages supprimés.{Style.RESET_ALL}', delete_after=3)

@bot.command()
async def meteo(ctx, *, city=None):
    if city is None:
        await ctx.send("Veuillez spécifier une ville.")
        return
        
    API_KEY = "VOTRE_CLE_API_OPENWEATHER"  # Remplacez par votre clé API OpenWeather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=fr"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        await ctx.send(f"{Fore.CYAN + Style.BRIGHT}Météo à {city}: {desc}, {temp}°C{Style.RESET_ALL}")
    else:
        await ctx.send("Ville non trouvée.")

@bot.command()
async def roll(ctx, maximum: int = 100):
    if maximum < 1:
        await ctx.send("Le nombre maximum doit être supérieur à 0.")
        return
    result = random.randint(1, maximum)
    await ctx.send(f"{Fore.MAGENTA + Style.BRIGHT} {ctx.author.name} lance un dé et obtient: {result}{Style.RESET_ALL}")

@bot.command()
async def status(ctx, status_type=None, *, text=None):
    if status_type is None or text is None:
        await ctx.send("Usage: +status [game/watching/listening/stream] [texte]")
        return
        
    status_type = status_type.lower()
    if status_type == "game":
        await bot.change_presence(activity=discord.Game(name=text))
    elif status_type == "watching":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
    elif status_type == "listening":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))
    elif status_type == "stream":
        await bot.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/J'VOUS_GAZ", assets=None))
    else:
        await ctx.send("Type de statut invalide. Utilisez: game, watching, listening ou stream")
        return
    await ctx.send(f"{Fore.GREEN + Style.BRIGHT}Statut changé en: {status_type} {text}{Style.RESET_ALL}")

bot.run(os.getenv('TOKEN'), bot=False)
