import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import requests
import json
import datetime
from colorama import Fore, Back, Style, init
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import qrcode
import string
import wikipedia
import psutil

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
    +say [message] - Envoie un message
    +embed [titre] [description] - Envoie un embed
    +servericon - Affiche l'icône du serveur
    +servercount - Affiche le nombre de serveurs où le bot est présent
    +nickname [nouveau pseudo] - Change le pseudo de l'utilisateur
    +poll [question] [options] - Crée un sondage
    +calc [expression] - Évalue une expression mathématique
    +ascii [texte] - Crée un ASCII art
    +remind [temps] [rappel] - Rappelle un événement
    +ban [membre] [raison] - Banni un membre
    +kick [membre] [raison] - Expulse un membre
    +mute [membre] [raison] - Met un membre en mode muet
    +unmute [membre] - Enlève le mode muet d'un membre
    +role [membre] [rôle] - Donne ou retire un rôle à un membre
    +purge [nombre] - Supprime un nombre spécifié de messages
    +slowmode [secondes] - Définit le mode lent d'un canal
    +lock - Verrouille un canal
    +unlock - Déverrouille un canal
    +giveaway [temps] [prix] - Crée un giveaway
    +weather [ville] - Affiche la météo d'une ville
    +translate [langue] [texte] - Traduit un texte
    +joke - Envoie une blague
    +morse [texte] - Convertit un texte en morse
    +spotify [recherche] - Recherche une musique sur Spotify
    +qrcode [texte] - Génère un QR code
    +password [longueur] - Génère un mot de passe
    +poll_advanced [question] [options] - Crée un sondage avancé
    +todo [action] [item] - Gère une liste de tâches
    +timer [secondes] - Démarre un timer
    +urban [terme] - Recherche un terme sur Urban Dictionary
    +wiki [recherche] - Recherche sur Wikipedia
    +stats - Affiche les statistiques du bot
    +anime [titre] - Recherche un anime
    +github [utilisateur] - Recherche un utilisateur sur GitHub
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
        
    API_KEY = "VOTRE_CLE_API_OPENWEATHER" 
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

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command()
async def embed(ctx, title, *, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.random())
    await ctx.send(embed=embed)

@bot.command()
async def servericon(ctx):
    if not ctx.guild:
        await ctx.send("Cette commande doit être utilisée dans un serveur!")
        return
    await ctx.send(ctx.guild.icon_url)

@bot.command()
async def servercount(ctx):
    servers = len(bot.guilds)
    await ctx.send(f"Je suis présent dans {servers} serveurs!")

@bot.command()
async def nickname(ctx, *, new_nickname=None):
    if not ctx.guild:
        await ctx.send("Cette commande doit être utilisée dans un serveur!")
        return
    try:
        await ctx.author.edit(nick=new_nickname)
        if new_nickname:
            await ctx.send(f"Pseudo changé en: {new_nickname}")
        else:
            await ctx.send("Pseudo réinitialisé")
    except discord.Forbidden:
        await ctx.send("Je n'ai pas la permission de changer votre pseudo!")

@bot.command()
async def poll(ctx, question, *options):
    if len(options) < 2:
        await ctx.send("Il faut au moins 2 options pour créer un sondage!")
        return
    if len(options) > 10:
        await ctx.send("Maximum 10 options pour un sondage!")
        return

    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    description = []
    for i, option in enumerate(options):
        description.append(f"{reactions[i]} {option}")
    
    embed = discord.Embed(title=question, description='\n'.join(description))
    poll_msg = await ctx.send(embed=embed)
    
    for i in range(len(options)):
        await poll_msg.add_reaction(reactions[i])

@bot.command()
async def calc(ctx, *, expression):
    try:
        result = eval(expression)
        await ctx.send(f"Résultat: {result}")
    except:
        await ctx.send("Expression invalide!")

@bot.command()
async def ascii(ctx, *, text):
    try:
        ascii_art = f"```\n{text}\n```"
        await ctx.send(ascii_art)
    except:
        await ctx.send("Erreur lors de la création de l'ASCII art!")

@bot.command()
async def remind(ctx, time: int, *, reminder):
    await ctx.send(f"Je vous rappellerai de '{reminder}' dans {time} secondes!")
    await asyncio.sleep(time)
    await ctx.send(f"Rappel: {reminder}")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.name} a été banni. Raison: {reason}")
    except:
        await ctx.send("Je n'ai pas la permission de bannir ce membre!")

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"{member.name} a été expulsé. Raison: {reason}")
    except:
        await ctx.send("Je n'ai pas la permission d'expulser ce membre!")

@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        try:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)
        except:
            await ctx.send("Je n'ai pas pu créer le rôle Muted!")
            return
    try:
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"{member.name} a été mute. Raison: {reason}")
    except:
        await ctx.send("Je n'ai pas la permission de mute ce membre!")

@bot.command()
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        await ctx.send("Le rôle Muted n'existe pas!")
        return
    try:
        await member.remove_roles(muted_role)
        await ctx.send(f"{member.name} a été unmute.")
    except:
        await ctx.send("Je n'ai pas la permission d'unmute ce membre!")

@bot.command()
async def role(ctx, member: discord.Member, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"Le rôle {role_name} n'existe pas!")
        return
    try:
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"Rôle {role_name} retiré de {member.name}")
        else:
            await member.add_roles(role)
            await ctx.send(f"Rôle {role_name} ajouté à {member.name}")
    except:
        await ctx.send("Je n'ai pas la permission de gérer les rôles!")

@bot.command()
async def purge(ctx, amount: int = 10):
    try:
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Suppression de {len(deleted)-1} messages.', delete_after=5)
    except:
        await ctx.send("Je n'ai pas la permission de supprimer les messages!")

@bot.command()
async def slowmode(ctx, seconds: int = 0):
    try:
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send("Mode lent désactivé.")
        else:
            await ctx.send(f"Mode lent défini sur {seconds} secondes.")
    except:
        await ctx.send("Je n'ai pas la permission de modifier le mode lent!")

@bot.command()
async def lock(ctx):
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("Canal verrouillé! 🔒")
    except:
        await ctx.send("Je n'ai pas la permission de verrouiller le canal!")

@bot.command()
async def unlock(ctx):
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("Canal déverrouillé! 🔓")
    except:
        await ctx.send("Je n'ai pas la permission de déverrouiller le canal!")

@bot.command()
async def giveaway(ctx, temps: int, *, prix):
    embed = discord.Embed(title="🎉 GIVEAWAY 🎉", description=f"Prix: {prix}\nDurée: {temps} secondes", color=discord.Color.green())
    message = await ctx.send(embed=embed)
    await message.add_reaction("🎉")
    await asyncio.sleep(temps)
    
    message = await ctx.channel.fetch_message(message.id)
    users = []
    reaction = discord.utils.get(message.reactions, emoji="🎉")
    
    async for user in reaction.users():
        if user.id != bot.user.id:
            users.append(user)
            
    if len(users) == 0:
        await ctx.send("Personne n'a participé au giveaway 😢")
        return
        
    gagnant = random.choice(users)
    await ctx.send(f"Félicitations {gagnant.mention}! Tu as gagné: {prix}! 🎉")

@bot.command()
async def weather(ctx, *, city):
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        api_key = os.getenv('WEATHER_API_KEY')
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric',
            'lang': 'fr'
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            
            embed = discord.Embed(title=f"Météo à {city}", color=discord.Color.blue())
            embed.add_field(name="Température", value=f"{temp}°C")
            embed.add_field(name="Description", value=desc)
            embed.add_field(name="Humidité", value=f"{humidity}%")
            embed.add_field(name="Vent", value=f"{wind} m/s")
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("Ville non trouvée!")
    except:
        await ctx.send("Erreur lors de la récupération des données météo!")

@bot.command()
async def translate(ctx, lang_to, *, text):
    try:
        from googletrans import Translator
        translator = Translator()
        translation = translator.translate(text, dest=lang_to)
        embed = discord.Embed(title="Traduction", color=discord.Color.green())
        embed.add_field(name="Texte original", value=text)
        embed.add_field(name=f"Traduction ({lang_to})", value=translation.text)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Erreur de traduction! Vérifiez le code de langue.")

@bot.command()
async def joke(ctx):
    try:
        response = requests.get("https://api.blablagues.net/?rub=blagues")
        data = response.json()
        blague = data["data"]["content"]["text"]
        await ctx.send(f"**{blague['head']}**\n{blague['content']}")
    except:
        await ctx.send("Erreur lors de la récupération de la blague!")

@bot.command()
async def morse(ctx, *, text):
    morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
        '9': '----.', '0': '-----', ' ': ' '
    }
    morse_text = ''
    for char in text.upper():
        if char in morse_dict:
            morse_text += morse_dict[char] + ' '
    await ctx.send(f"```{morse_text}```")

@bot.command()
async def spotify(ctx, *, query):
    try:
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
        results = sp.search(q=query, limit=5)
        
        embed = discord.Embed(title="Résultats Spotify", color=discord.Color.green())
        for idx, track in enumerate(results['tracks']['items']):
            embed.add_field(name=f"{idx+1}. {track['name']}", 
                          value=f"Artiste: {track['artists'][0]['name']}\nAlbum: {track['album']['name']}", 
                          inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Erreur lors de la recherche Spotify!")

@bot.command()
async def qrcode(ctx, *, text):
    try:
        img = qrcode.make(text)
        img.save("qr_temp.png")
        await ctx.send(file=discord.File("qr_temp.png"))
        os.remove("qr_temp.png")
    except:
        await ctx.send("Erreur lors de la création du QR code!")

@bot.command()
async def password(ctx, length: int = 12):
    import string
    if length < 8:
        await ctx.send("La longueur minimale est de 8 caractères!")
        return
    if length > 100:
        await ctx.send("La longueur maximale est de 100 caractères!")
        return
    
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    await ctx.author.send(f"Voici votre mot de passe généré: ||{password}||")
    await ctx.message.delete()

@bot.command()
async def poll_advanced(ctx, question, *options):
    if len(options) < 2:
        await ctx.send("Il faut au moins 2 options!")
        return
    if len(options) > 10:
        await ctx.send("Maximum 10 options!")
        return

    emoji_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    description = []
    for i, option in enumerate(options):
        description.append(f"{emoji_numbers[i]} {option}")
    
    embed = discord.Embed(title=question, description='\n'.join(description), color=discord.Color.blue())
    embed.set_footer(text="Sondage créé par " + ctx.author.name)
    poll_message = await ctx.send(embed=embed)
    
    for i in range(len(options)):
        await poll_message.add_reaction(emoji_numbers[i])

@bot.command()
async def todo(ctx, action="list", *, item=None):
    todo_file = "todo.json"
    if not os.path.exists(todo_file):
        with open(todo_file, "w") as f:
            json.dump([], f)
    
    with open(todo_file, "r") as f:
        todos = json.load(f)
    
    if action == "list":
        if not todos:
            await ctx.send("La liste est vide!")
            return
        embed = discord.Embed(title="Liste des tâches", color=discord.Color.blue())
        for i, todo in enumerate(todos, 1):
            embed.add_field(name=f"#{i}", value=todo, inline=False)
        await ctx.send(embed=embed)
    
    elif action == "add" and item:
        todos.append(item)
        with open(todo_file, "w") as f:
            json.dump(todos, f)
        await ctx.send(f"Tâche ajoutée: {item}")
    
    elif action == "remove" and item:
        try:
            index = int(item) - 1
            removed = todos.pop(index)
            with open(todo_file, "w") as f:
                json.dump(todos, f)
            await ctx.send(f"Tâche supprimée: {removed}")
        except:
            await ctx.send("Index invalide!")
    
    elif action == "clear":
        todos.clear()
        with open(todo_file, "w") as f:
            json.dump(todos, f)
        await ctx.send("Liste effacée!")

@bot.command()
async def timer(ctx, seconds: int):
    if seconds > 7200:
        await ctx.send("Le temps maximum est de 2 heures (7200 secondes)!")
        return
    if seconds < 1:
        await ctx.send("Le temps minimum est de 1 seconde!")
        return
    
    message = await ctx.send(f"Timer: {seconds} secondes restantes")
    while seconds > 0:
        await asyncio.sleep(1)
        seconds -= 1
        if seconds % 5 == 0:  # Update every 5 seconds to avoid rate limits
            await message.edit(content=f"Timer: {seconds} secondes restantes")
    await message.edit(content="Timer terminé! ⏰")
    await ctx.send(f"{ctx.author.mention} Timer terminé!")

@bot.command()
async def urban(ctx, *, term):
    try:
        url = f"http://api.urbandictionary.com/v0/define?term={term}"
        response = requests.get(url)
        data = response.json()
        
        if not data['list']:
            await ctx.send(f"Aucune définition trouvée pour '{term}'")
            return
            
        definition = data['list'][0]
        embed = discord.Embed(title=term, color=discord.Color.blue())
        embed.add_field(name="Définition", value=definition['definition'][:1024], inline=False)
        embed.add_field(name="Exemple", value=definition['example'][:1024], inline=False)
        embed.add_field(name="👍", value=definition['thumbs_up'])
        embed.add_field(name="👎", value=definition['thumbs_down'])
        
        await ctx.send(embed=embed)
    except:
        await ctx.send("Erreur lors de la recherche!")

@bot.command()
async def wiki(ctx, *, search):
    try:
        wikipedia.set_lang("fr")
        result = wikipedia.summary(search, sentences=3)
        embed = discord.Embed(title=search, description=result, color=discord.Color.blue())
        await ctx.send(embed=embed)
    except wikipedia.exceptions.DisambiguationError as e:
        await ctx.send(f"Terme ambigu. Options possibles: {', '.join(e.options[:5])}")
    except wikipedia.exceptions.PageError:
        await ctx.send(f"Aucun article trouvé pour '{search}'")
    except:
        await ctx.send("Erreur lors de la recherche Wikipedia!")

@bot.command()
async def stats(ctx):
    embed = discord.Embed(title="Statistiques du bot", color=discord.Color.blue())
    embed.add_field(name="Serveurs", value=len(bot.guilds))
    embed.add_field(name="Utilisateurs", value=len(set(bot.get_all_members())))
    embed.add_field(name="Canaux", value=len(list(bot.get_all_channels())))
    embed.add_field(name="Ping", value=f"{round(bot.latency * 1000)}ms")
    
    memory = psutil.Process().memory_info().rss / 1024 / 1024
    embed.add_field(name="Utilisation mémoire", value=f"{memory:.2f} MB")
    
    uptime = datetime.datetime.now() - bot.start_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    embed.add_field(name="Uptime", value=f"{hours}h {minutes}m {seconds}s")
    
    await ctx.send(embed=embed)

@bot.command()
async def anime(ctx, *, title):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={title}"
        response = requests.get(url)
        data = response.json()
        
        if not data['data']:
            await ctx.send(f"Aucun anime trouvé pour '{title}'")
            return
            
        anime = data['data'][0]
        embed = discord.Embed(title=anime['title'], url=anime['url'], color=discord.Color.blue())
        embed.set_thumbnail(url=anime['images']['jpg']['image_url'])
        embed.add_field(name="Score", value=anime['score'])
        embed.add_field(name="Episodes", value=anime['episodes'])
        embed.add_field(name="Status", value=anime['status'])
        embed.add_field(name="Type", value=anime['type'])
        if anime['synopsis']:
            embed.add_field(name="Synopsis", value=anime['synopsis'][:1024], inline=False)
        
        await ctx.send(embed=embed)
    except:
        await ctx.send("Erreur lors de la recherche d'anime!")

@bot.command()
async def github(ctx, username):
    try:
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            await ctx.send(f"Utilisateur '{username}' non trouvé!")
            return
            
        embed = discord.Embed(title=data['login'], url=data['html_url'], color=discord.Color.purple())
        embed.set_thumbnail(url=data['avatar_url'])
        embed.add_field(name="Repos publics", value=data['public_repos'])
        embed.add_field(name="Followers", value=data['followers'])
        embed.add_field(name="Following", value=data['following'])
        if data['bio']:
            embed.add_field(name="Bio", value=data['bio'], inline=False)
        
        await ctx.send(embed=embed)
    except:
        await ctx.send("Erreur lors de la recherche GitHub!")

bot.start_time = datetime.datetime.now()

bot.run(os.getenv('TOKEN'), bot=False)
