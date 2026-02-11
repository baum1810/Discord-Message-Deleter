# Discord Message Deleter

This Python script deletes your own messages from Discord DMs and guild channels using the Discord API.

## Features

* Fetches your Discord user ID automatically
* Scans all DM channels
* Scans all servers (guilds) you are in
* Finds messages sent by your account
* Deletes those messages
* Handles rate limits automatically
* Uses pagination to process large message histories

## Requirements

* Python 3.8+
* `requests` library

Install dependencies:

```bash
pip install requests
```

## Configuration

Open the script and replace:

```python
USER_TOKEN = 'xxxx'
```

with your Discord user token.

## Usage

Run the script:

```bash
python script.py
```

The script will:

1. Fetch your user ID
2. Scan all DM channels and delete your messages
3. Scan all guilds and channels and delete your messages
4. Print progress in the console

## How It Works

The script uses these Discord API endpoints:

* `/users/@me` to get your user ID
* `/users/@me/channels` to get DM channels
* `/users/@me/guilds` to get guilds
* `/guilds/{guild_id}/channels` to get channels
* `/channels/{channel_id}/messages` to fetch messages
* `/channels/{channel_id}/messages/{message_id}` to delete messages

It filters messages by author ID so only your messages are deleted.

## Rate Limit Handling

Discord enforces rate limits. This script:

* Waits between requests
* Detects HTTP 429 responses
* Retries automatically after the required delay

## Warning

Using a user token with scripts may violate Discord Terms of Service and can result in account suspension or termination. Use at your own risk.

## Security

Never share your user token. Anyone with your token has full access to your account.

## Disclaimer

This script is provided for educational purposes only. You are responsible for how you use it.

## License

MIT License
