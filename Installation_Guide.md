<h1 align="center">
  <br>
  <img width=100% src="https://imgur.com/7s1Q7qR.png" alt="GMBot Banner">
  <br>
  Installation Guide
  <br>
</h1>

>[!Note]
>
> ***Feel free to copy this bot but make sure you mention this repository in your bot's description.***


## Step 1:

#### Fork this repository.
* If you don't yet have a Github account, [create one](https://github.com/join)! It's free and easy.
* Click [here](https://github.com/TheCarBun/GM-Bot/fork) or use the button in the upper righthand side of this page to fork the repository so that it will be associated with your Github account.


* Please **star our project** if you like it using the top-right Star icon. Every star helps us! 


## Step 2:

#### Create a new [Discord Application](https://discordapp.com/developers/applications) in the Discord Developer Portal
* Give app a friendly name and click the **Create App** button
* Scroll down to the **Bot** section
* Click the **Create a Bot User** button
* Click the **Yes, do it!** button
* Reset and copy the bot's **TOKEN**, you will need it later
* Under **Privileged Gateway Intents** enable **MESSAGE CONTENT INTENT**

## Step 3:

Invite your bot to your discord server:

* Go to OAuth2 section then Url Generator
* Under Scopes enable:
  * [x] `bot`
  * [x] `application.commands`
* Under Bot Permission enable:
  * [x] `Manage Webhooks`
  * [x] `Read Messages/View Channels`
  * [x] `Send Messages`
  * [x] `Embed Links`
  * [x] `Attach Files`
  * [x] `Read Message History`
  * [x] `Mention Everyone`
  * [x] `Use Slash Commands`

* Invite your bot to the server with the generated URL

## Step 4:

Install all requirements from [requirements.txt](requirements.txt) with
```
pip install -r requirements.txt
```
Or
<br>
Manually install the following packages:
```
pip discord.py
```

## Step 5:

```
token = "TOKEN"
bot_master = MASTER_USER_ID
gm_logo = "BOT_LOGO_URL"
gm_color = "BOT_COLOR_HEX_CODE"
on_log_ch = CHANNEL_ID
```

 Go to [config.py](src\config.py) and replace:<br>
`BOT_TOKEN` with your bot's token.<br>
`MASTER_USER_ID` with the bot manager's User ID or you own User ID<br>
`BOT_LOGO_URL` with url of your bot
s logo<br>
`BOT_COLOR_HEX_CODE`: with hex color code of your choice<br>
`CHANNEL_ID`: with Channel ID where you want to log on_ready event


## Step 6:

Run the bot
