import asyncio
from code import interact
from doctest import debug_script
import math
from tabnanny import check
import time
import datetime
import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.commands import Option
from sqlalchemy import desc
from config import *
from commands.inventory import *
from commands.summon import *
from ellia_token import TOKEN

class currentPage():
    def __init__(self):
        self.page = 0

test_server = ["976120059598610462"]
cd = time.time()
guild_cd = {}

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

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
    with open('Users/user_log.txt', 'a') as log :
        now = datetime.datetime.now()
        log.write(f"[{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}] [{ctx.author.id}]{ctx.author.name} used : /news\n")
        log.close()
    embed = discord.Embed(title="**[Changelog] Ellia **", description="Dernières modifications : **20/07/2022**", color=discord.Color.from_rgb(0, 255, 166))
    embed.add_field(name=f'[v0.6]', inline=False, value=f'- Différenciation entre un New et un Dupe\n- Ajout de la commande pour consulter son bestiaire **/box**')
    embed.add_field(name=f'[v0.7]', inline=False, value=f'- Ajout de plusieurs filtres pour le bestiaire (élément, grade, invocateur)')
    embed.add_field(name=f'[v0.8]', inline=False, value=f'- Ajout d\'un journal de de modifications **/news**\n- N\'affiche plus **Dupe** lors que t\'obtiens un dupe')
    embed.add_field(name=f'[v0.9]', inline=False, value=f'- Options pour afficher uniquement les L&D ou élementaires **/box**\n- Pagination pour voir le bestiaire entier\n- Numérotation des pages\n- Problème de pagination résolu')
    embed.add_field(name=f'[v0.10]', inline=False, value=f'- Apparition d\'étincelle lors des summons\n- Résolution d\'un problème de la commande **/box**')
    embed.add_field(name=f'[v0.11]', inline=False, value=f'- Ajout de la commande **gamble**, voir /help pour en savoir plus\n  - On peut maintenant écrire le nom des monstres sans majuscules')
    embed.add_field(name=f'[En développement]', inline=False, value=f'- Différents types d\'affichage pour le bestiaire')
    path = "assets/changelog.png"
    file = discord.File(path, filename="image.png")
    embed.set_thumbnail(url = "attachment://" + "image.png")
    await ctx.respond(embed = embed, file=file)

@bot.slash_command(name='help', description='Tout savoir sur Ellia')
async def help(ctx):
    with open('Users/user_log.txt', 'a') as log :
        now = datetime.datetime.now()
        log.write(f"[{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}] [{ctx.author.id}]{ctx.author.name} used : /help\n")
        log.close()
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
    ldls = "<:ellia_ldls:981189545846513734>"
    embed.add_field(name=f"/gamble : Quitte ou double 🎲", inline=False, value=f"Choisi un 5{star} light & dark, t'as **60%** de chance de le perdre et **40%** de chance d'en invoquer un autre {ldls}")
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/976377270740594698/979331411834187806/help.png")
    await ctx.respond(embed = embed)

@bot.slash_command(name='gamble', description='Sois tu perds ton LD, soit t\'en invoques un autre')
@commands.cooldown(1, 5, commands.BucketType.user)
async def gamble(ctx, mob_ld: Option(str, "Mob à parier", required = True)): # type: ignore
    with open('Users/user_log.txt', 'a') as log:
        now = datetime.datetime.now()
        log.write(f"[{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}] [{ctx.author.id}]{ctx.author.name} used : /gamble {mob_ld}\n")
        log.close()
    roll = random.randrange(100)
    mob_ld = mob_ld.title()
    scroll = "<:ellia_ldls:981189545846513734>"
    monster = "<:ellia_monster:977122506152509440>"
    userid = str(ctx.author.id)
    check_user(userid)
    pseudo = ctx.author.display_name
    mob = summon_trans_ld()
    avatar = ctx.author.display_avatar
    check = open('Users/user_list.txt', 'r+')
    if f'{userid}\n' not in check:
        emb = discord.Embed(title = f'{pseudo} n\'a aucun monstre {monster}', color = discord.Color.dark_red(), description='')
        emb.set_thumbnail(url = avatar)    
        await ctx.respond(embed = emb)
        return
    got = check_mob(userid, mob_ld)
    if got == 1:
        await ctx.respond("Tu n\'as pas ce monstre.")
        return
    elif got == 2:
        await ctx.respond("Ce monstre n\'existe pas.")
        return
    if is_new([userid, mob]) == 0:
        new = " **(New)**"
    else:
        new = ""
    data = [userid, mob]
    couleur = discord.Color.dark_purple()
    if get_element(mob) == "[Light]\n":
        couleur = discord.Color.from_rgb(255, 255, 255)
    elif get_element(mob) == "[Dark]\n":
        couleur = discord.Color.dark_purple()
    if get_element(mob_ld) != "[Light]\n" and get_element(mob_ld) != "[Dark]\n":
        await ctx.respond("Ce monstre n'est pas utilisable.")
        return
    star = "<:ellia_star:976853657540767835>"
    stars = get_grade(mob)
    stars_ld = get_grade(mob_ld)
    if stars_ld != f'{star}{star}{star}{star}{star}':
        await ctx.respond("Ce monstre n'est pas utilisable.")
        return
    embed = discord.Embed(description = f"**{pseudo}** a obtenu : \n**{mob}** {stars}{new}", color = couleur, title = f"Pari gagné avec **{mob_ld}** {scroll}")
    path = "assets/Monsters/Units/" + mob + ".jpg"
    file = discord.File(path, filename="image.png")
    embed.set_thumbnail(url = "attachment://image.png")

    lose = discord.Embed(description = f"**{pseudo}** a perdu : \n**{mob_ld}** {stars}", color = couleur, title = f"Pari perdu 🎲")
    path2 = "assets/Monsters/Units/" + mob_ld + ".jpg"
    file2 = discord.File(path2, filename="ld.png")
    lose.set_thumbnail(url = "attachment://ld.png")
    if roll <= 59:
        delete_mob(userid, mob_ld)
        await ctx.respond(embed=lose, file = file2)
    else:
        save_bestiary(data)
        await ctx.defer()
        message = await ctx.send("https://tenor.com/view/summoners-war-lightning-summoners-war-lightning-summoners-war-summon-summon-gif-17920540")
        await asyncio.sleep(3)
        await message.delete()
        await ctx.respond(embed=embed, file = file)

class currentPage():
    def __init__(self):
        self.page = 0

@bot.slash_command(name='box', description='Affiche le bestiaire')
async def box(ctx, name: Option(discord.Member, "Nom de l'invocateur", required = False, default = ''), # type: ignore
element: Option(str, "Choisir un élément", required = False, default="", choices=["[Fire]\n", "[Wind]\n", "[Water]\n", "[Light]\n", "[Dark]\n", "Light & Dark", "Elementaires"]), # type: ignore
grade: Option(str, "Choisir un grade", required = False, default="", choices = ["3", "4", "5"])): # type: ignore
    with open('Users/user_log.txt', 'a') as log :
        now = datetime.datetime.now()
        log.write(f"[{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}] [{ctx.author.id}]{ctx.author.name} used : /box {name} {element} {grade}\n")
        log.close()
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
    no_mob = discord.Embed(title = f'Aucun monstre trouvé pour {user} {monster}', color=discord.Color.dark_red(), description='')
    no_mob.set_thumbnail(url = avatar)    
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
    if page == 0 and item == 0:
        await ctx.respond(embed = no_mob)
        return
    if item <= 21 and item != 0:
        embeds.append(emb)
        page += 1
    back = Button(label="", style=discord.ButtonStyle.green, emoji="⏪")
    forward = Button(label="", style=discord.ButtonStyle.green, emoji="⏩")
    async def next_page(interaction):
        if interaction.user.id != ctx.author.id:
            return
        if current.page + 1 >= page:
            return
        current.page += 1
        if current.page == page - 1:
            view = view3
        elif current.page < page:
            view = view2
        await interaction.response.edit_message(embed=embeds[current.page], view=view)
    async def previous_page(interaction):
        if interaction.user.id != ctx.author.id:
            return
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
    await ctx.defer()
    if page > 1:
        await ctx.respond(embed = embeds[0], view=view1)
    else:
        await ctx.respond(embed = embeds[0])

@bot.slash_command(name='vl', description='Utilise un vélin légendaire (toutes les 10 minutes)')
@commands.cooldown(1, 600, commands.BucketType.user)
async def velin_legendaire(ctx):
    with open('Users/user_log.txt', 'a') as log :
        now = datetime.datetime.now()
        log.write(f"[{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}] [{ctx.author.id}]{ctx.author.name} used : /vl\n")
        log.close()
    scroll = "<:ellia_vl:976796784900853771>"
    star = "<:ellia_star:976853657540767835>"
    userid = str(ctx.author.id)
    check_user(userid)
    pseudo = ctx.author.display_name
    mob = summon_vl()
    new = ""
    if is_new([userid, mob]) == 0:
        new = " **(New)**"
    data = [userid, mob]
    save_bestiary(data)
    couleur = discord.Color.red()
    if get_element(mob) == "[Fire]\n":
        couleur = discord.Color.red()
    if get_element(mob) == "[Water]\n":
        couleur = discord.Color.blue()
    if get_element(mob) == "[Wind]\n":
        couleur = discord.Color.orange()
    stars = get_grade(mob)
    embed = discord.Embed(description = f"**{pseudo}** a obtenu : \n**{mob}** {stars}{new}", color = couleur, title = f"Invocation légendaire {scroll}")
    path = "assets/Monsters/Units/" + mob + ".jpg"
    file = discord.File(path, filename="image.png")
    embed.set_thumbnail(url = "attachment://" + "image.png")
    await ctx.defer()
    if stars == f'{star}{star}{star}{star}{star}':
        message = await ctx.send("https://tenor.com/view/summoners-war-lightning-summoners-war-lightning-summoners-war-summon-summon-gif-17920540")
        await asyncio.sleep(3)
        await message.delete()
        await ctx.respond(embed=embed, file = file)
    else:
        await ctx.respond(embed = embed, file = file)

@bot.slash_command(name='trans_ld', description='Commande VIP hehe (15 minutes)')
@commands.cooldown(1, 900, commands.BucketType.user)
async def velin_ld_trans(ctx):
    with open('Users/user_log.txt', 'a') as log :
        now = datetime.datetime.now()
        log.write(f"[{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}] [{ctx.author.id}]{ctx.author.name} used : /trans_ld\n")
        log.close()
    vip = VIP
    if ctx.author.id not in vip:
        await ctx.respond(f'Tu peux pas faire la commande erf')
        return
    scroll = "<:ellia_ldls:981189545846513734>"
    star = "<:ellia_star:976853657540767835>"
    userid = str(ctx.author.id)
    check_user(userid)
    pseudo = ctx.author.display_name
    mob = summon_trans_ld()
    if is_new([userid, mob]) == 0:
        new = " **(New)**"
    else:
        new = ""
    data = [userid, mob]
    save_bestiary(data)
    couleur = discord.Color.dark_purple()
    if get_element(mob) == "[Light]\n":
        couleur = discord.Color.from_rgb(255, 255, 255)
    if get_element(mob) == "[Dark]\n":
        couleur = discord.Color.dark_purple()
    stars = get_grade(mob)
    embed = discord.Embed(description = f"**{pseudo}** a obtenu : \n**{mob}** {stars}{new}", color = couleur, title = f"Invocation light and dark {scroll}")
    path = "assets/Monsters/Units/" + mob + ".jpg"
    file = discord.File(path, filename="image.png")
    embed.set_thumbnail(url = "attachment://" + "image.png")
    await ctx.defer()
    if stars == f'{star}{star}{star}':
        await ctx.respond(embed = embed, file = file)
    else:
        message = await ctx.send("https://tenor.com/view/summoners-war-lightning-summoners-war-lightning-summoners-war-summon-summon-gif-17920540")
        await asyncio.sleep(3)
        await message.delete()
        await ctx.respond(embed=embed, file = file)

@bot.slash_command(name='ld', description='Utilise un vélin light & dark (toutes les 5 minutes)')
@commands.cooldown(1, 300, commands.BucketType.user)
async def velin_ld(ctx):
    with open('Users/user_log.txt', 'a') as log :
        now = datetime.datetime.now()
        log.write(f"[{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}] [{ctx.author.id}]{ctx.author.name} used : /ld\n")
        log.close()
    scroll = "<:ellia_ld:976796844925546566>"
    star = "<:ellia_star:976853657540767835>"
    userid = str(ctx.author.id)
    check_user(userid)
    pseudo = ctx.author.display_name
    mob = summon_ld()
    if is_new([userid, mob]) == 0:
        new = " **(New)**"
    else:
        new = ""
    data = [userid, mob]
    save_bestiary(data)
    couleur = discord.Color.dark_purple()
    if get_element(mob) == "[Light]\n":
        couleur = discord.Color.from_rgb(255, 255, 255)
    if get_element(mob) == "[Dark]\n":
        couleur = discord.Color.dark_purple()
    stars = get_grade(mob)
    embed = discord.Embed(description = f"**{pseudo}** a obtenu : \n**{mob}** {stars}{new}", color = couleur, title = f"Invocation light and dark {scroll}")
    path = "assets/Monsters/Units/" + mob + ".jpg"
    file = discord.File(path, filename="image.png")
    embed.set_thumbnail(url = "attachment://" + "image.png")
    await ctx.defer()
    if stars == f'{star}{star}{star}':
        await ctx.respond(embed = embed, file = file)
    else:
        message = await ctx.send("https://tenor.com/view/summoners-war-lightning-summoners-war-lightning-summoners-war-summon-summon-gif-17920540")
        await asyncio.sleep(3)
        await message.delete()
        await ctx.respond(embed=embed, file = file)

@bot.slash_command(name='trans', description='Utilise un vélin transcendance (toutes les 60 minutes)')
@commands.cooldown(1, 3600, commands.BucketType.user)
async def velin_trans(ctx):
    with open('Users/user_log.txt', 'a') as log :
        now = datetime.datetime.now()
        log.write(f"[{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}] [{ctx.author.id}]{ctx.author.name} used : /trans\n")
        log.close()
    scroll = "<:ellia_trans:976796872020721705>"
    userid = str(ctx.author.id)
    check_user(userid)
    pseudo = ctx.author.display_name
    mob = summon_trans()
    if is_new([userid, mob]) == 0:
        new = "**(New)**"
    else:
        new = ""
    data = [userid, mob]
    save_bestiary(data)
    couleur = discord.Color.default()
    if get_element(mob) == "[Fire]\n":
        couleur = discord.Color.red()
    if get_element(mob) == "[Water]\n":
        couleur = discord.Color.blue()
    if get_element(mob) == "[Wind]\n":
        couleur = discord.Color.orange()
    stars = get_grade(mob)
    embed = discord.Embed(description = f"**{pseudo}** a obtenu : \n**{mob}** {stars}{new}", color = couleur, title = f"Invocation transcendance {scroll}")
    path = "assets/Monsters/Units/" + mob + ".jpg"
    file = discord.File(path, filename="image.png")
    embed.set_thumbnail(url = "attachment://" + "image.png")
    await ctx.defer()
    await ctx.respond(embed = embed, file = file)

@bot.slash_command(name='give_jeton', description='Le créateur te donne un jeton pour parier')
async def give_jeton(ctx, name: Option(discord.Member, "Nom de l'invocateur")): # type: ignore
    with open('Users/user_log.txt', 'a') as log :
        now = datetime.datetime.now()
        log.write(f"[{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}] [{ctx.author.id}]{ctx.author.name} used : /jeton\n")
        log.close()
    if ctx.author.id != 147746286383136769:
        await ctx.respond("Arrête.")
        return
    userid = str(name.id)
    mob = "Thebae"
    data = [userid, mob]
    check_user(userid)
    save_bestiary(data)
    await ctx.respond(f"Jeton donné à **{name.display_name}**")

bot.run(TOKEN)