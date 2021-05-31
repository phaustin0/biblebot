# import necessary modules
import discord
from discord.ext import commands
import json
import settings
import os

# token of bot (you will never know what it is)
token = settings.token

# define books and their respective short forms and indices
books = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "1Samuel", "2Samuel",
         "1Kings", "2Kings", "1Chronicles", "2Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms",
         "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel",
         "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
         "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1Corinthians", "2Corinthians", "Galatians",
         "Ephesians", "Philippians", "Colossians", "1Thessalonians", "2Thessalonians", "1Timothy", "2Timothy",
         "Titus", "Philemon", "Hebrews", "James", "1Peter", "2Peter", "1John", "2John", "3John", "Jude",
         "Revelations"]

books_short = ["Gen", "Ex", "Lev", "Num", "Deu", "Jos", "Jud", "Ruth", "1Sam", "2Sam",
               "1Ki", "2Ki", "1Chr", "2Chr", "Ezra", "Neh", "Est", "Job", "Ps",
               "Pro", "Ecc", "Song", "Isa", "Jer", "Lam", "Eze", "Dan",
               "Hos", "Joel", "Amos", "Oba", "Jonah", "Micah", "Nah", "Hab", "Zep", "Hag", "Zec",
               "Mal", "Mat", "Mk", "Lk", "Jn", "Acts", "Rom", "1Cor", "2Cor", "Gal",
               "Eph", "Phil", "Col", "1Thes", "2Thes", "1Tim", "2Tim",
               "Titus", "Phmn", "Heb", "Jam", "1Pet", "2Pet", "1Jn", "2Jn", "3Jn", "Jude",
               "Rev"]


# adding books to a list
book_index = {}

for i in range(len(books)):
    book_index[books[i]] = i + 1
for i in range(len(books_short)):
    book_index[books_short[i]] = i + 1


# find path to verses.json no matter what system bot.py is run on
src_dir = os.path.dirname(os.path.abspath(__file__))
bible_dir = os.path.join(src_dir, "bible_verses")
verse_path = os.path.join(bible_dir, "verses.json")


# load the bible.json
with open(verse_path, "r") as f:
    bible = json.load(f)

# list of all the verses
verses = bible["resultset"]["row"]

# creation of bot
bot = commands.Bot(command_prefix=".")

# remove default help command to facilitate custom help command
bot.remove_command("help")


# manipulate reference given to make it easier to pull verses from json file
def parse_reference(ref):
    # Should contain the list of all the verses
    verses_list = []

    # Temporary List
    temp_list = []

    data = ref.split(":")
    if len(data) != 2:
        # this means something went wrong
        return None

    book = data[0]
    verses = data[1]

    # manipulation happening right here
    temp_list = verses.split(",")
    for v in temp_list:
        if "-" not in v:
            verses_list.append(int(v))
        else:
            lower = v.split("-")[0]
            upper = v.split("-")[1]
            for i in range(int(lower), int(upper) + 1):
                verses_list.append(i)

    return ["".join(book.split(" ")[:-1]), int(book.split(" ")[-1]), verses_list]


# print ready to console to signal its readiness and change status
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Bible"))
    print("ready")


# check for errors and send an error message to help user understand the commands
@bot.event
async def on_command_error(ctx, error):
    # if user typed unknown command
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "Command not found. Please type `.help` for existing commands or check your spelling."
        )

    # if user missed a parameter
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "There is a missing parameter. Please type in the required parameter."
        )


# useless command nobody should know about
@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)


# bulk of the bot. returns bible verses
@bot.command()
async def kjv(ctx, *, ref):

    # manipulate reference
    ref = parse_reference(ref)

    # looks in every verse in the json file
    for verse in verses:

        # look for the book
        if book_index[ref[0]] == verse["field"][1]:

            # look for the chapter
            if ref[1] == verse["field"][2]:

                # print out every verse stated
                for j in ref[2]:
                    if j == verse["field"][3]:
                        b = books[book_index.get(ref[0]) - 1]
                        if b[0] == "1" or b[0] == "2" or b[0] == "3":
                            b = f"{b[:1]} {b[1:]}"
                        await ctx.send(
                            f"`{b} {str(verse['field'][2])}:{str(verse['field'][3])}`"
                        )
                        await ctx.send(f"> {str(verse['field'][4])}")


# custom help command in case of need
@bot.command()
async def help(ctx):
    await ctx.send(
        "This bot prints out the bible verse. To print out a bible verse, use this command -> `.kjv {book chapter:verses}`"
    )
    await ctx.send(
        "You can type out full name of book, or use the short form. To find compatible short forms, type this -> `.short {book}`"
    )


# tells user the short form of the book in case the book name is too long or easily misspelled
@bot.command()
async def short(ctx, *, ref):

    # remove spaces to help match easier
    if " " in ref:
        string = ""
        r = ref.split(" ")
        for i in r:
            string += f"{i}"
            ref = string
    index = book_index[ref]

    # add back the spaces
    l = ref
    s = books_short[index - 1]

    if l[0] == "1" or l[0] == "2" or l[0] == "3":
        l = f"{l[:1]} {l[1:]}"
    if s[0] == "1" or s[0] == "2" or s[0] == "3":
        s = f"{s[:1]} {s[1:]}"

    await ctx.send(f"{l} -> {s}")


# actually run the bot (with the token you will never know)
bot.run(token)
