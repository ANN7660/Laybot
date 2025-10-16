Voici ton code avec l’analyse des rôles ajoutée :

```python
import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import os
from keep_alive import keep_alive

# ===== CONFIGURATION DES SALONS =====

WELCOME_CHANNEL_ID = 1384523345705570487  # ID du salon de bienvenue
LEAVE_CHANNEL_ID = None  # Mettre None si pas utilisé, sinon remplacer par l'ID

# Configuration du bot

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Événement de connexion

@bot.event
async def on_ready():
    print(f'🤖 {bot.user} est connecté et prêt!')
    print(f'📊 Serveurs: {len(bot.guilds)}')
    print(f'👥 Utilisateurs: {len(set(bot.get_all_members()))}')
    print('=' * 50)
    
    await bot.change_presence(
        activity=discord.Game(name="HK le meilleur 🔥"),
        status=discord.Status.dnd
    )
    
    # 🆕 AFFICHE LES RÔLES AU-DESSUS DU BOT
    print("\n🎭 ANALYSE DES RÔLES PAR SERVEUR :")
    print('=' * 50)
    
    for guild in bot.guilds:
        print(f"\n📍 Serveur : {guild.name}")
        
        # Récupère le membre bot dans ce serveur
        bot_member = guild.me
        bot_role_position = bot_member.top_role.position
        
        print(f"🤖 Rôle du bot : {bot_member.top_role.name} (Position: {bot_role_position})")
        
        # Liste tous les rôles au-dessus du bot
        roles_above = [role for role in guild.roles if role.position > bot_role_position]
        
        if roles_above:
            print(f"⚠️  {len(roles_above)} rôle(s) AU-DESSUS du bot :")
            for role in sorted(roles_above, key=lambda r: r.position, reverse=True):
                members_count = len(role.members)
                print(f"   🔺 {role.name} (Pos: {role.position}) - {members_count} membre(s)")
        else:
            print("✅ Aucun rôle au-dessus du bot (position optimale)")
        
        # Liste les rôles au même niveau ou en dessous
        roles_below = [role for role in guild.roles if 0 < role.position <= bot_role_position and role != bot_member.top_role]
        
        if roles_below:
            print(f"\n✅ {len(roles_below)} rôle(s) EN DESSOUS ou AU MÊME NIVEAU :")
            for role in sorted(roles_below, key=lambda r: r.position, reverse=True):
                members_count = len(role.members)
                print(f"   🔹 {role.name} (Pos: {role.position}) - {members_count} membre(s)")
        
        print('-' * 50)
    
    print("\n✅ Analyse des rôles terminée !\n")

# Message de bienvenue

@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    
    if not welcome_channel:
        welcome_channels = ['bienvenue', 'général', 'welcome', 'general']
        for channel_name in welcome_channels:
            welcome_channel = discord.utils.get(member.guild.channels, name=channel_name)
            if welcome_channel:
                break
        
        if not welcome_channel:
            welcome_channel = member.guild.system_channel
    
    if welcome_channel:
        try:
            await welcome_channel.send(f"Bienvenue {member.mention} profite bien sur **Lay** !")
        except discord.Forbidden:
            print(f"❌ Pas de permission pour envoyer dans {welcome_channel.name}")
    else:
        print(f"⚠️ Aucun salon de bienvenue trouvé")
    
    # MP de bienvenue
    try:
        dm_embed = discord.Embed(
            title="🎉 Bienvenue sur Lay !",
            description=f"""Salut {member.mention} ! 👋

Bienvenue sur notre serveur **Lay** ! On est ravis de t'accueillir dans notre communauté 🔥

**📝 Pour bien commencer :**
• N'hésite pas à **parler** dans les salons
• **Présente-toi** pour qu'on apprenne à te connaître
• Découvre les différents salons et trouve ta place
• Amuse-toi bien et respecte les autres membres !

Si tu as des questions, l'équipe est là pour t'aider 😊

**Profite bien de ton séjour parmi nous !** ✨""",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        
        if member.guild.icon:
            dm_embed.set_thumbnail(url=member.guild.icon.url)
            dm_embed.set_footer(text=f"Équipe {member.guild.name}", icon_url=member.guild.icon.url)
        else:
            dm_embed.set_footer(text=f"Équipe {member.guild.name}")
        
        await member.send(embed=dm_embed)
        print(f"✅ MP de bienvenue envoyé à {member.display_name}")
        
    except discord.Forbidden:
        print(f"❌ Impossible d'envoyer un MP à {member.display_name} (MPs fermés)")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi du MP: {e}")

# ===== CONFIGURATION DES SALONS =====

@bot.command(name='set_welcome')
@commands.has_permissions(administrator=True)
async def set_welcome_channel(ctx, channel: discord.TextChannel):
    """🏠 Définit le salon de bienvenue"""
    global WELCOME_CHANNEL_ID
    WELCOME_CHANNEL_ID = channel.id
    
    embed = discord.Embed(
        title="✅ Salon de bienvenue configuré",
        description=f"Les messages de bienvenue seront envoyés dans {channel.mention}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name='set_leave')
@commands.has_permissions(administrator=True)  
async def set_leave_channel(ctx, channel: discord.TextChannel):
    """👋 Définit le salon des départs"""
    global LEAVE_CHANNEL_ID
    LEAVE_CHANNEL_ID = channel.id
    
    embed = discord.Embed(
        title="✅ Salon des départs configuré", 
        description=f"Les messages de départ seront envoyés dans {channel.mention}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name='channels_config')
@commands.has_permissions(administrator=True)
async def show_channels_config(ctx):
    """📋 Affiche la configuration des salons"""
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    leave_channel = bot.get_channel(LEAVE_CHANNEL_ID) if LEAVE_CHANNEL_ID else None
    
    embed = discord.Embed(
        title="⚙️ Configuration des salons",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🏠 Bienvenue", 
        value=welcome_channel.mention if welcome_channel else "❌ Non configuré",
        inline=False
    )
    
    embed.add_field(
        name="👋 Départs",
        value=leave_channel.mention if leave_channel else "❌ Non configuré", 
        inline=False
    )
    
    await ctx.send(embed=embed)

# ===== COMMANDES DM =====

@bot.command(name='dmall', aliases=['dm_all', 'msgall'])
@commands.has_permissions(administrator=True)
async def dm_all_members(ctx, *, message):
    """📩 Envoie un message privé à tous les membres du serveur"""
    
    # Compter les vrais membres (sans bots)
    real_members = [m for m in ctx.guild.members if not m.bot and m != ctx.author]
    
    embed = discord.Embed(
        title="⚠️ Confirmation DM ALL",
        description=f"Veux-tu envoyer ce message à **{len(real_members)}** membres ?",
        color=discord.Color.yellow()
    )
    embed.add_field(name="📝 Message", value=f"```{message[:500]}{'...' if len(message) > 500 else ''}```", inline=False)
    embed.add_field(name="⏰ Temps limite", value="30 secondes", inline=True)
    
    confirm_msg = await ctx.send(embed=embed)
    await confirm_msg.add_reaction("✅")
    await confirm_msg.add_reaction("❌")
    
    def check(reaction, user):
        return (user == ctx.author and 
                str(reaction.emoji) in ["✅", "❌"] and 
                reaction.message.id == confirm_msg.id)
    
    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
        
        if str(reaction.emoji) == "❌":
            await confirm_msg.edit(content="❌ Envoi annulé.", embed=None)
            await confirm_msg.clear_reactions()
            return
            
        if str(reaction.emoji) == "✅":
            await confirm_msg.delete()
            
            progress_embed = discord.Embed(
                title="📤 Envoi en cours...",
                description="Envoi des messages privés aux membres",
                color=discord.Color.blue()
            )
            progress_msg = await ctx.send(embed=progress_embed)
            
            sent_count = 0
            failed_count = 0
            
            # Message personnalisé
            dm_embed = discord.Embed(
                title="📢 Message du serveur",
                description=message,
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            dm_embed.add_field(name="👤 Envoyé par", value=ctx.author.display_name, inline=True)
            dm_embed.set_footer(text=f"Message de {ctx.guild.name}")
            
            if ctx.guild.icon:
                dm_embed.set_thumbnail(url=ctx.guild.icon.url)
            
            for member in real_members:
                try:
                    await member.send(embed=dm_embed)
                    sent_count += 1
                    
                    if sent_count % 10 == 0:
                        progress_embed.description = f"📤 Envoyé à **{sent_count}** membres\n❌ Échecs: **{failed_count}**"
                        await progress_msg.edit(embed=progress_embed)
                    
                    await asyncio.sleep(1.5)
                    
                except discord.Forbidden:
                    failed_count += 1
                except discord.HTTPException:
                    failed_count += 1
                except Exception as e:
                    print(f"Erreur DM pour {member}: {e}")
                    failed_count += 1
            
            final_embed = discord.Embed(
                title="📊 Résultats DM ALL",
                color=discord.Color.green() if failed_count < sent_count else discord.Color.orange()
            )
            final_embed.add_field(name="✅ Messages envoyés", value=sent_count, inline=True)
            final_embed.add_field(name="❌ Échecs", value=failed_count, inline=True)
            
            total = sent_count + failed_count
            success_rate = round((sent_count / total) * 100, 1) if total > 0 else 0
            final_embed.add_field(name="📈 Taux de succès", value=f"{success_rate}%", inline=True)
            final_embed.set_footer(text=f"Terminé par {ctx.author.display_name}")
            
            await progress_msg.edit(embed=final_embed)
            
    except asyncio.TimeoutError:
        await confirm_msg.edit(content="⏰ Temps écoulé. Envoi annulé.", embed=None)
        await confirm_msg.clear_reactions()

@bot.command(name='dmrole', aliases=['dm_role'])
@commands.has_permissions(administrator=True)
async def dm_role_members(ctx, role: discord.Role, *, message):
    """📩 Envoie un MP à tous les membres d'un rôle spécifique"""
    
    real_members = [m for m in role.members if not m.bot and m != ctx.author]
    
    if not real_members:
        return await ctx.send(f"❌ Aucun membre trouvé avec le rôle **{role.name}**!")
    
    embed = discord.Embed(
        title="⚠️ Confirmation DM ROLE",
        description=f"Veux-tu envoyer ce message aux **{len(real_members)}** membres du rôle **{role.name}** ?",
        color=role.color if role.color != discord.Color.default() else discord.Color.yellow()
    )
    embed.add_field(name="📝 Message", value=f"```{message[:500]}{'...' if len(message) > 500 else ''}```", inline=False)
    
    confirm_msg = await ctx.send(embed=embed)
    await confirm_msg.add_reaction("✅")
    await confirm_msg.add_reaction("❌")
    
    def check(reaction, user):
        return (user == ctx.author and 
                str(reaction.emoji) in ["✅", "❌"] and 
                reaction.message.id == confirm_msg.id)
    
    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
        
        if str(reaction.emoji) == "❌":
            await confirm_msg.edit(content="❌ Envoi annulé.", embed=None)
            return
            
        if str(reaction.emoji) == "✅":
            await confirm_msg.delete()
            
            sent_count = 0
            failed_count = 0
            
            dm_embed = discord.Embed(
                title=f"📢 Message pour le rôle {role.name}",
                description=message,
                color=role.color if role.color != discord.Color.default() else discord.Color.green(),
                timestamp=datetime.now()
            )
            dm_embed.add_field(name="👤 Envoyé par", value=ctx.author.display_name, inline=True)
            dm_embed.add_field(name="🎭 Rôle ciblé", value=role.name, inline=True)
            dm_embed.set_footer(text=f"Message du serveur {ctx.guild.name}")
            
            progress_msg = await ctx.send("📤 Envoi en cours...")
            
            for member in real_members:
                try:
                    await member.send(embed=dm_embed)
                    sent_count += 1
                    await asyncio.sleep(1.5)
                except:
                    failed_count += 1
            
            result_embed = discord.Embed(
                title=f"📊 Résultats DM {role.name}",
                color=discord.Color.green()
            )
            result_embed.add_field(name="✅ Envoyés", value=sent_count, inline=True)
            result_embed.add_field(name="❌ Échecs", value=failed_count, inline=True)
            
            await progress_msg.edit(content="", embed=result_embed)
            
    except asyncio.TimeoutError:
        await confirm_msg.edit(content="⏰ Temps écoulé. Envoi annulé.", embed=None)

# ===== MODÉRATION =====

@bot.command(name='ban', aliases=['bannir'])
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def ban_member(ctx, member: discord.Member, *, raison="Aucune raison fournie"):
    """🔨 Ban un membre du serveur"""
    if member == ctx.author:
        return await ctx.send("❌ Tu ne peux pas te bannir toi-même!")
    
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("❌ Tu ne peux pas bannir quelqu'un avec un rôle supérieur!")
    
    if member == ctx.guild.owner:
        return await ctx.send("❌ Tu ne peux pas bannir le propriétaire du serveur!")
    
    # 🆕 Vérification du rôle du bot
    if member.top_role >= ctx.guild.me.top_role:
        return await ctx.send("❌ Je ne peux pas bannir quelqu'un avec un rôle supérieur au mien!")
    
    try:
        try:
            dm_embed = discord.Embed(
                title="🔨 Bannissement",
                description=f"Tu as été banni de **{ctx.guild.name}**",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            dm_embed.add_field(name="📝 Raison", value=raison, inline=False)
            dm_embed.add_field(name="👮 Par", value=ctx.author.display_name, inline=False)
            await member.send(embed=dm_embed)
        except:
            pass
        
        await member.ban(reason=f"Par {ctx.author} - {raison}")
        
        embed = discord.Embed(
            title="✅ Membre banni",
            description=f"**{member.display_name}** a été banni",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.add_field(name="📝 Raison", value=raison, inline=False)
        embed.add_field(name="👮 Par", value=ctx.author.mention, inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)
        
        await ctx.send(embed=embed)
    
    except discord.Forbidden:
        await ctx.send("❌ Je n'ai pas les permissions pour bannir ce membre!")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {e}")

@bot.command(name='mute', aliases=['silence'])
@commands.has_permissions(manage_roles=True)
@commands.bot_has_permissions(moderate_members=True)
async def mute_member(ctx, member: discord.Member, duration: int = 10, *, raison="Aucune raison fournie"):
    """🔇 Timeout un membre (durée en minutes)"""
    if member == ctx.author:
        return await ctx.send("❌ Tu ne peux pas te mute toi-même!")
    
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("❌ Tu ne peux pas mute quelqu'un avec un rôle supérieur!")
    
    # 🆕 Vérification du rôle du bot
    if member.top_role >= ctx.guild.me.top_role:
        return await ctx.send("❌ Je ne peux pas timeout quelqu'un avec un rôle supérieur au mien!")
    
    try:
        timeout_duration = timedelta(minutes=duration)
        await member.timeout(timeout_duration, reason=f"Par {ctx.author} - {raison}")
        
        embed = discord.Embed(
            title="🔇 Membre timeout",
            description=f"**{member.display_name}** a été mis en timeout",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        embed.add_field(name="⏰ Durée", value=f"{duration} minutes", inline=True)
        embed.add_field(name="📝 Raison", value=raison, inline=False)
        embed.add_field(name="👮 Par", value=ctx.author.mention, inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)
        
        await ctx.send(embed=embed)
    
    except discord.Forbidden:
        await ctx.send("❌ Je n'ai pas les permissions pour timeout ce membre!")
    except Exception as e:
        await ctx.send(f"❌ Erreur lors du timeout: {e}")

@bot.command(name='unmute', aliases=['demute'])
@commands.has_permissions(manage_roles=True)
async def unmute_member(ctx, member: discord.Member):
    """🔊 Retire le timeout d'un membre"""
    
    if member.timed_out_until is None:
        return await ctx.send("❌ Ce membre n'est pas en timeout!")
    
    try:
        await member.timeout(None, reason=f"Démuté par {ctx.author}")
        
        embed = discord.Embed(
            title="🔊 Membre démuté",
            description=f"**{member.display_name}** a été démuté",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.add_field(name="👮 Par", value=ctx.author.mention, inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)
        
        await ctx.send(embed=embed)
    
    except Exception as e:
        await ctx.send(f"❌ Erreur lors du démute: {e}")

@bot.command(name='delall', aliases=['clearall', 'purge'])
@commands.has_permissions(manage_messages=True)
async def delete_all(ctx, limite: int = 100):
    """🗑️ Supprime tous les messages d'un canal"""
    if limite > 1000:
        return await ctx.send("❌ Limite maximale: 1000 messages!")
    
    if limite < 1:
        return await ctx.send("❌ Le nombre doit être positif!")
    
    embed = discord.Embed(
        title="⚠️ Confirmation requise",
        description=f"Veux-tu vraiment supprimer **{limite}** messages?",
        color=discord.Color.yellow()
    )
    embed.add_field(name="⏰ Temps limite", value="30 secondes", inline=False)
    
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")
    
    def check(reaction, user):
        return (user == ctx.author and 
                str(reaction.emoji) in ["✅", "❌"] and 
                reaction.message.id == msg.id)
    
    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
        
        if str(reaction.emoji) == "✅":
            await msg.delete()
            deleted = await ctx.channel.purge(limit=limite)
            
            confirm_embed = discord.Embed(
                title="✅ Messages supprimés",
                description=f"**{len(deleted)}** messages supprimés!",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            temp_msg = await ctx.send(embed=confirm_embed)
            await asyncio.sleep(5)
            await temp_msg.delete()
        else:
            await msg.clear_reactions()
            await msg.edit(content="❌ Suppression annulée.", embed=None)
    
    except asyncio.TimeoutError:
        await msg.clear_reactions()
        await msg.edit(content="⏰ Temps écoulé. Suppression annulée.", embed=None)

# 🆕 COMMANDE POUR VÉRIFIER LES RÔLES

@bot.command(name='checkroles', aliases=['check_roles', 'roles'])
@commands.has_permissions(administrator=True)
async def check_roles(ctx):
    """🎭 Vérifie les rôles au-dessus du bot"""
    
    bot_member = ctx.guild.me
    bot_role_position = bot_member.top_role.position
    
    # Rôles au-dessus
    roles_above = [role for role in ctx.guild.roles if role.position > bot_role_position]
    
    embed = discord.Embed(
        title="🎭 Analyse des rôles",
        description=f"Position du bot : **{bot_member.top_role.name}** (Pos: {bot_role_position})",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    # Affiche les rôles au-dessus
    if roles_above:
        roles_text = "\n".join([
            f"🔺 **{role.name}** (Pos: {role.position}) - {len(role.members)} membre(s)"
            for role in sorted(roles_above, key=lambda r: r.position, reverse=True)
        ])
        embed.add_field(
            name=f"⚠️ {len(roles_above)} rôle(s) AU-DESSUS (le bot ne peut pas les gérer)",
            value=roles_text[:1024],  # Limite Discord
            inline=False
        )
    else:
        embed.add_field(
            name="✅ Rôles au-dessus",
            value="Aucun (position optimale !)",
            inline=False
        )
    
    # Rôles en dessous
    roles_below = [role for role in ctx.guild.roles if 0 < role.position < bot_role_position]
    
    if roles_below:
        roles_text = "\n".join([
            f"🔹 **{role.name}** (Pos: {role.position})"
            for role in sorted(roles_below, key=lambda r: r.position, reverse=True)[:10]  # Limite à 10
        ])
        if len(roles_below) > 10:
            roles_text += f"\n... et {len(roles_below) - 10} autre(s)"
        
        embed.add_field(
            name=f"✅ {len(roles_below)} rôle(s) EN DESSOUS (le bot peut les gérer)",
            value=roles_text,
            inline=False
        )
    
    embed.set_footer(text=f"Demandé par {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
    
    await ctx.send(embed=embed)

# ===== AIDE =====

@bot.command(name='help_mod', aliases=['aide'])
async def help_moderation(ctx):
    """📋 Affiche les commandes de modération"""
    embed = discord.Embed(
        title="🛡️ Commandes de Modération",
        description="Liste des commandes disponibles",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    embed.add_field(name="🔨 `!ban @membre [raison]`", value="Bannit un membre", inline=False)
    embed.add_field(name="🔇 `!mute @membre [minutes] [raison]`", value="Timeout temporaire", inline=False)
    embed.add_field(name="🔊 `!unmute @membre`", value="Retire le timeout", inline=False)
    embed.add_field(name="🗑️ `!delall [nombre]`", value="Supprime des messages", inline=False)
    embed.add_field(name="🏓 `!ping`", value="Teste la latence", inline=False)
    embed.add_field(name="🎭 `!checkroles`", value="Vérifie les rôles du bot", inline=False)
    
    embed.add_field(name="\n⚙️ Configuration", value="\u200b", inline=False)
    embed.add_field(name="🏠 `!set_welcome #salon`", value="Config bienvenue", inline=False)
    embed.add_field(name="👋 `!set_leave #salon`", value="Config départs", inline=False)
    embed.add_field(name="📋 `!channels_config`", value="Affiche la config", inline=False)
    
    embed.add_field(name="\n📩 Messages privés", value="\u200b", inline=False)
    embed.add_field(name="📤 `!dmall <message>`", value="MP à tous les membres", inline=False)
    embed.add_field(name="🎭 `!dmrole @role <message>`", value="MP aux membres d'un rôle", inline=False)
    
    embed.set_footer(text="Permissions admin requises", icon_url=ctx.author.display_avatar.url)
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    """🏓 Affiche la latence du bot"""
    latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latence: **{latency}ms**",
        color=discord.Color.green() if latency < 100 else discord.Color.orange()
    )
    
    await ctx.send(embed=embed)

# Gestion des erreurs

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ Permissions insuffisantes",
            description="Tu n'as pas les permissions nécessaires!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Membre introuvable!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Arguments invalides! Utilise `!help_mod`")
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        print(f"Erreur: {error}")

# Lancement du bot

if __name__ == "__main__":
    try:
        # Vérification du token
        token = os.environ.get('BOT_TOKEN')
        
        if not token:
            print("❌ ERREUR CRITIQUE : La variable BOT_TOKEN n'est pas définie !")
            print("📝 Sur Replit : Va dans Secrets (🔒) et ajoute BOT_TOKEN")
            exit(1)
```