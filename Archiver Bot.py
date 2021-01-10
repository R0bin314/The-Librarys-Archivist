"""
Developed by R0bin77#331 on Discord.
Feel free to use this code for your own projects if you wish.
Send me a message if you have any questions.
"""


import discord
from discord.ext import commands
import time
import sys
import shutil
import isbnlib
import sqlite3
import random
import csv
import os

token="TOKEN"
client=commands.Bot(command_prefix="a!")
previous_command = ""
number_of_members=0
number_of_titles=0
titles_csv = []

path = "/home/robin/main/test-archive/"

files = []

for r, d, f in os.walk(path):
    for file in f:
        files.append(os.path.join(r, file)) #Scan for files
directory_list = []
for file in files:
    directory_list.append(file)

#Parse the CSV archive.
def csv_parse(directory):
    with open("{}".format(directory)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if row[3] == "":
                    print()
                else:
                    x=row[3].replace("\n", " ")
                    if "http" in x:
                        print()
                    else:
                        print('TITLE SPLIT FINAL: {}'.format(x))
                        line_count += 1
                        titles_csv.append(x)
        print(f'Processed {line_count} lines.')
        return titles_csv

#Update the database.
def update(titles_, author_list, title_list):
    i=0
    for title in titles_:
        print()
        print('TITLE: {}'.format(title))
        print('TITLES: {}'.format(titles_))
        print('AUTHORS: {}'.format(author_list))
        print('TITLE LIST: {}'.format(title_list))
        try:
            sqliteConnection = sqlite3.connect('/home/robin/main/Archive-Programs/The-Librarys-Archivist-linux/The-Library.db')
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            
            sqlite_insert_query = 'INSERT INTO Books (Title, Author) VALUES (\'{}\',\'{}\')'.format(title_list[i],author_list[i])
            print(sqlite_insert_query)
            i+=1
            count = cursor.execute(sqlite_insert_query)
            sqliteConnection.commit()
            print("Record inserted successfully into Books table ", cursor.rowcount)
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

"""Used to ensure that commands are used only by people with certain roles. Required parameters is author_roles (roles) and strings of the allowed roles.

INCLUDE THIS CODE AT THE TOP OF THE COMMAND FUNCTION IF YOU'RE VERIFY_USER_ROLES:
author_roles = message.author.roles
"""

def verify_user_roles(roles, *argv):
    for arg in argv:
        print(arg)
        if arg in str(roles):
            return True
    return False

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

"""
BOOK COMMANDS:
These commands are used to interact with the sqlite database and find information about books.

update_db: This command archives the server from scratch and uploads it to the database.

add: This command adds individual books to the database.

isbn: This command gives you the ISBN number of a book.
"""

@client.command()
async def update_db(message):
    author_roles = message.author.roles
    if verify_user_roles(author_roles, "Librarian", "Admin", "Head Librarian (Owner)") == True:
        await message.channel.send("Updating archive... Please don't use any commands.")
        exec(open("/home/robin/main/Archive-Programs/The-Librarys-Archivist-linux/Archive-Updater.py").read())
        await message.channel.send("The server has been archived. Updating the database... Please don't use any commands.")
        for file in directory_list:
            titles_final = csv_parse(file)
            print('Complete.')
        author_list = []
        title_list = []
        for title in titles_final:
            try:
                if "ï»¿" in title:
                    title = title.split("ï»¿")[1]
                if "by " in title:
                    author_title = title.split(" by ")
                    title_list.append(author_title[0])
                    author_list.append(author_title[1])
                else:
                    title_list.append(line)
                    author_list.append('N/A')
            except:
                print(title)
        try:
            update(titles_final, author_list, title_list)
        except IndexError:
            print('Index Error')
        finally:
            await message.channel.send("The database has been updated.")
            time.sleep(1)
            await message.channel.send("Sending a .zip of the Archive...")
            shutil.make_archive('/home/robin/main/test-archive/', 'zip', '/home/robin/main/test-archive/') 
            file = discord.File('/home/robin/main/test-archive.zip', 'Archive-Csv.zip')
            await message.channel.send("",file=file)
    else:
        await message.channel.send("You can't use this command! Please ask a librarian or admin to use this command.")

@client.command()
async def add(message, *argv):
    author_roles = message.author.roles
    if verify_user_roles(author_roles, "Head Librarian (Owner)") == True:
        
        book_arg_list = list(argv)
        print(book_arg_list)
        if len(book_arg_list) == (book_arg_list.index("by") + 1):
            await message.channel.send("Error: no author specified. If there is no author, please enter the author's name as \"N/A.\" Thank you.")
        else:
            try:
                book_title = ' '.join(book_arg_list[:book_arg_list.index("by")])
                book_author = ' '.join(book_arg_list[(book_arg_list.index("by") + 1):])
                sqliteConnection = sqlite3.connect('/home/robin/main/Archive-Programs/The-Librarys-Archivist-linux/The-Library.db')
                cursor = sqliteConnection.cursor()
                await message.channel.send("Successfully Connected to the database.")
                sqlite_insert_query = 'INSERT INTO Books (Title, Author) VALUES (\'{}\',\'{}\');'.format(book_title,book_author)
                count = cursor.execute(sqlite_insert_query)
                sqliteConnection.commit()
                await message.channel.send("Book entered into the database.")
                cursor.close()
                
            except sqlite3.Error as error:
                await message.channel.send("Failed to insert data into sqlite table. Please contact Robin. Error: {} ".format(error))
                await message.channel.send(sqlite_insert_query)
                
            finally:
                if (sqliteConnection):
                    sqliteConnection.close()
                    print("The SQLite connection is closed")
    else:
        await message.channel.send("You can't use this command! Please ask a librarian or admin to use this command.")

@client.command()
async def isbn(message, *argv):
    isbn_string_words = []
    for argument in argv:
        isbn_string_words.append(str(argument))
        isbn_string = " ".join(isbn_string_words)
    try:
        await message.channel.send("The ISBN number of {} is: {}".format(isbn_string, isbnlib.isbn_from_words(isbn_string)))
    except:
        await message.channel.send("It looks like the book you're searching for doesn't exist. Or perhaps the archive is incomplete?")

"""
MANAGERIAL COMMANDS:
These commands are for managing the bot and moderating the server.

shutdown: This command shuts down the bot. It can only be used by the Head Librarian.
kick: This command kicks a user. The syntax for this command is a!kick <user> <reason>. It can only be used by an admin or above.
ban: This command bans a user. The syntax for this command is a!ban <user> <reason>. It can only be used by an admin or above.
commands_list: This command sends the user a list of commands. You can add "admin" to the end of this command to see admin commands.
statistics: This provides statistics about the server (number of users, number of books in the database).

"""

@client.command()
async def shutdown(message):
    author_roles = message.author.roles
    if verify_user_roles(author_roles, "Head Librarian (Owner)") == True:
        print(message.author)
        print("Shutting down.")
        await message.channel.send("Shutting down...")
        sys.exit()
    else:
        print(message.author)
        logs = open("logs.txt", "a")
        logs.write("UNAUTHORIZED COMMAND (SHUT DOWN) BY " + str(message.author) + "\n")
        logs.close()
        await message.channel.send("You aren't allowed to use this command. Your attempt has been logged.")
        
@client.command()
async def kick(message, member : discord.Member, *, reason = None):
    author_roles = message.author.roles
    if verify_user_roles(author_roles, "Admin", "Head Librarian (Owner)") == True:
        if reason == None:
            reason = "No reason given."
            await message.channel.send("The user has been kicked successfully.")
            channel_dm = await member.create_dm()
            await channel_dm.send("You have been banned from The Library. No reason was given. \nIf you have any questions, please contact {}".format(message.author))
            await member.kick(reason=reason)
        else:
            if message.author == member:
                await message.channel.send(member.mention + " You can't kick yourself!")
            else:
                await message.channel.send("The user has been kicked successfully.")
                channel_dm = await member.create_dm()
                await channel_dm.send("You have been kicked from The Library. The reason given was: {}. \nIf you have any questions, please contact {}".format(reason,message.author))
                await member.kick(reason=reason)
    else:
        await message.channel.send("You can't use this command!")
        
@client.command()
async def ban(message, member:discord.Member, *, reason=None):
    author_roles = message.author.roles
    if verify_user_roles(author_roles, "Admin", "Head Librarian (Owner)") == True:
        if reason == None:
            if message.author == member:
                await message.channel.send(member.mention + " You can't ban yourself!")
            else:
                reason="No reason given."
                channel_dm = await member.create_dm()
                await channel_dm.send("You have been banned from The Library. No reason was given. \nIf you have any questions, please contact {}".format(message.author))
                await member.ban(reason=reason)
                await message.channel.send("The user has been banned successfully.")
        else:
            if message.author == member:
                await message.channel.send(member.mention + " You can't ban yourself!")
            else:
                channel_dm = await member.create_dm()
                await channel_dm.send("You have been banned from The Library. The reason given was: {}. \nIf you have any questions, please contact {}".format(reason,message.author))
                await member.ban(reason=reason)
    else:
        await message.channel.send("You can't use this command!")
        
@client.command()
async def commands_list(message, *argv):
    arg_list = [arg  for arg in argv]
    if arg_list!=[]:
        if arg_list[0].lower() == "admin": 
            await message.channel.send("""
**Admin Commands:**

**a!update_db:** *This command automatically updates the database.*

**a!add:** *This command lets you add a book to our database.*

**a!ban:** *This command bans the mentioned user. It will also send the user a DM with the reason for why they were banned. The syntax is: a!ban <user> <reason>.*

**a!kick:** *This command kicks the mentioned user. It will also send the user a DM with the reason for why they were kicked. The syntax is: a!kick <user> <reason>.*
""")
        else:
            await message.channel.send("Error: invalid parameters.")
    else:
        await message.channel.send("""
**Commands:**

**a!commands_list:** *This command sends you a list of commands.*

**a!ama:** You can ask me a question using this command.

**a!stats:** *This command send you the current number of members in the Library and number of titles in the Library. The number of titles is updated daily and the number of members is updated automatically.*

**a!desc:** *This command provides you with a description of a book given an ISBN number or title. Using ISBN is recommended since it provides a more accurate result.*

**a!isbn:** *This command provides you with the ISBN number of a book. This is not always accurate, though.*
""")

@client.command()
async def stats(message):
    try:
        sqliteConnection = sqlite3.connect('/home/robin/main/Archive-Programs/The-Librarys-Archivist-linux/The-Library.db')
        cursor = sqliteConnection.cursor()
        sqlite_insert_query = 'SELECT COUNT(*) FROM books;'
        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        rows = cursor.fetchall()
        number_of_books = rows[0][0]
        cursor.close()
        
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
            await message.channel.send('**SERVER STATISTICS:**\nNumber of users: {}\nNumber of books: {}'.format(message.guild.member_count, number_of_books))
            
"""
MISCELLANEOUS COMMANDS:
These commands are mostly for fun and don't fall under any other categories.
"""
@client.command()
async def ama(message, *argv):
    arg_list = [arg for arg in argv]
    question = " ".join(arg_list)
    await message.channel.send("**Your question:** {}".format(question))
    await message.channel.send("Thinking...")
    answers = random.randint(1,8)
    if answers == 1:
        await message.channel.send("It is certain.")
    
    elif answers == 2:
        await message.channel.send("Outlook good.")
    
    elif answers == 3:
        await message.channel.send("You may rely on it.")
    
    elif answers == 4:
        await message.channel.send("Ask again later.")
    
    elif answers == 5:
        await message.channel.send("Concentrate and ask again.")
    
    elif answers == 6:
        await message.channel.send("Reply hazy, try again.")
    
    elif answers == 7:
        await message.channel.send("My reply is no.")
    
    elif answers == 8:
        await message.channel.send("My sources say no.")
    else:
        print('Error')
        
@client.command()
async def update_status(message, *argv):
    author_roles = message.author.roles
    if verify_user_roles(author_roles, "Head Librarian (Owner)") == True:
        arg_list = [arg for arg in argv]
        await client.change_presence(activity=discord.Game(name="{}".format(" ".join(arg_list))))
    else:
        await message.channel.send("Nice try but only Robin can change my status ;)")
        
@client.command()
async def paper(message, *argv):
    arg_list = [arg  for arg in argv]
    print(arg_list)
    os.system('rm -f /home/robin/main/scihub/*')
    os.system("python3 -m PyPaperBot --doi='{}' --dwn-dir='/home/robin/main/scihub/'".format(arg_list[1]))
    shutil.make_archive('/home/robin/main/scihub/', 'zip', '/home/robin/main/scihub/') 
    file = discord.File('/home/robin/main/scihub.zip', 'paper.zip')
    await message.channel.send("Here is your paper, {}!".format(message.author.mention),file=file)
client.run(token)
