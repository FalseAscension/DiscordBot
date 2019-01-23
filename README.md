# FalseBot

FalseBot is an Asynchronous, Modular Python port of the Discord Websocket Gateway API (with limited support for the RESTful API).

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

Included is a demo program 'falsebot.py'.

To set up, first put your Bot Token into file 'botToken' in the project directory.
```
echo "....." > botToken
```

You will need to add your bot to a server to start. 'Manage Server' permissions is required for this. See https://discordapp.com/developers/docs/topics/oauth2#bots for information on adding to a server.

Next, simply run 'falsebot.py':
```
python3.7 falsebot.py
```

Your bot should appear online and spit some information about the Guilds it is in into the console.

For any messages containing "siege", the bot should respond "seej".
The bot will reply to "hello falsebot" with "Hello, World!

Included at the later end of the file are the start of some image processing functions. 
In this version I am just playing around, and once I have something polished enough I will likely merge some of the decorators and utility functions into their own class.
