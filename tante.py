import discord
from discord.ext import commands, tasks
from itertools import cycle
from pprint import pprint
import random
import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import copy
import config

MYAUTHORID = 
MYAUTHORROLE = 

bot = commands.Bot(command_prefix = '.')

status = cycle(['Updating in 60s','Updating in 55s','Updating in 50s','Updating in 45s','Updating in 40s','Updating in 35s','Updating in 30s','Updating in 25s','Updating in 20s','Updating in 15s','Updating in 10s', 'Updating in 5s','Updating now..'])

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    change_status.start()
    #checklists.start()

def tante_id(ctx):
    return ctx.author.id == MYAUTHORID
    #return ctx.author.roles == MYAUTHORROLE

def organizer_id(ctx):
    return ctx.author.id == MYAUTHORID
    #return ctx.author.roles == MYAUTHORROLE

@bot.command(pass_context = True)
@commands.has_role('start')
async def peng(ctx):
    await ctx.send(f'pong! {round(bot.latency * 1000)}ms')


@commands.check(tante_id)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


###################################################################################
##############################       MC 01           ##############################
###################################################################################

@bot.command(aliases=['mcs01', 'mcsr1', 'MC1', 'MCSR1', 'mc', 'mcsr', 'MC', 'MCSR'])
@commands.has_role('Organizer')
async def mc1(ctx):
    #delete commmand message
    await ctx.channel.purge(limit=1)
    # initial hook up to google api and find spreadsheet
    # store data in old_list
    scope2 = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds2 = ServiceAccountCredentials.from_json_keyfile_name("./creds.json", scope2)
    gsclient2 = gspread.authorize(creds2)
    sheet2 = gsclient2.open("FILE_NAME_HERE").worksheet("WORKSHEET_NAME_HERE")
    old_list2 = []
    itemlist2 = []
    itemrange = sheet2.col_values(1)

    #post a discord embed to be edited with information in loops below
    embed = discord.Embed(title="Click Here to Softreserve", url="https://forms.gle/jvgsXaix4HJht7a68", description="", colour=discord.Color.blue())
    msg = await ctx.send(embed=embed)


    async def bot_update():
        await bot.wait_until_ready()
        while not bot.is_closed():
            #hook up to google api and find spreadsheet
            embed = discord.Embed(title="Click Here to register", url="GOOGLE_FORMS_URL_HERE", description="Insert Description Here", colour=discord.Color.blue())
            embed.set_author(name="Tante's Bot - Register to Google Sheets", url="GOOGLE_FORMS_URL_HERE", icon_url="https://logo.com/MYICON.png")
            embed.set_footer(text="Google Sheets to Discord bot made by @ADDEP")
            scope2 = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
            creds2 = ServiceAccountCredentials.from_json_keyfile_name("./creds.json", scope2)
            gsclient2 = gspread.authorize(creds2)
            sheet2 = gsclient2.open("FILE_NAME_HERE").worksheet("WORKSHEET_NAME_HERE")
            itemlist2 = sheet2.get_all_values()
            itemrange = len(sheet2.col_values(1))

            items2 = {}
            for i in range(2,itemrange):
                    if itemlist2[i][1] not in items2.keys():
                        items2[itemlist2[i][1]] = [itemlist2[i][3]]
                    else:
                        items2[itemlist2[i][1]].append(itemlist2[i][3])
            for item2 in items2:
                person2 = items2[item2]
                persons2 = []
                for person2 in person2 :
                    persons2.append(person2)
                persons2 = ('\n'.join(map(str, persons2)))
                embed.add_field(name="__**{}**__".format(item2), value=persons2, inline=True)
            await asyncio.sleep(60)
            await msg.edit(embed=embed)
    sr_update2 = bot.loop.create_task(bot_update())
