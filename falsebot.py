#    This file is part of FalseBot
#    Project Home: https://github.com/FalseAscension/FalseBot
#
#    FalseBot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    FalseBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with FalseBot.  If not, see <https://www.gnu.org/licenses/>.

from discordBot import discord_bot_connection,discord_chat_handler,opcodes
import asyncio,time,json,re,argparse

# Initialise our bot with an API token read from file 'botToken'
# See https://discordapp.com/developers/applications/ to get your own
with open('tokens', 'r') as f:
    tokens = json.loads(f.read())
bot = discord_bot_connection(**tokens)

# Initialise a chat handler object.
ch = discord_chat_handler(bot)

from contextlib import redirect_stdout
# A function decorator useful for creating a command with keyword arguments. Not yet completely polished, does the job for now,
def commandWithArgs(description, **kwargs):
    def makeWrapper(func):

        prog = kwargs.pop('name') if 'name' in kwargs else func.__name__
        parser = argparse.ArgumentParser(description=description, conflict_handler='resolve', prog=prog)
        for k,v in kwargs.items():
            parser.add_argument('--' + k, **v)

        def wrapper(message):
            args = message['content'].split(" ")[1:]
            with io.StringIO() as buf, redirect_stdout(buf):
                try:
                    args = vars(parser.parse_args(args))
                    output = buf.getvalue()
                    if len(output):
                        bot.say_in_channel(message['channel_id'], f"```{output}```") # for some reason this doesn't work? still goes to stdout...
                except SystemExit:
                    output = buf.getvalue()
                    if len(output):
                        bot.say_in_channel(message['channel_id'], f"```{output}```") # this does though??
                    return
            func(message, **args)

        return wrapper
            
    return makeWrapper

# Print when we receive a HEARTBEAT ACK opcode, mostly as an easy way to monitor that the bot is still active.
@bot.message(opcodes.HEARTBEAT_ACK)
async def heartbeat_ack_received(message):
    print(f"HEARTBEAT ACK Received at {time.time()}")

# Detect when people start playing 'Fortnite' and tell them it's illegal.
#@bot.dispatch('PRESENCE_UPDATE')
#async def presenceUpdate(event):
#    if 'game' in event and event['game'] and 'fortnite' in event['game']['name'].lower():
#        bot.say_in_channel('370195763894157312', f"<@{event['user']['id']}> FORTNITE IS ILLEGAL.")

# Match all messages which contain 'siege' (case insensitive).
@ch.matchContent(lambda x: "siege" in x.lower())
def siege(message):
    bot.say_in_channel(message['channel_id'], "seej")

# A simple Hello, World! example.
@ch.matchContent(lambda x: 'hello falsebot' in x.lower())
def helloWorld(message):
    bot.say_in_channel(message['channel_id'], "Hello, World!")

## Bunch of image processing commands

import urllib.request,io
from PIL import Image, ImageDraw, ImageFont

# Just an easy way to take a PIL image and convert it to a file-like object.
def fileFromImage(Image, format="jpeg"):
    newfile = io.BytesIO()
    Image.save(newfile, format=format)
    newfile.seek(0)
    return newfile

# Looks through the channel buffer for a given channel for any images.
def findRecentImageInChannel(channel_id):
    url = None
    for m in reversed(ch.channelBuffer[channel_id]):
        if m and m['attachments'] and len(m['attachments']) > 0:# Dump the entire channel buffer (3 messages by default)
            url = m['attachments'][0]['url']
    if not url:
        return None

    req = urllib.request.Request(url,data=None,
        headers={
            'User-Agent': 'Mozilla/5.0'
        })
    img = Image.open(urllib.request.urlopen(req))

    return img

# A function decorator to turn a function which takes an Image as an argument and returns a processed one into a command.
# kwargs are preserved through to the decorated function.
def imageCommand(func):
    def wrapper(message, **kwargs):
        img = findRecentImageInChannel(message['channel_id'])
        if not img:
            return bot.say_in_channel(message['channel_id'], "Sorry, I could not find a recent image to process.")
        out = func(img, **kwargs)
        return bot.send_file(message['channel_id'], fileFromImage(out, format="png"), filename="out.png")
    return wrapper

## All the image stuff above should probably be moved to a new class or discord_chat_handler at the very least


def averageOfThree(p):
    return (p[0]+p[1]+p[2])/3
def perceivedBrightness(p):
    return 0.2126*p[0] + 0.7152*p[1] + 0.0722*p[2]
brightness = perceivedBrightness

def bandw(img):
    size = img.size
    img=img.getdata()

    bandw = list(map(brightness, img))
    
    out = Image.new('L', size)
    out.putdata(bandw)

    return out
# I want to re-use this algorithm in another function, so avoid decorating it...
ch.matchContent(re.compile("^\^bandw").search)(imageCommand(bandw))

# ASCII Characters corresponding to brightness values (lookup table)
# I generated this with an external script which drew each character and averaged
# it's brightness by summing each pixel and diving by the size.
# For each value from 0-255 I then assigned an ascii character.
brightchars = [
 ' ', ' ', ' ', ' ', ' ', '~', '~', '~', '~', '~', '~', '~', '~', ':', ':', ':', 
 ':', ':', ':', ':', ':', ':', ':', '`', '`', '`', '`', '`', '`', '+', '+', '+', 
 '+', '+', '+', 'i', 'i', 'i', 'i', 'i', 'i', "'", "'", "'", "'", "'", '/', '/', 
 '/', '|', '|', '(', '(', 'r', 'x', 'x', 'l', 'l', '<', '<', '<', 'I', 'I', 'I', 
 'I', '{', '{', '{', '!', '!', 'c', 'c', 'o', 'o', '[', '[', 't', 't', 'p', 'p', 
 'n', '=', 'g', 'g', 'g', 'k', 'k', 'k', '"', '"', '1', '1', '1', '4', '4', '^', 
 '^', '^', '^', '^', '^', '^', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'A', 'A', 'A', 
 'A', 'd', 'd', 'b', 'h', 'h', '3', '3', '2', '2', '2', '7', 'U', 'U', 'V', 'V', 
 '?', '?', '?', '5', '5', '0', '0', '0', '&', '&', 'F', '9', '6', '6', 'C', 'C', 
 'E', 'E', '8', '8', '8', '8', '8', '$', '$', '$', '$', '$', '%', '%', '%', '#', 
 '#', '#', '#', '#', '#', '#', 'O', 'O', 'O', 'O', 'O', 'B', 'B', 'B', 'B', 'P', 
 'N', 'N', 'N', 'N', 'N', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 
 'R', 'R', 'R', 'R', 'R', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 
 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 
 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '@', 
 '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@']

from functools import reduce

@ch.matchContent(re.compile("^\^ascii").search)
@commandWithArgs("Convert an image to ASCII art.", name="^ascii",
            foreground={"help":"R,G,B value to use as foreground (Default 255,255,255)",
                        "default":(255,255,255), "type":lambda x: tuple(map(int, x.split(',') ) )},
            background={"help":"R,G,B value to use as background (Default 0,0,0)",
                        "default":(0,0,0), "type":lambda x: tuple(map(int, x.split(',') ) )},
            downscaling={"help":"Downscaling factor. (Default 3)",
                        "default":3, "type":float})
@imageCommand
def ascii(img, **kwargs):
    img = bandw(img)
    size = img.size

    img = img.resize((int(size[0]/kwargs['downscaling']), int(size[1]/kwargs['downscaling'])))
    size = img.size
    img = list(img.getdata())
    
    # Assign an ascii character to each pixel.
    characters = list(map(lambda b: brightchars[b], img))

    asciised = Image.new('RGB', (size[0]*10,size[1]*10), color=kwargs['background'])
    draw = ImageDraw.Draw(asciised)
    
    # Draw an image with all these ascii chars.
    for y in range(size[1]):
        for x in range(size[0]):
            index = y*size[0]+x
            draw.text((x*10 - 2.5, y*10), characters[index], fill=kwargs['foreground'])
    
    return asciised


if __name__ == "__main__":
    asyncio.run(bot.start())
