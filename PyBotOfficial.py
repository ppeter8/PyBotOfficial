#PyBot by anonymusprogrammer
import discord 
from discord.ext import commands 
from discord.ext.commands import Bot 
import asyncio
import chalk

global messages
messages = []

client = commands.Bot(command_prefix = '**')

#ready check

@client.event 
async def on_ready(): 
    print("PyBot is now online.")
    print("Bot name = " + client.user.name)
    print("Bot id = " + client.user.id)
    await client.change_presence(game=discord.Game(name="PythonRules"))
        
@client.event
async def on_message(message):
    global messages
    messages.append(message)

    fileID = open('interactions.txt', 'r')
    content = fileID.readlines()
    fileID.close()
    for line in content:
        trigger, response = line.split('-')
        if message.content.upper() == trigger.upper():
            await client.send_message(message.channel, response)

    await client.process_commands(message)



#pymod check

@client.command(pass_context=True, brief='Sprawdza czy jesteś PyModem.', description='Sprawdza, czy jesteś PyModem.')
async def amipymod(ctx):
    fileID = open('PyMods.txt', 'r')
    content = fileID.readlines()
    fileID.close()
    pymod=False
    for line in content:
        if ctx.message.author.id in line:
            pymod=True
    if pymod:
        await client.say('Jesteś PyModem.')
    else:
        await client.say('Nie jesteś PyModem.')


#info

@client.command(pass_context=True, brief='Pokazuje informacje o otagowanym.', description='Pokazuje nazwę, ID, status, najwyższą rolę, czas dołączenia na server otagowanego i sprawdza czy jest on PyModem.\n Komenda jedynie dla PyModów.')
async def info(ctx, user: discord.Member):
    await client.say("Nazwa otagowanego to: {}.".format(user.name))
    await client.say("ID otagowanego to: {}.".format(user.id))
    await client.say("Status otagowanego to: {}.".format(user.status))
    await client.say("Najwyższa rola otagowanego to: {}.".format(user.top_role))
    await client.say("Otagowany dołączył o: {}.".format(user.joined_at))
    fileID = open('PyMods.txt', 'r')
    content = fileID.readlines()
    fileID.close()
    pymod=False
    for line in content:
        if user.id in line:
            pymod=True
    if pymod:
        await client.say("Otagowany {}.".format('jest pymodem'))
    else:
        await client.say("Otagowany {}.".format('nie jest pymodem'))


#addpymod

@client.command(pass_context=True, brief='Dodaje otagowanego do listy PyModów.', description='Dodaje otagowanego do listy PyModów.\n Komenda jedynie dla PyModów.')
async def addpymod(ctx, user: discord.Member):
    fileID = open('PyMods.txt', 'r')
    content = fileID.readlines()
    fileID.close()
    pymod=False
    for line in content:
        if ctx.message.author.id in line:
            pymod=True
    for line in content:
        if user.id in line:
            await client.say('Otagowany już jest PyModem.')
            return
    if pymod:
        fileID = open('PyMods.txt', 'a')
        content = fileID.writelines(user.id + '\n')
        fileID.close()
        fileID = open('PyMods_n.txt', 'a')
        content = fileID.writelines(user.name + '\n')
        fileID.close()
        await client.say(user.name + ', witamy w gronie pymodów')
    else:
        await client.say('Komenda dostępna tylko dla PyModów.')


#removepymod

@client.command(pass_context=True, brief='Usuwa otagowanego z listy PyModów.', description='Usuwa otagowanego z listy PyModów.\n Komenda (obecnie) jedynie dla Twórcy.')
async def removepymod(ctx, user: discord.Member):
    if ctx.message.author.id == '477431968792051712':
        fileID = open('PyMods.txt', 'r')
        content = fileID.readlines()
        pymod=True
        for line in content:
            if user.id in line:
                pymod=False
        if pymod:
            await client.say('Otagowany nie był PyModem.')
            return
        fileID.close()
        fileID = open('PyMods.txt', 'w')
        for line in content:
            if user.id not in line:
                fileID.writelines(line)
        fileID.close()
        fileID = open('PyMods_n.txt', 'r')
        content = fileID.readlines()
        fileID.close()
        fileID = open('PyMods_n.txt', 'w')
        for line in content:
            if user.name not in line:
                fileID.writelines(line)
        fileID.close()
        await client.say(user.name + ' nie jest już dłużej PyModem')
    else:
        await client.say('Tylko twórca może korzystać z tej komendy.')


#pymodlist

@client.command(pass_context=True, brief='Wyświetla listę PyModów.', description='Wyświetla listę Pymodów.')      
async def pymodlist(ctx):
    fileID = open('PyMods_n.txt', 'r')
    content = fileID.readlines()
    fileID.close()
    await client.say('Lista Pymodów:')
    for pymod in content:
        await client.say(pymod)



#clear
        
@client.command(pass_context=True, brief='Usuwa wiadomości.', description='Usuwa wszystkie wiadomości.\n W przypadku podania liczby usuwa liczbę wiadomości.\n Komenda jedynie dla PyModów.')
async def clear(ctx, amt=0):
    global messages
    fileID = open('PyMods.txt', 'r')
    content = fileID.readlines()
    fileID.close()
    pymod=False
    for line in content:
        if ctx.message.author.id in line:
            pymod=True
            
    if pymod:
        if amt == 0:
            d_messages = messages
            for message in messages:
                await client.delete_message(message)
            messages = []
        else:
            d_messages = messages[-int(amt)-1:]
            for message in d_messages:
                await client.delete_message(message)
            messages = messages[:-int(amt)-1]
        await client.say('Usunięto ' + str(len(d_messages)-1) + ' wiadomości.')
    else:
        await client.say('Komenda dostępna tylko dla PyModów.')


#kick
        
@client.command(pass_context=True, brief='Wyrzuca otagowanego z servera.', description='Wyrzuca otagowanego z servera.\n Komenda jedynie dla PyModów.')
async def kick(ctx, user: discord.Member):
    fileID = open('PyMods.txt', 'r')
    content = fileID.readlines()
    fileID.close()
    pymod=False
    for line in content:
        if ctx.message.author.id in line:
            pymod=True
    if pymod:
        await client.say('{} posmakował buta od {}.'.format(user.name, ctx.message.author))
        await client.say('{} :boot: {}'.format(ctx.message.author, user.name))
        await client.kick(user)
    else:
        await client.say('Komenda dostępna tylko dla PyModów.')



#link
        
@client.command(pass_context=True, brief='Podaje link do servera testowego.', description='Podaje link do servera testowego, gdzie testowane są udoskonalenia do PyBota!')
async def testserver(ctx):
    await client.say('Link do serveru testowego to: https://discord.gg/KWCwpvc')



#interaction

@client.command(pass_context=True, brief='Tworzy nową interakcję.', description='Tworzy nową interakcję, przykład:\n **addinteraction rudy-to chuj\n Gdy napiszesz wiadomość rudy, bot odpowie: to chuj\n Komenda dostępna jedynie dla PyModów.')
async def addinteraction(ctx, *string):
    string=' '.join(string)
    fileID = open('PyMods.txt', 'r')
    content = fileID.readlines()
    fileID.close()
    pymod=False
    for line in content:
        if ctx.message.author.id in line:
            pymod=True
    if pymod:
        fileID = open('interactions.txt', 'r')
        content = fileID.readlines()
        fileID.close()
        for line in content:
            if string in line:
                await client.say('Interakcja już istnije.')
                return
        fileID = open('interactions.txt', 'a')
        fileID.writelines(string + '\n')
        fileID.close()
        await client.say('Interakcja została pomyśnie dodana.')
    else:
        await client.say('Komenda dostępna tylko dla PyModów.')
    

@client.command(pass_context=True, brief='Usuwa interakcję.', description='Usuwa interakcję.\n Przykład: **removeinteraction rudy-to_chuj\n Komenda jedynie dla PyModów.')
async def removeinteraction(ctx, *string):
    string=' '.join(string)
    fileID = open('PyMods.txt', 'r')
    content = fileID.readlines()
    fileID.close()
    pymod=False
    for line in content:
        if ctx.message.author.id in line:
            pymod=True
    if pymod:
        fileID = open('interactions.txt', 'r')
        content = fileID.readlines()
        fileID.close()
        cur=False
        for line in content:
            if string in line:
                cur=True
        if cur:
            fileID = open('interactions.txt', 'w')
            for line in content:
                if string not in line:
                    fileID.writelines(line)
            fileID.close()
            await client.say('interakcja została pomyślnie usunięta.')
        else:
            await client.say('Nie ma takiej interakcji.')
    else:
        await client.say('Komenda dostępna tylko dla PyModów.')


@client.command(pass_context=True, brief='Wyświetla listę interakcji.', description='Wyświetla listę interakcji.')
async def interactionlist(ctx):
    fileID = open('interactions.txt', 'r')
    content = fileID.readlines()
    fileID.close()
    for interaction in content:
        await client.say(interaction)


@client.command(pass_context=True, brief='Kontakt z twórcą.', description='Kontakt z twórcą. \nPrzykład: **contact Chcę PyModa!')
async def contact(ctx, *content):
    content=' '.join(content)
    fileID.open('Problems.txt', 'a')
    fileID.writelines(ctx.message.author.name + '\n')
    fileID.writelines(content + '\n')
    fileID.writelines('\n')
    fileID.close()








#pymod check

##fileID = open('PyMods.txt', 'r')
##content = fileID.readlines()
##fileID.close()
##pymod=False
##for line in content:
##    if ctx.message.author.id in line:
##        pymod=True





      
client.run("NDg4NDIwNTg3NzQ0NjU3NDIw.Dnb8zg.KtBqCIGM5vv0oQTkSQn1_kYoG8U")
