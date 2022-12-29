# job-board
Job board for awesome jobs. Streams data from a specific channel and posts it somewhere.

## Approved channels
The bot will only stream data from channels that have been approved. Incoming content must be in the list in `discord-channels.csv`. The `guild.id` and `channel.id` are required and must be in a sha256 hash format.

## Python dev setup
Set up a virtual environment by running
```
python3 -m virtualenv .
```
This will initalize a virtual environment in this directory.

To enter the virtual environment, run
```
source bin/activate
```

To install library dependencies, run
```
pip install -r requirements.txt
```

## Bot tokens
A token for the bot can be retrieved from the [Discord Developer Applications panel](https://discord.com/developers/applications/). You may save it to a file named `config.json`, styled like so:
```
{
    "discord_bot_token":"<bot_token>"
}
```
This page has more info on how to add the bot to the server: [https://discordpy.readthedocs.io/en/stable/discord.html](https://discordpy.readthedocs.io/en/stable/discord.html).

Adding the bot to your server will depend on authorizing it via the Discord OAuth2 url generated here:
`https://discord.com/api/oauth2/authorize?client_id=928752486817341460&response_type=code&scope=messages.read`


## Deploying

Set up the dependencies:
```
sudo apt update -y && sudo apt-upgrade -y;
sudo apt install python3-pip
python3 -m pip install -r requirements.txt
```