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
