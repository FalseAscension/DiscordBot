# DiscordBot

DiscordBot is an Asynchronous, Modular Python port of the Discord Websocket Gateway API (with limited support for the RESTful API).
See https://discordapp.com/developers/docs/topics/gateway for the specification.

This project is very much in development and in no way polished. If you find a bug or think of an improvement, feel free to submit a pull request.

## Requirements

This project uses Python 3.5 or later with the asyncio and aiohttp modules.
Install these with:
```
pip install asyncio aiohttp
```

You will need a Discord Bot Token in order to connect.
Get one from https://discordapp.com/developers/applications/

## Documentation

See the main 'discordBot.py' internal commentary for complete documentation.

## Demo

Included is a quick demo program 'hello.py'.
To set up, first put your Bot Token into file 'botToken' in the project directory.
```
echo "....." > botToken
```

You will need to add your bot to a server to start. 'Manage Server' permissions is required for this. See https://discordapp.com/developers/docs/topics/oauth2#bots for information on adding to a server.

Next, simply run 'hello.py':
```
python hello.py
```

Your bot should appear online and spit some information about the Guilds it is in into the console.
Upon receiving a message containing "TF2", the bot should respond "TF2 is ILLEGAL in this server".
For any messages containing "siege", the bot should respond "seej".
