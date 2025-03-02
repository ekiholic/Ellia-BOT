import asyncio
from code import interact
from doctest import debug_script
import os
import random
import math
from tabnanny import check
import time
from threading import Timer
import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.commands import Option
from sqlalchemy import desc
from os import path
from config import *
from ellia_token import TOKEN

class currentPage():
    def __init__(self):
        self.page = 0

test_server = ["976120059598610462"]
box_path = "Users/User_bestiary/"
cd = time.time()
guild_cd = {}

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot Events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        temps = str(time.strftime('%M minutes et %S secondes', time.gmtime(error.retry_after)))
        msg = f"Attends **{temps}** chacal"
        await ctx.respond(msg)

# Bot Commands
@bot.slash_command(name='news', description='Consultez le changelog d\'Ellia')
async def changelog(ctx):
    embed = discord.Embed(title="**[Changelog] Ellia **", description="Dernières modifications : **31/05/2022**", color=discord.Color.from_rgb(0, 255, 166))
    embed.add_field(name=f'[v0.6]', inline=False, value=f'- Différenciation entre un New et un Dupe\n- Ajout de la commande pour consulter son bestiaire **/box**')
    embed.add_field(name=f'[v0.7]', inline=False, value=f'- Ajout de plusieurs filtres pour le bestiaire (élément, grade, invocateur)')
    embed.add_field(name=f'[v0.8]', inline=False, value=f'- Ajout d\'un journal de de modifications **/news**\n- N\'affiche plus **Dupe** lors que t\'obtiens un dupe')
    embed.add_field(name=f'[v0.9]', inline=False, value=f'- Options pour afficher uniquement les L&D ou élementaires **/box**\n- Pagination pour voir le bestiaire entier\n- Numérotation des pages\n- Problème de pagination résolu')
    embed.add_field(name=f'[En développement]', inline=False, value=f'- Différents types d\'affichage pour le bestiaire')
    path = "Source/changelog.png"
    file = discord.File(path, filename="image.png")
    embed.set_thumbnail(url = "attachment://" + "image.png")
    await ctx.respond(embed = embed, file=file)

@bot.slash_command(name='help', description='Tout savoir sur Ellia')
async def help(ctx):
    star = "<:ellia_star:976853657540767835>"
    embed = discord.Embed(title="**Guide du bot Ellia**", color=discord.Color.green(), description="Tu trouveras plus de détails sur les commandes du bot ici.")
    emote = "<:ellia_ld:976796844925546566>"
    embed.add_field(name=f"/ld : Vélin light & dark {emote}", inline=False, value=f"Utilisable une fois toutes les **5 minutes**, invoque un monstre **light** & **dark** :\n{star}{star}{star} : **89.00%**\n{star}{star}{star}{star} : **9.50%**\n{star}{star}{star}{star}{star} : **1.50%**")
    emote = "<:ellia_vl:976796784900853771>"
    embed.add_field(name=f"/vl : Vélin légendaire {emote}", inline=False, value=f"Utilisable une fois toutes les **10 minutes**, invoque un monstre **élémentaire** :\n{star}{star}{star}{star} : **91.00%**\n{star}{star}{star}{star}{star} : **9.00%**")
    emote = "<:ellia_trans:976796872020721705>"
    embed.add_field(name=f"/trans : Vélin transcendance {emote}", inline=False, value=f"Utilisable une fois toutes les **60 minutes**, invoque un monstre **5 {star}**")
    emote = "<:ellia_monster:977122506152509440>"
    embed.add_field(name=f"/box : Bestiaire {emote}", inline=False, value=f"Tu peux consulter ton bestiaire, ou admirer celui d'un autre invocateur.\nTu peux trier par grade et/ou attribut.")
    emote = "<:ellia_changelog:979008161665134592>"
    embed.add_field(name=f"/news : Changelog {emote}", inline=False, value=f"Tu peux voir tous les changements effectués sur le bot.")
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/976377270740594698/979331411834187806/help.png")
    await ctx.respond(embed = embed)

@bot.slash_command(name='box', description='Affiche le bestiaire (nom des monstres)')
async def box(ctx, name: Option(discord.Member, "Nom de l'invocateur", required = False, default = ''),
mode: Option(str, "Mode d'affichage", required = False, default = 'texte', choices=['texte', 'image']),
element: Option(str, "Choisir un élément", required = False, default="", choices=["[Fire]\n", "[Wind]\n", "[Water]\n", "[Light]\n", "[Dark]\n", "Light & Dark", "Elementaires"]),
grade: Option(str, "Choisir un grade", required = False, default="", choices = ["3", "4", "5"])):
    user = ""
    userid = ""
    avatar = ""
    mobs_name = []
    mobs = {}
    display_mob = ""
    stars = ""
    elem = ""
    monster = "<:ellia_monster:977122506152509440>"
    count = 0
    item = 0
    page = 0
    current = currentPage()
    embeds = []
    if name == '':
        name= ctx.author
        user = str(ctx.author.display_name)
        userid = str(ctx.author.id)
    else:
        user = str(name.display_name)
        userid = str(name.id)
    avatar = name.display_avatar
    check = open('Users/user_list.txt', 'r+')
    if f'{userid}\n' not in check:
        emb = discord.Embed(title = f'{user} n\'a aucun monstre {monster}', color = discord.Color.dark_red(), description='')
        emb.set_thumbnail(url = avatar)    
        await ctx.respond(embed = emb)
        return
    f = open(box_path + userid, 'r')
    count_mob = 0
    for i in f:
        count+=1
        mob = i[:-1]
        if mob not in mobs_name:
            mobs_name.append(mob)
            mobs[mob] = 1
            if sort_monster(element, grade, mob) == 0:
                count_mob += 1
        else:
            mobs[mob] += 1
    max = int(math.ceil(count_mob/21))
    if max == 0:
        max = 1
    emb = discord.Embed(title = f'Bestiaire de {user} : x{count}{monster} {str(page+1)}/{max}', color = discord.Color.dark_red(), description='')
    emb.set_thumbnail(url = avatar)
    for i in mobs:
        if item >= 21:
            embeds.append(emb)
            item = 0
            page += 1
            emb = discord.Embed(title = f'Bestiaire de {user} : x{count}{monster} {str(page+1)}/{max}', color = discord.Color.dark_red(), description='')
            emb.set_thumbnail(url = avatar)
        if mobs[i] > 1:
            display_mob = f'{i} x{mobs[i]}'
        else:
            display_mob = f'{i}'
        stars = get_grade(i)
        elem = get_elem_emote(get_element(i))
        if sort_monster(element, grade, i) == 0:
            emb.add_field(name=f'{elem}{display_mob}', value=f'{stars}\u200b', inline=True)
            item += 1
    if item <= 21 and item != 0:
        embeds.append(emb)
        page += 1
    back = Button(label="", style=discord.ButtonStyle.green, emoji="⏪")
    forward = Button(label="", style=discord.ButtonStyle.green, emoji="⏩")
    async def next_page(interaction):
        if current.page + 1 >= page:
            return
        current.page += 1
        if current.page == page - 1:
            view = view3
        elif current.page < page:
            view = view2
        await interaction.response.edit_message(embed=embeds[current.page], view=view)
    async def previous_page(interaction):
        if current.page - 1 < 0:
            return
        current.page -= 1
        if current.page == 0:
            view = view1
        elif current.page < page:
            view = view2
        await interaction.response.edit_message(embed=embeds[current.page], view=view)
    back.callback = previous_page
    forward.callback = next_page
    view1 = View()
    view1.add_item(forward)
    view2 = View()
    view2.add_item(back)
    view2.add_item(forward)
    view3 = View()
    view3.add_item(back)
    if page > 1:
        await ctx.respond(embed = embeds[0], view=view1)
    else:
        await ctx.respond(embed = embeds[0])

bot.run(TOKEN)