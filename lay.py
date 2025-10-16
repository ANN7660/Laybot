import discord
from discord.ext import commands
import os

# Configuration des intents

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=’!’, intents=intents)

@bot.event
async def on_ready():
print(’\n’ + ‘=’ * 60)
print(‘BOT EN LIGNE !’)
print(’=’ * 60)
print(f’Nom: {bot.user}’)
print(f’ID: {bot.user.id}’)
print(f’Serveurs: {len(bot.guilds)}’)
print(’=’ * 60)

```
print('\nSERVEURS:')
for guild in bot.guilds:
    print(f'  - {guild.name} (ID: {guild.id})')

print('\n' + '=' * 60)
print('Bot pret ! Tape !ping ou !role')
print('=' * 60 + '\n')

await bot.change_presence(
    activity=discord.Game(name="!role | !ping"),
    status=discord.Status.online
)
```

@bot.event
async def on_message(message):
if message.author == bot.user:
return

```
print(f'\nMESSAGE RECU:')
print(f'  Auteur: {message.author}')
print(f'  Contenu: "{message.content}"')
print(f'  Salon: #{message.channel.name}')

if message.content.startswith('!'):
    print(f'  -> COMMANDE DETECTEE !')

await bot.process_commands(message)
```

@bot.command(name=‘ping’)
async def ping(ctx):
print(f’\nCOMMANDE !ping par {ctx.author}\n’)
latency = round(bot.latency * 1000)
await ctx.send(f’Pong! Latence: {latency}ms’)

@bot.command(name=‘role’, aliases=[‘roles’])
async def show_roles(ctx):
print(f’\nCOMMANDE !role par {ctx.author}\n’)

```
try:
    bot_member = ctx.guild.me
    bot_top_role = bot_member.top_role
    bot_position = bot_top_role.position
    
    print(f'Role du bot: {bot_top_role.name} (Position: {bot_position})')
    
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
    
    print(f'Au-dessus: {len(roles_above)}')
    print(f'En-dessous: {len(roles_below)}')
    
    embed = discord.Embed(
        title="Hierarchie des Roles",
        description=f"**Role du bot:** {bot_top_role.mention}\n**Position:** `{bot_position}`",
        color=bot_top_role.color if bot_top_role.color != discord.Color.default() else discord.Color.blue()
    )
    
    if roles_above:
        text = "\n".join([f"`{r.position}` {r.mention}" for r in roles_above[:15]])
        if len(roles_above) > 15:
            text += f"\n*... et {len(roles_above) - 15} autres*"
        embed.add_field(name=f"Au-dessus ({len(roles_above)})", value=text, inline=False)
    else:
        embed.add_field(name="Au-dessus", value="*Aucun*", inline=False)
    
    bot_text = "\n".join([f"`{r.position}` {r.mention}" for r in bot_roles])
    embed.add_field(name="Bot", value=bot_text, inline=False)
    
    if roles_below:
        text = "\n".join([f"`{r.position}` {r.mention}" for r in roles_below[:15]])
        if len(roles_below) > 15:
            text += f"\n*... et {len(roles_below) - 15} autres*"
        embed.add_field(name=f"En-dessous ({len(roles_below)})", value=text, inline=False)
    else:
        embed.add_field(name="En-dessous", value="*Aucun*", inline=False)
    
    embed.add_field(
        name="Total",
        value=f"**{len(ctx.guild.roles)}** roles dans le serveur",
        inline=False
    )
    
    embed.set_footer(text=f"Par {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
    
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    
    await ctx.send(embed=embed)
    print('Embed envoye !\n')
    
except Exception as e:
    print(f'ERREUR: {e}\n')
    await ctx.send(f'Erreur: {e}')
```

@bot.command(name=‘test’)
async def test(ctx):
print(f’\nCOMMANDE !test\n’)
await ctx.send(‘Le bot fonctionne !’)

@bot.event
async def on_command_error(ctx, error):
if isinstance(error, commands.CommandNotFound):
print(f’Commande inconnue: {ctx.message.content}’)
await ctx.send(f’Commande inconnue ! Utilise !ping ou !role’)
else:
print(f’ERREUR: {error}’)
await ctx.send(f’Erreur: {error}’)

if **name** == “**main**”:
print(’\n’ + ‘=’ * 60)
print(‘DEMARRAGE DU BOT…’)
print(’=’ * 60 + ‘\n’)

```
TOKEN = os.environ.get('BOT_TOKEN')

if not TOKEN:
    print('ERREUR: Variable BOT_TOKEN non trouvee !')
    print('Configure BOT_TOKEN dans les variables d\'environnement')
    exit(1)

print(f'Token trouve: {TOKEN[:20]}...')
print('\nConnexion a Discord...\n')

try:
    bot.run(TOKEN)
except discord.LoginFailure:
    print('\nTOKEN INVALIDE !')
except Exception as e:
    print(f'\nERREUR: {e}\n')
```