#    This file is part of DiscordBot
#    Project Home: https://github.com/FalseAscension/DiscordBot
#
#    DiscordBot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    DiscordBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with DiscordBot.  If not, see <https://www.gnu.org/licenses/>.

from discordBot import discord_bot_connection,discord_chat_handler,opcodes
import asyncio,re

# Initialise our bot with an API token read from file 'botToken'
# See https://discordapp.com/developers/applications/ to get your own
with open("botToken", 'r') as f:
    botToken = f.readline().strip()
bot = discord_bot_connection(botToken)

# Example of a registered dispatch function.
# Wait until a guild becomes available and print a list of members and channels
# TODO clean this up a bit.
@bot.dispatch('GUILD_CREATE')
async def guild_create(guild):
    gid = guild['id'] 
    print("Guild available: %s (%s)" % (gid, guild['name']))

    if 'member_count' in guild and 'members' in guild and 'channels' in guild:
        
        # Print out all members in guild
        print("Received %i members: " % len(guild['members']))
        for member in guild['members']:
            user = member['user']
            if 'nick' not in member:
                member['nick'] = user['username']
            if member['nick'] is None:
                member['nick'] = user['username']
            print("Member: %s (ID: %s, USERNAME: %s, TAG: %s) %s" % (member['nick'], user['id'], user['username'], user['discriminator'], ("(BOT)" if 'bot' in user and user['bot'] else "")))

        # Print out all channels in guild
        print("Received %i channels: " % len(guild['channels']))
        for channel in guild['channels']:
            print("Channel: %s (ID: %s TYPE: %i)" % (channel['name'], channel['id'], channel['type']))

## Example of a registered message function.
@bot.message(opcodes.HEARTBEAT_ACK)
async def heartbeat_ack(message):
    print("Heartbeat ACK received.")


# Initialise a chat handler object
ch = discord_chat_handler(bot)

# Match all messages which match regex search.
# Regex: any string containing 'TF2'
# TODO put in a more complex example.
@ch.match(re.compile('TF2').search)
async def tf2(message):
    await bot.say_in_channel(message['channel_id'], "TF2 is ILLEGAL in this server")

# Match all messages which contain 'siege'
@ch.match((lambda x: "siege" in x))
async def siege(message):
    await bot.say_in_channel(message['channel_id'], "seej")

if __name__ == "__main__":
    asyncio.run(bot.start())
