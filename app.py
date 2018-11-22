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
import asyncio,time,json

# Initialise our bot with an API token read from file 'botToken'
# See https://discordapp.com/developers/applications/ to get your own
with open('tokens', 'r') as f:
    tokens = json.loads(f.read())
bot = discord_bot_connection(**tokens)

# Initialise a chat handler object.
ch = discord_chat_handler(bot)

# Print when we receive a HEARTBEAT ACK opcode, mostly as an easy way to monitor that the bot is still active.
@bot.message(opcodes.HEARTBEAT_ACK)
async def heartbeat_ack_received(message):
    print(f"HEARTBEAT ACK Received at {time.time()}")

async def messageAtInterval(channel_id, message, interval):
    while True:
        bot.say_in_channel(channel_id, message)
        await asyncio.sleep(interval)

# A command to store and periodically send a message to a channel.
@ch.matchContent(lambda x: x.startswith("^attach"))
def attachInterval(message):
    args = message['content'].split(' ')[1:]
    if len(args) < 3:
        return bot.say_in_channel(message['channel_id'], "Invalid Syntax. Syntax: ^attach [interval] [units] [message]")
    if not args[0].isdigit():
        return bot.say_in_channel(message['channel_id'], "Invalid Syntax. Syntax: ^attach [interval] [units] [message]")
    if args[1].lower() not in ["seconds", "minutes", "hours", "days"]:
        return bot.say_in_channel(message['channel_id'], "units must be one of: seconds, minutes, hours, days")
    interval = -1
    if args[1].lower() == "seconds":
        interval = int(args[0])
    elif args[1].lower() == "minutes":
        interval = int(args[0]) * 60
    elif args[1].lower() == "hours":
        interval = int(args[0]) * 3600
    elif args[1].lower() == "days":
        interval = int(args[0]) * 86400
    bot.say_in_channel(message['channel_id'], f"Attaching message: '{' '.join(args[2:])}' to be sent every {' '.join(args[0:2])} ({interval}s)")
    asyncio.ensure_future(messageAtInterval(message['channel_id'], ' '.join(args[2:]), interval))

# Detect when people start playing 'Fortnite' and tell them it's illegal.
@bot.dispatch('PRESENCE_UPDATE')
async def presenceUpdate(event):
    if 'game' in event and event['game'] and 'fortnite' in event['game']['name'].lower():
        bot.say_in_channel('370195763894157312', f"<@{event['user']['id']}> FORTNITE IS ILLEGAL.")

# Dump the entire channel buffer (3 messages by default)
@ch.matchContent(lambda x: x.startswith('^bufferdump'))
def bufferDump(message):
    bot.say_in_channel(message['channel_id'], "Dumping buffer...")
    for m in ch.channelBuffer[message['channel_id']]:
        if m:
            bot.say_in_channel(message['channel_id'], m['content'])

# A command to make the bot say something whenever it hears something. This could be better.
@ch.matchContent(lambda x: x.lower().startswith("^callandresponse") or x.lower().startswith("^car"))
def callAndResponse(message):
    messages = ' '.join(message['content'].split(' ')[1:]).split(';')
    matcher = lambda x: messages[0] in x.lower()
    bot.say_in_channel(message['channel_id'], f"Okay, I will say '{messages[1]}' whenever I hear '{messages[0]}'")
    ch.register_match(matcher, (lambda msg: bot.say_in_channel(msg['channel_id'], messages[1])))

# A simple Hello, World! example.
@ch.matchContent(lambda x: 'hello falsebot' in x.lower())
def helloWorld(message):
    bot.say_in_channel(message['channel_id'], "Hello, World!")

# Match all messages which contain 'siege' (case insensitive).
@ch.matchContent(lambda x: "siege" in x.lower())
def siege(message):
    bot.say_in_channel(message['channel_id'], "seej")

if __name__ == "__main__":
    asyncio.run(bot.start())
