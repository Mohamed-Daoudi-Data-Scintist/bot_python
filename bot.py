import discord
import protected_history
import arbre_discussion
from discord.ext import commands
from threading import Lock
from sondage import Sondage
import rappel
import datetime
import asyncio




intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents=intents)
voted_users = set()

last_command = ""
command_history = protected_history.ProtectedCommandHistory()
sondage_actif = False
sondage_en_cours = None
rappels = []


# Création de l'instance du bot de conversation
bot_conversation = arbre_discussion.ConversationBot()
bot_conversation.add_topic("programmation")
bot_conversation.add_topic("cuisine")
bot_conversation.create_tree()

@client.event
async def on_ready():
    print("Bot prêt")

@client.event
async def on_message(message):
    global last_command

    if message.author == client.user:
        return
    elif message.content.startswith("Quoi"):
        await message.channel.send("Feur")
    elif message.content.startswith("Qui"):
        await message.channel.send("Rikou")
    elif message.content.startswith("Hein"):
        await message.channel.send("Heinpagnan\nQuoicoubeh Quoicoubeh")
    elif message.content.startswith("La particularité de Ilias"):
        await message.channel.send("Toujours à son prime")
    elif message.content.startswith("Exactement"):
        await message.channel.send("Réel akhy")
    
    if message.content != "!lastcommand":
        last_command = message.content
        command_history.append(last_command, message.author.id)

    await client.process_commands(message)


@client.command(name="delete")
async def delete(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
    print("Commande de suppression exécutée")

@client.command(name="lastcommand")
async def last_command(ctx):
    global last_command
    
    if last_command != "":
        await ctx.send(f"Dernière commande utilisée : {last_command}")
    else:
        await ctx.send("Aucune commande n'a été utilisée récemment.")

@client.command(name="history")
async def user_history(ctx):
    user_id = ctx.author.id
    user_commands = command_history.get_user_commands(user_id)

    if len(user_commands) > 0:
        await ctx.send(f"Historique des commandes pour l'utilisateur {ctx.author.name}:")
        for command in user_commands:
            await ctx.send(command)
    else:
        await ctx.send("Aucune commande n'a été enregistrée pour cet utilisateur.")

@client.command(name="back")
async def go_back(ctx):
    command = command_history.move_backward()

    if command is not None:
        await ctx.send(f"Commande précédente : {command}")
    else:
        await ctx.send("Vous êtes déjà au début de l'historique.")

@client.command(name="forward")
async def go_forward(ctx):
    command = command_history.move_forward()

    if command is not None:
        await ctx.send(f"Commande suivante : {command}")
    else:
        await ctx.send("Vous êtes déjà à la fin de l'historique.")

@client.command(name="clearhistory")
async def clear_history(ctx):
    user_id = ctx.author.id
    command_history.clear_history(user_id)
    await ctx.send("Historique des commandes effacé.")

@client.command(name="requestaccess")
async def request_access(ctx):
    user_id = ctx.author.id
    command_history.request_access(user_id)
    await ctx.send("Demande d'accès à l'historique envoyée.")

@client.command(name="releaseaccess")
async def release_access(ctx):
    user_id = ctx.author.id
    command_history.release_access(user_id)
    await ctx.send("Accès à l'historique libéré.")

@client.command(name="start_conversation")
async def start_conversation(ctx):
    response = bot_conversation.start_conversation()
    await ctx.send(response)

@client.command(name="reponse")
async def reponse(ctx, *, response):
    bot_response = bot_conversation.response(response)
    await ctx.send(bot_response)

@client.command(name="reset_conversation")
async def reset_conversation(ctx):
    bot_conversation.reset_conversation()
    await ctx.send("La conversation avec le bot a été réinitialisée.")

@client.command(name="savehistory")
async def save_history(ctx):
    command_history.save_to_text("historique.txt")
    await ctx.send("L'historique des commandes a été sauvegardé.")

@client.command(name="loadhistory")
async def load_history(ctx):
    command_history.load_from_text("historique.txt")
    await ctx.send("L'historique des commandes a été chargé.")

@client.command(name="creersondage")
async def creer_sondage(ctx, question, *options):
    global sondage_actif, sondage_en_cours

    if sondage_actif:
        await ctx.send("Un sondage est déjà en cours.")
    else:
        sondage_en_cours = Sondage(question, options)
        sondage_actif = True
        await ctx.send("Un nouveau sondage a été créé.")

@client.command(name="votesondage")
async def voter_sondage(ctx, option):
    global sondage_actif, sondage_en_cours

    if sondage_actif:
        if ctx.author.id not in voted_users:
            sondage_en_cours.ajouter_vote(option)
            voted_users.add(ctx.author.id)
            await ctx.send("Votre vote a été enregistré.")
        else:
            await ctx.send("Vous avez déjà voté dans ce sondage.")
    else:
        await ctx.send("Aucun sondage en cours.")

@client.command(name="resultatsondage")
async def resultat_sondage(ctx):
    global sondage_actif, sondage_en_cours

    if sondage_actif:
        resultat = sondage_en_cours.afficher_resultats()
        await ctx.send(resultat)
    else:
        await ctx.send("Aucun sondage en cours.")

@client.command(name="terminersondage")
async def terminer_sondage(ctx):
    global sondage_actif, sondage_en_cours

    if sondage_actif:
        resultat = sondage_en_cours.afficher_resultats()
        await ctx.send(resultat)
        sondage_actif = False
        sondage_en_cours = None
    else:
        await ctx.send("Aucun sondage en cours.")

@client.command(name="rappel")
async def creer_rappel(ctx):
    await ctx.send(f"ID du canal : {ctx.channel.id}")



@client.command(name="creerrappel")
async def creer_rappel(ctx, description, heure):
    heure = datetime.datetime.strptime(heure, "%H:%M").time()
    nouveau_rappel = rappel.Rappel(description, heure)
    rappels.append(nouveau_rappel)
    await ctx.send("Rappel créé avec succès.")

@client.command(name="afficherrappels")
async def afficher_rappels(ctx):
    if len(rappels) > 0:
        for rappel in rappels:
            maintenant = datetime.datetime.now().time()
            await ctx.send(maintenant)
            await ctx.send(rappel.afficher_rappel())
    else:
        await ctx.send("Aucun rappel enregistré.")

@client.event
async def on_ready():
    print("Bot prêt")
    while True:
        maintenant = datetime.datetime.now().time()
        print(maintenant.hour)
        for rappel in rappels:
            if rappel.est_l_heure():
                await client.get_channel('1091261255496503308').send(rappel.afficher_rappel())
                rappels.remove(rappel)
        await asyncio.sleep(60)  # Vérifie les rappels chaque minute



client.run("MTA5MTI1OTc0MTAwNDY0MDMwNg.Gu7M_l.98gtRXYCs9DDHFivFDvZA2BF0sFCI6A2GfHp7s")