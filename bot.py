import sys
import time
import datetime
import datetime
import uuid
import json
import discord
import os
import re
import pandas as pd
import hashlib
import requests

########################################################################
# CONFIG SETUP
########################################################################
CONFIGFILE = sys.argv[1]
CONFIG = json.load(open(CONFIGFILE))

DISCORD_BOT_TOKEN = CONFIG['discord_bot_token']
SINK_URL = CONFIG['sink_url']
SINK_AUTHORIZATION = CONFIG['sink_authorization']

########################################################################
# VALIDATOR SETUP
########################################################################
df = pd.read_csv('discord-channels.csv')
APPROVED_CHANNELS = df.to_dict('records')
APPROVED_CHANNEL_COMBOS = {}
for entry in APPROVED_CHANNELS:
    APPROVED_CHANNEL_COMBOS.update({entry['guild.name']:str(entry['guild.id'])+':'+str(entry['channel.id'])}) 
del df

########################################################################
# FUNCTIONS
########################################################################

def string_to_hash(string: str) -> str:
    """
    Function to hash a string
    """
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def validator(message: discord.Message) -> bool:
    """
    Function to validate the guild:channel combos for incoming message
    """
    observed_combo = string_to_hash(str(message.guild.id))+':'+string_to_hash(str(message.channel.id))
    if observed_combo in APPROVED_CHANNEL_COMBOS.values():
        return True
    else:
        return False

def genTS() -> dict:
    """
    Function to generate a timestamp in both int and isoformat
    """
    ts = datetime.datetime.utcnow().timestamp()
    return {
        'timestamp_int': int(ts),
        'timestamp':  datetime.datetime.fromtimestamp(ts).isoformat()
    }

def genUID() -> str:
    """
    Function to generate a unique ID
    """
    return str(uuid.uuid4())

def createRecord(data: dict) -> dict:
    """
    Function to create a record
    """
    record = genTS()
    record['uid'] = genUID()
    record['record_id'] = str(record['timestamp_int']) + '-' + record['uid']
    record.update(data)
    record.update({'config': {
        'name': CONFIG['name'],
        'created_at': CONFIG['created_at'],
        'filename': CONFIGFILE
    }})
    return record

def sinkData(data: dict = {}):
    """
    Function to sink data to a location
    """
    record = createRecord(data)

    headers = {
        'apikey': SINK_AUTHORIZATION
    }
    
    response = requests.post(SINK_URL, headers=headers, juson=data)

    return response

def parse_event_message(message: discord.Message) -> dict:
    """
    Function to parse a message event
    """
    try:
        raw_mentions = message.raw_mentions
    except:
        raw_mentions = []
    try:
        raw_channel_mentions = message.raw_channel_mentions
    except:
        raw_channel_mentions = []
    try:
        raw_role_mentions = message.raw_role_mentions
    except:
        raw_role_mentions = []
    try:
        channel_mentions = message.channel_mentions
    except:
        channel_mentions = []

    channel_mentions = []
    for channel_tmp in message.channel_mentions:
        channel_container = {}
        try:
            channel_container['id'] = channel_tmp.id
        except:
            channel_container['id'] = None
        try:
            channel_container['name'] = channel_tmp.name
        except:
            channel_container['name'] = None
        try:
            channel_container['position'] = channel_tmp.position
        except:
            channel_container['position'] = None
        try:
            channel_container['nsfw'] = channel_tmp.nsfw
        except:
            channel_container['nsfw'] = None
        try:
            channel_container['news'] = channel_tmp.news
        except:
            channel_container['news'] = None
        try:
            channel_container['category_id'] = channel_tmp.category_id
        except:
            channel_container['category_id'] = None
        
        channel_mentions.append(channel_container)
    
    try:
        clean_content = message.clean_content
    except:
        clean_content = None
    try:
        created_at = message.created_at.isoformat()#.strftime('%Y-%m-%dT%H:%M:%SZ')
    except:
        created_at = None
    try:
        edited_at = message.edited_at.isoformat()#.strftime('%Y-%m-%dT%H:%M:%SZ')
    except:
        edited_at = None
    try:
        is_system = message.is_system()
    except:
        is_system = None
    try:
        system_content = message.system_content
    except:
        system_content = None
    try:
        activity = message.activity
    except:
        activity = None
    try:
        application = message.application
    except:
        application = None
    try:
        attachments = message.attachments
    except:
        attachments = []
    
    if len(attachments) > 0:
        attachment_container = []
        for attachment in attachments:
            tmp_attachment = {}
            try:
                tmp_attachment['id'] = attachment.id
            except:
                tmp_attachment['id'] = None
            try:
                tmp_attachment['filename'] = attachment.filename
            except:
                tmp_attachment['filename'] = None
            try:
                tmp_attachment['url'] = attachment.url
            except:
                tmp_attachment['url'] = None
            
            attachment_container.append(tmp_attachment)
        attachments = attachment_container
    
    author = {}
    try:
        author['id'] = message.author.id
    except:
        author['id'] = None
    try:
        author['name'] = message.author.name
    except:
        author['name'] = None
    try:
        author['discriminator'] = message.author.discriminator
    except:
        author['discriminator'] = None
    try:
        author['bot'] = message.author.bot
    except:
        author['bot'] = None
    try:
        author['nick'] = message.author.nick
    except:
        author['nick'] = None
    
    author_guild = {}
    try:
        author_guild_container = message.author.guild
        author_guild['id'] = author_guild_container.id
        author_guild['name'] = author_guild_container.name
        author_guild['shard_id'] = author_guild_container.shard_id
        author_guild['chunked'] = author_guild_container.chunked
        author_guild['member_count'] = author_guild_container.member_count
    except:
        author_guild['id'] = None
        author_guild['name'] = None
        author_guild['shard_id'] = None
        author_guild['chunked'] = None
        author_guild['member_count'] = None

    try:
        components = message.components
    except:
        components = None
    try:
        content = message.content
    except:
        content = None
    
    embeds_container = []
    for embed in message.embeds:
        try:
            embeds_container.append(embed.to_dict())
        except:
            embeds_container.append({})
    embeds = embeds_container

    try:
        flags = message.flags.value
    except:
        flags = None
    try:
        interaction = message.interaction
    except:
        interaction = None
    try:
        mention_everyone = message.mention_everyone
    except:
        mention_everyone = None
    
    mentions = []
    try:
        for member in message.mentions:
            mentions.append({'id':member.id,'content':member.content})
    except:
        pass
    
    try:
        nonce = message.nonce
    except:
        nonce = None
    try:
        pinned = message.pinned
    except:
        pinned = None
    try:
        reactions = message.reactions
    except:
        reactions = None
    
    reference = {}
    try:
        reference_message_id = message.reference.message_id
    except:
        reference_message_id = None
    try:
        reference_channel_id = message.reference.channel_id
    except:
        reference_channel_id = None
    try:
        reference_guild_id = message.reference.guild_id
    except:
        reference_guild_id = None
    reference = {
        'message_id':reference_message_id,
        'channel_id':reference_channel_id,
        'guild_id':reference_guild_id
    }
    
    role_mentions = []
    try:
        for role in message.role_mentions:
            role_mentions.append({'id':role.id,'name':role.name})
    except:
        pass

    stickers = []
    try:
        for sticker in message.stickers:
            stickers.append({'id':sticker.id,'name':sticker.name,'format':sticker.format,'url':sticker.url})
    except:
        pass
    try:
        tts = message.tts
    except:
        tts = None
    try:
        message_type = message.type._asdict()
    except:
        message_type = None
    try:
        webhook_id = message.webhook_id
    except:
        webhook_id = None
    try:
        jump_url = message.jump_url
    except:
        jump_url = None
    

    channel = {}
    try:
        channel_container = message.channel
    except:
        channel_container = None
    try:
        channel['id'] = channel_container.id
    except:
        channel['id'] = None
    try:
        channel['name'] = channel_container.name
    except:
        channel['name'] = None
    try:
        channel['position'] = channel_container.position
    except:
        channel['position'] = None
    try:
        channel['nsfw'] = channel_container.nsfw
    except:
        channel['nsfw'] = None
    try:
        channel['news'] = channel_container.news
    except:
        channel['news'] = None
    try:
        channel['category_id'] = channel_container.category_id
    except:
        channel['category_id'] = None

    guild = {}
    guild_container = message.guild
    try:
        guild['id'] = guild_container.id
    except:
        guild['id'] = None
    try:
        guild['name'] = guild_container.name
    except:
        guild['name'] = None
    try:
        guild['shard_id'] = guild_container.shard_id
    except:
        guild['shard_id'] = None
    try:
        guild['chunked'] = guild_container.chunked
    except:
        guild['chunked'] = None
    try:
        guild['member_count'] = guild_container.member_count
    except:
        guild['member_count'] = None

    try:
        message_id = message.id
    except:
        message_id = None


    return {
        'raw_mentions': raw_mentions,
        'raw_channel_mentions': raw_channel_mentions,
        'raw_role_mentions': raw_role_mentions,
        'channel_mentions': channel_mentions,
        'clean_content': clean_content,
        'created_at': created_at,
        'edited_at': edited_at,
        'is_system': is_system,
        'system_content': system_content,
        'activity': activity,
        'application': application,
        'attachments': attachments,
        'author': author,
        'author_guild': author_guild,
        'components': components,
        'content': content,
        'embeds': embeds,
        'flags': flags,
        'interaction': interaction,
        'mention_everyone': mention_everyone,
        'mentions': mentions,
        'nonce': nonce,
        'pinned': pinned,
        'reactions': reactions,
        'reference': reference,
        'role_mentions': role_mentions,
        'stickers': stickers,
        'tts': tts,
        'type': message_type,
        'webhook_id': webhook_id,
        'jump_url': jump_url,
        'channel': channel,
        'guild': guild,
        'id': message_id
    }

def extract_urls_from_content(content: str):
    """
    Extracts URLs from the message content
    """
    urls = []
    try:
        urls = re.findall(r'(https?://\S+)', content)
    except:
        pass
    return urls

########################################################################
# DISCORD CLIENT SETUP
########################################################################
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


########################################################################
# ASYNC EVENT HANDLERS
########################################################################
@client.event
async def on_message(message):
    """
    Handles the on_message event
    """
    if validator(message):
        parsed_message_event = parse_event_message(message)
        urls = extract_urls_from_content(parsed_message_event['content'])
        content_sha256 = string_to_hash(parsed_message_event['content'])
        guild_id_sha256 = string_to_hash(parsed_message_event['guild']['id'])
        channel_id_sha256 = string_to_hash(parsed_message_event['channel']['id'])
        author_id_sha256 = string_to_hash(parsed_message_event['author']['id'])
        for url in urls:
            sinkData({'url':url,'guild':guild_id_sha256,'channel': channel_id_sha256, 'author': author_id_sha256, 'content':content_sha256})


########################################################################
# MAIN RUN
########################################################################
client.run(DISCORD_BOT_TOKEN)