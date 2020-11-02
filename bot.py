import discord
from discord.ext import commands
import json
from src import settings

token = settings.token

# define books and their respective indices
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
               "Eph", "Philippians", "Col", "1Thes", "2Thes", "1Tim", "2Tim",
               "Titus", "Phmn", "Heb", "Jam", "1Pet", "2Pet", "1Jn", "2Jn", "3Jn", "Jude",
               "Rev"]


# adding books to list
book_index = {}

for i in range(len(books)):
    book_index[books[i]] = i + 1
for i in range(len(books_short)):
    book_index[books_short[i]] = i + 1


# load the bible.json
with open('./bible_verses/verses.json', 'r') as f:
    bible = json.load(f)

verses = bible['resultset']['row']

bot = commands.Bot(command_prefix='.')

bot.remove_command('help')


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


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Bible"))
    print('ready')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found. Please type `.help` for existing commands or check your spelling.')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('There is a missing parameter. Please type in the required parameter.')


@bot.command(help='Clears a default amount of 5 messages if not specified.')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)


@bot.command(help='Prints out a specified Bible verse.')
async def kjv(ctx, *, ref):
    ref = parse_reference(ref)
    for verse in verses:
        if book_index[ref[0]] == verse['field'][1]:
            if ref[1] == verse['field'][2]:
                for j in ref[2]:
                    if j == verse['field'][3]:
                        b = books[book_index.get(ref[0]) - 1]
                        if b[0] == '1' or b[0] == '2' or b[0] == '3':
                            b = f'{b[:1]} {b[1:]}'
                        await ctx.send(f"`{b} {str(verse['field'][2])}:{str(verse['field'][3])}`")
                        await ctx.send(f"> {str(verse['field'][4])}")


@bot.command()
async def help(ctx):
    await ctx.send('This bot prints out the bible verse. To print out a bible verse, use this command -> `.kjv {book chapter:verses}`')
    await ctx.send('You can type out full name of book, or use the short form. To find compatible short forms, type this -> `.short {book}`')


@bot.command()
async def short(ctx, *, ref):
    if ' ' in ref:
        string = ''
        r = ref.split(' ')
        for i in r:
            string += f'{i}'
            ref = string
    index = book_index[ref]
    await ctx.send(f'{ref} -> {books_short[index - 1]}')

bot.run(token)
