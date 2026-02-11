import requests
import time

# Replace these value
USER_TOKEN = 'xxxx'

headers = {
    'Authorization': USER_TOKEN,
    'Content-Type': 'application/json'
}

def get_my_user_id():
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        if response.status_code == 200:
            return response.json()['id']
        else:
            print(f"Failed to fetch user ID: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching user ID: {e}")
        return None

def fetch_dm_channels():
    try:
        response = requests.get('https://discord.com/api/v9/users/@me/channels', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch DM channels: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching DM channels: {e}")
        return []

def fetch_my_message_ids(channel_id, my_id):
    message_ids = []
    last_id = None
    while True:
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=100'
        if last_id:
            url += f'&before={last_id}'
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch messages in channel {channel_id}: {response.status_code}")
                break
            messages = response.json()
            if not messages:
                break
            for msg in messages:
                if msg['author']['id'] == my_id:
                    message_ids.append(msg['id'])
            if len(messages) < 100:
                break
            last_id = messages[-1]['id']
            time.sleep(2)
        except Exception as e:
            print(f"Error fetching messages in channel {channel_id}: {e}")
            break
    return message_ids

def delete_message(channel_id, message_id):
    try:
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}'
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return True
        elif response.status_code == 429:
            retry_after = float(response.json().get('retry_after', 5)) / 1000
            print(f"Rate limited. Waiting {retry_after:.2f} seconds...")
            time.sleep(retry_after)
            return delete_message(channel_id, message_id)
        else:
            print(f"Failed to delete message {message_id} in channel {channel_id}: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error deleting message {message_id} in channel {channel_id}: {e}")
        return False

def fetch_my_guilds():
    try:
        response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch guilds: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching guilds: {e}")
        return []

def fetch_guild_channels(guild_id):
    try:
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch channels for guild {guild_id}: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching channels for guild {guild_id}: {e}")
        return []



def main():
    my_id = get_my_user_id()
    if not my_id:
        return
    print(f"My User ID: {my_id}")
    dm_channels = fetch_dm_channels()
    print(f"Found {len(dm_channels)} DM channels.")
    for channel in dm_channels:
        channel_id = channel['id']
        print(f"\nProcessing DM channel: {channel_id}")
        message_ids = fetch_my_message_ids(channel_id, my_id)
        print(f"Found {len(message_ids)} messages to delete in this DM.")
        for i, msg_id in enumerate(message_ids, 1):
            print(f"Deleting message {i}/{len(message_ids)} in DM {channel_id}")
            if delete_message(channel_id, msg_id):
                print(f"Deleted message {msg_id}")
            time.sleep(2)

    guilds = fetch_my_guilds()
    print(f"\nFound {len(guilds)} guilds.")
    for guild in guilds:
        guild_id = guild['id']
        print(f"\nProcessing guild: {guild_id}")
        channels = fetch_guild_channels(guild_id)
        print(f"Found {len(channels)} channels in this guild.")
        for channel in channels:
            channel_id = channel['id']
            print(f"\nProcessing channel: {channel_id} in guild {guild_id}")
            message_ids = fetch_my_message_ids(channel_id, my_id)
            print(f"Found {len(message_ids)} messages to delete in this channel.")
            for i, msg_id in enumerate(message_ids, 1):
                print(f"Deleting message {i}/{len(message_ids)} in channel {channel_id}")
                if delete_message(channel_id, msg_id):
                    print(f"Deleted message {msg_id}")
                time.sleep(2)

main()
