import discord
import os, sys, json
import getpass
import time
from colored import fg, bg, attr

green = fg('#4EC98F')
magenta = fg('#7D0068')
yellow = fg('#FFCC00')
red = fg('#FF0000')
white = fg('#FFFFFF')
blue = fg('#3179B1')
lavender = fg('#A074C4')
BOLD = attr('bold')
res = attr('reset')


ready = False
pending = []

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    running_mode = 'Frozen/executable'
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive (e.g. 'python myapp.py')"
    except NameError:
        application_path = os.getcwd()
        running_mode = 'Interactive'

os.system('cls' if os.name == 'nt' else 'clear')

#fp = application_path + "respectspaid.json"
#respects = 0
#with open(fp) as f_obj:
#    respects = json.load(f_obj)

if os.name == 'nt':
    application_path = application_path + "\\"
    jfile = application_path + 'settings.json'
else:
    application_path = application_path + "/"
    jfile = application_path + 'settings.json'

if os.path.exists(jfile):
    jdata = json.load(open(jfile))
else:
    jdata = open(jfile, 'w')
    jtmp = '{\n\"token\":\"Token_Here\"\n}'
    jdata.write(jtmp)
    jdata.close()
    jdata = json.load(open(jfile))

os.environ["rg"] = str(jdata['token'])
token = str(jdata['token'])

if token == "Token_Here":
    token = getpass.getpass(f"{white}What is your discord user authorization token?(You can check my github for a guide on how to get this): ")
    jdata = open(jfile, 'w')
    jtmp = '{\n"token":"'+ token +'"\n}'
    jdata.write(jtmp)
    jdata.close()
    jdata = json.load(open(jfile))

def ConvertSectoDay(n): 
    day = n // (24 * 3600) 
    n = n % (24 * 3600) 
    hour = n // 3600
    n %= 3600
    minutes = n // 60
    n %= 60
    seconds = n 
    de = ''
    if day and day != 1:
        de = de + str(day) + " days, "
    elif day:
        de = de + str(day) + " days, "
    if hour and hour != 1:
        de = de + str(hour) + " hrs, "
    elif hour:
        de = de + str(hour) + " hr, "
    if minutes and minutes != 1:
        de = de + str(minutes) + " mins, "
    elif minutes:
        de = de + str(minutes) + " min, "
    if seconds and seconds != 1:
        de = de + str(seconds) + " secs."
    elif seconds:
        de = de + str(seconds) + " sec."
    else:
        de = de + str(seconds) + " secs."
    return de

expire_after = 30
expire_purdy = ''
bot = discord.Client()

def greet_stdout(): 
    global expire_after
    global expire_purdy
    print(f"{magenta}[{time.strftime('%I:%M %p', time.localtime()).rstrip()}]{white} Connected to {lavender}{BOLD}Discord{res}{white} as user {green}{BOLD}{bot.user}{res}{white}")
    expire_after = input(f"{white}How many seconds do you want your messages to stick around for?: {BOLD}{green}")
    print(f"{res}{magenta}[{time.strftime('%I:%M %p', time.localtime()).rstrip()}]{white} Messages typed while this session is active will expire after {yellow}{BOLD}{expire_purdy}{res}{white}")

    expire_after = int(expire_after)
    expire_purdy = ConvertSectoDay(int(expire_after))

@bot.event
async def on_ready():
    global ready
    if ready == False:
        ready = True
        greet_stdout()

@bot.event
async def on_connect():
    global ready
    if ready == False:
        ready = True
        greet_stdout()

@bot.event
async def on_message(msg):
    global expire_after
    global expire_purdy
    global ready
    global pending
    if ready == False:
        ready = True
        greet_stdout()

    if msg.author == bot.user:
        pending.append(msg.id)
        await msg.edit(delete_after=expire_after)
        print(f"{magenta}[{time.strftime('%I:%M %p', time.localtime()).rstrip()}]{white} Message with ID {green}{BOLD}{msg.id}{res}{white} will expire in {yellow}{BOLD}{expire_purdy}{res}{white}")

@bot.event
async def on_raw_message_delete(msg):
    global pending
    chan = bot.get_channel(msg.channel_id)
    if msg.message_id in pending:
        pending.remove(msg.message_id)

        print(f"{magenta}[{time.strftime('%I:%M %p', time.localtime()).rstrip()}]{white} Message with ID {green}{BOLD}{msg.message_id}{res}{white} has expired and has been deleted from {blue}{BOLD}#{chan}{res}{white}.")

bot.run(token, bot=False)
