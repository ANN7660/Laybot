import discord
from discord.ext import commands
import os

# Configuration des intents (TRÈS IMPORTANT)

intents = discord.Intents.all()  # Active TOUS les intents pour le debug

bot = commands.Bot(command_prefix=’!’, intents=intents)

# ===== ÉVÉNEMENTS DE DEBUG =====

@bot.event
async def on_ready():
print(’\n’ + ‘=’ * 60)
print(‘🟢 BOT EN LIGNE !’)
print(’=’ * 60)
print(f’👤 Nom: {bot.user}’)
print(f’🆔 ID: {bot.user.id}’)
print(f’📊 Serveurs: {len(bot.guilds)}’)
print(’=’ * 60)

```
# Liste les serveurs
print('\n📋 SERVEURS:')
for guild in bot.guilds:
    print(f'  • {guild.name} (ID: {guild.id})')

print('\n' + '=' * 60)
print('✅ Bot prêt à recevoir des commandes !')
print('💬 Tape !ping ou !role dans un salon Discord')
print('=' * 60 + '\n')

# Statut
await bot.change_presence(
    activity=discord.Game(name="!role | !ping"),
    status=discord.Status.online
)
```

@bot.event
async def on_message(message):
“”“Affiche TOUS les messages reçus (pour debug)”””

```
# Ignore les messages du bot
if message.author == bot.user:
    return

# AFFICHE TOUS LES MESSAGES REÇUS
print(f'\n📨 MESSAGE REÇU:')
print(f'   Auteur: {message.author}')
print(f'   Contenu: "{message.content}"')
print(f'   Salon: #{message.channel.name}')
print(f'   Serveur: {message.guild.name if message.guild else "MP"}')

# Vérifie si c'est une commande
if message.content.startswith('!'):
    print(f'   ⚡ C\'EST UNE COMMANDE !')

# IMPORTANT: Process les commandes
await bot.process_commands(message)
```

# ===== COMMANDES =====

@bot.command(name=‘ping’)
async def ping(ctx):
“”“Test simple”””
print(f’\n✅ COMMANDE !ping EXÉCUTÉE par {ctx.author}\n’)
latency = round(bot.latency * 1000)
await ctx.send(f’🏓 Pong! Latence: {latency}ms’)

@bot.command(name=‘role’, aliases=[‘roles’])
async def show_roles(ctx):
“”“Affiche la hiérarchie des rôles”””
print(f’\n✅ COMMANDE !role EXÉCUTÉE par {ctx.author}\n’)

```
try:
    # Récupère le bot dans le serveur
    bot_member = ctx.guild.me
    bot_top_role = bot_member.top_role
    bot_position = bot_top_role.position
    
    print(f'🤖 Rôle du bot: {bot_top_role.name} (Position: {bot_position})')
    
    # Trie tous les rôles
    all_roles = sorted(ctx.guild.roles, key=lambda r: r.position, reverse=True)
    
    roles_above = []
    roles_below = []
    bot_roles = []
    
    for role in all_roles:
        if role.position > bot_position:
            roles_above.append(role)
        elif role.position == bot_position:
            bot_roles.append(role)
        elif role.position < bot_position and role.name != "@everyone":
            roles_below.append(role)
    
    print(f'⬆️  Rôles au-dessus: {len(roles_above)}')
    print(f'⬇️  Rôles en-dessous: {len(roles_below)}')
    
    # Création de l'embed
    embed = discord.Embed(
        title="🎭 Hiérarchie des Rôles",
        description=f"**Rôle du bot:** {bot_top_role.mention}\n**Position:** `{bot_position}`",
        color=bot_top_role.color if bot_top_role.color != discord.Color.default() else discord.Color.blue()
    )
    
    # Rôles au-dessus
    if roles_above:
        text = "\n".join([f"`{r.position}` {r.mention}" for r in roles_above[:15]])
        if len(roles_above) > 15:
            text += f"\n*... et {len(roles_above) - 15} autres*"
        embed.add_field(name=f"⬆️ Au-dessus ({len(roles_above)})", value=text, inline=False)
    else:
        embed.add_field(name="⬆️ Au-dessus", value="*Aucun*", inline=False)
    
    # Rôle du bot
    bot_text = "\n".join([f"`{r.position}` {r.mention}" for r in bot_roles])
    embed.add_field(name="🤖 Bot", value=bot_text, inline=False)
    
    # Rôles en-dessous
    if roles_below:
        text = "\n".join([f"`{r.position}` {r.mention}" for r in roles_below[:15]])
        if len(roles_below) > 15:
            text += f"\n*... et {len(roles_below) - 15} autres*"
        embed.add_field(name=f"⬇️ En-dessous ({len(roles_below)})", value=text, inline=False)
    else:
        embed.add_field(name="⬇️ En-dessous", value="*Aucun*", inline=False)
    
    # Stats
    embed.add_field(
        name="📊 Total",
        value=f"**{len(ctx.guild.roles)}** rôles dans le serveur",
        inline=False
    )
    
    embed.set_footer(text=f"Par {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
    
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    
    await ctx.send(embed=embed)
    print('✅ Embed envoyé avec succès!\n')
    
except Exception as e:
    print(f'❌ ERREUR: {e}\n')
    await ctx.send(f'❌ Erreur: {e}')
```

@bot.command(name=‘test’)
async def test(ctx):
“”“Commande de test ultra simple”””
print(f’\n✅ COMMANDE !test EXÉCUTÉE\n’)
await ctx.send(‘✅ Le bot fonctionne parfaitement!’)

# ===== GESTION DES ERREURS =====

@bot.event
async def on_command_error(ctx, error):
if isinstance(error, commands.CommandNotFound):
print(f’⚠️  Commande inconnue: {ctx.message.content}’)
await ctx.send(f’❌ Commande inconnue! Utilise `!ping` ou `!role`’)
else:
print(f’❌ ERREUR: {error}’)
await ctx.send(f’❌ Erreur: {error}’)

# ===== LANCEMENT =====

if **name** == “**main**”:
print(’\n’ + ‘🚀’ * 30)
print(‘DÉMARRAGE DU BOT…’)
print(‘🚀’ * 30 + ‘\n’)

```
TOKEN = os.environ.get('BOT_TOKEN')

if not TOKEN:
    print('❌ ERREUR CRITIQUE: Variable BOT_TOKEN non trouvée!')
    print('📝 Configure BOT_TOKEN dans les variables d\'environnement')
    print('\nSur Replit:')
    print('  1. Clique sur "Secrets" (🔒 dans le menu)')
    print('  2. Ajoute: Key = BOT_TOKEN, Value = ton_token')
    print('  3. Redémarre le bot\n')
    exit(1)

print(f'✅ Token trouvé: {TOKEN[:20]}...')
print('\n⏳ Connexion à Discord...\n')

try:
    bot.run(TOKEN)
except discord.LoginFailure:
    print('\n❌ TOKEN INVALIDE!')
    print('Vérifie ton token sur: https://discord.com/developers/applications\n')
except Exception as e:
    print(f'\n❌ ERREUR DE CONNEXION: {e}\n')
```