import discord
from discord.ext import commands
import asyncio
import json
from datetime import datetime, timedelta
from discord import Embed as Embed, Color as Color
from discord.ui import Button, View, Select
from config import *

bot = commands.Bot(command_prefix=commands.when_mentioned,
                   intents=discord.Intents.all())

# ===== Events =====

# On Ready ---------
@bot.event
async def on_ready():
  ch = bot.get_channel(on_log_ch)  #gets log channel
  print("GM Bot is online!")
  redem = Embed(
    title="GM Bot is Online!",
    color=Color.from_str(gm_color),
  )
  redem.add_field(name="Bot ID :", value=f"{bot.user.id}", inline=False)
  redem.add_field(name="Bot :", value=f"{bot.user.mention}", inline=False)
  redem.add_field(name="Ping :",
                  value=f"{round(bot.latency,2)} ms",
                  inline=False)
  redem.set_thumbnail(
    url=
    "https://i.pinimg.com/originals/a9/68/27/a96827aa75c09ba6c6dcf38b8f6daa90.gif"
  )

  await ch.send(embed=redem)  #Sends in support server
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")

  except Exception as e:
    print(e)
    print(f"{bot.user} is Online!")


# -------------------------------------


# On Message ----------
# ---------- GM counter
@bot.event
async def on_message(message: discord.Message):

  user = message.author  # User
  if user.bot:  # Checks if user is a bot
    return

  user_guild = message.guild.id  # Server ID
  msg_time = datetime.now()  # Time when message was sent
  gm_msg = message.content.lower()  # Gets message
  embed = discord.Embed(title=f"GM {user.name}!",
                        color=discord.Color.from_str(gm_color))  #Base Embed
  embed.set_thumbnail(url=user.avatar.url)

  # initializing variables ...
  with open("src/gm_channel.json") as gmchjson:  #JSON Where GM Channel is stored
    gm_ch_data = json.load(gmchjson)

  gm_json_len = len(gm_ch_data)
  gm_ch_present = False
  for x in range(gm_json_len):  #Checks if the server has a GM Channel
    if message.guild.id == gm_ch_data[x]["server_id"]:
      gm_ch_present = True
      gm_index = x
      break

  if gm_ch_present:  #If there is a GM channel
    gm_ch = bot.get_channel(
      gm_ch_data[gm_index]["gm_channel"])  # initializes GM Channel

    if message.channel == gm_ch and "gm" in gm_msg:  # Checks channel and message
      with open("gm.json") as gmjson:  # Opens JSON where it stores user stats
        user_data = json.load(gmjson)

      data_len = len(user_data)
      user_not_present = False

      for x in range(data_len):  # Checks ID of all users from JSON
        if user.id == user_data[x]["user_id"] and user_data[x][
            "server_id"] == user_guild:  # Checks if user is present in JSON
          user_not_present = False
          index = x  #Saves index of the user from JSON
          break
        else:
          user_not_present = True

      if user_not_present:  # If user is not present in JSON
        new_data = {
          "server_id": user_guild,
          "user_id": user.id,
          "count": 1,
          "streak": 1,
          "last_used": msg_time.isoformat(),
          "level": 1
        }
        user_data.append(new_data)  #adds new data to JSON
        try:
          with open("gm.json", "w") as g:
            user_data = json.dump(user_data, g)  #Dumps all data to JSON
        except:
          print("Dumping error")
        else:
          print("New User Added")
          embed.description = f'This is your first GM!\nSend GM everyday to maintain your streak!!'
          embed.color = discord.Color.from_str(gm_color)
          embed.set_author(name="Level 1", icon_url=gm_logo)

      else:  # If user is present in JSON

        #Initializes variables which will be needed later
        last_used = datetime.fromisoformat(user_data[index]["last_used"])
        time_diff = msg_time - last_used
        count = user_data[index]["count"]
        embed.set_footer(text="GM everyday to continue your streak!",
                         icon_url=gm_logo)

        if time_diff < timedelta(hours=19, minutes=59,
                                 seconds=59):  #If 20 hours have not passed yet
          rem_time = timedelta(hours=20) - time_diff
          rem_time_h = int(rem_time.total_seconds() // 3600)
          rem_time_m = int((rem_time.total_seconds() % 3600) // 60)
          embed.description = f"You can say GM again after {rem_time_h} hours and {rem_time_m} mins."  #Specifies time they can say GM again which is after 24 hours have passed
        else:  #If 20 hours have passed till last said GM
          user_data[index]["count"] += 1
          user_data[index]["last_used"] = msg_time.isoformat()
          level = user_data[index]["level"]

          if time_diff >= timedelta(hours=20) and time_diff < timedelta(
              hours=39, minutes=59):  #If Streak Continues
            user_data[index]["streak"] += 1
            embed.description = f'You\'ve said GM **{user_data[index]["streak"]}** times in a row and a total of **{user_data[index]["count"]}** times!'

          else:  # If Streak ends
            user_data[index]["streak"] = 1
            embed.description = f'Your Streak has started again!\nYou\'ve said GM **{user_data[index]["count"]}** times in total!'

          count = user_data[index]["count"]
          if count == 3:
            user_data[index]["level"] = 2
            embed.add_field(name="Congrats! You're now level 2", value=" ")
          elif count == 7:
            user_data[index]["level"] = 3
            embed.add_field(name="Congrats! You're now level 3", value=" ")
          elif count == 14:
            user_data[index]["level"] = 4
            embed.add_field(name="Congrats! You're now level 4", value=" ")
          elif count == 25:
            user_data[index]["level"] = 5
            embed.add_field(name="Congrats! You're now level 5", value=" ")
          elif count == 47:
            user_data[index]["level"] = 6
            embed.add_field(name="Congrats! You're now level 6", value=" ")
          elif count == 80:
            user_data[index]["level"] = 7
            embed.add_field(name="Congrats! You're now level 7", value=" ")
          elif count == 135:
            user_data[index]["level"] = 8
            embed.add_field(name="Congrats! You're now level 8", value=" ")
          elif count == 223:
            user_data[index]["level"] = 9
            embed.add_field(name="Congrats! You're now level 9", value=" ")
          else:
            pass

        level = user_data[index]["level"]
        # Assigning Level to embed
        if level == 1:
          embed.set_author(name=f"Level 1", icon_url=gm_logo)
        elif level == 2:
          embed.set_author(name=f"Level 2", icon_url=gm_logo)
        elif level == 3:
          embed.set_author(name=f"Level 3", icon_url=gm_logo)
        elif level == 4:
          embed.set_author(name=f"Level 4", icon_url=gm_logo)
        elif level == 5:
          embed.set_author(name=f"Level 5", icon_url=gm_logo)
        elif level == 6:
          embed.set_author(name=f"Level 6", icon_url=gm_logo)
        elif level == 7:
          embed.set_author(name=f"Level 7", icon_url=gm_logo)
        elif level == 8:
          embed.set_author(name=f"Level 8", icon_url=gm_logo)
        elif level == 9:
          embed.set_author(name=f"Level 9", icon_url=gm_logo)
        else:
          pass

        with open("gm.json", "w") as file:
          json.dump(user_data, file)  #Stores all new data
      await message.channel.send(embed=embed)
  await bot.process_commands(message
                             )  # To enable the bot to read other commands


# ----------- Rank Command
@bot.tree.command(name="rank", description="Shows your GM Rank")
async def rank(i: discord.Interaction, user: discord.User = None):

  if user == None:  # If no user is entered, it will return stats of the user who invoked command
    user = i.user

  embed = Embed(title=f"{user.name}'s GM Rank", color=Color.from_str(gm_color)) #initial embed
  embed.set_thumbnail(url=user.avatar.url)

  with open("src/gm_channel.json") as gm: #loading gm data
    gm_data = json.load(gm)

  gm_channel_present = False  # Checks if the server is present in data
  for x in range(len(gm_data)):
    if gm_data[x]["server_id"] == i.guild_id:
      gm_channel_present = True
      break

  if gm_channel_present:  #If server is present, means bot is setup

    with open("gm.json") as file:
      user_data = json.load(file)

    server_id = i.guild.id
    server_data = [ud for ud in user_data if ud['server_id'] == server_id
                   ]  #Sorts all data for the server

    sorted_data = sorted(
      server_data, key=lambda x: x["count"], reverse=True
    )  # Sorts users by increasing count from the sorted server data
    user_not_present = True
    for x in range(len(sorted_data)):  # Checks ID of all users from JSON
      if user.id == sorted_data[x][
          "user_id"]:  # Checks if user is present in JSON
        user_not_present = False
        index = x  #Saves index of the user from JSON
        break

    if user_not_present:  # If user is not present
      embed.description = f"{user.display_name} has not started saying GM yet."
    else:  #If user is present it will display all stats
      count = sorted_data[index]["count"]
      streak = sorted_data[index]["streak"]
      level = sorted_data[index]["level"]
      embed.description = f"**LEVEL : **{level}\n**Total GMs : **{count}\n**Current Streak : **{streak}"
      embed.set_author(name=f"Rank #{x+1}", icon_url=user.avatar.url)
    await i.response.send_message(embed=embed)

  else:  #If the bot is not yet setup
    await i.response.send_message(
      "GM Channel is not set up. Run the command `/setup` to enable gm count!")


# --------------- Leaderboard Command
@bot.tree.command(name="leaderboard", description="Shows your GM Rank")
async def lb(i: discord.Interaction):

  embed = Embed(title="GM Leaderboard :", color=Color.from_str(gm_color))
  embed.set_author(name=i.user.name, icon_url=i.user.avatar.url)
  embed.set_thumbnail(url=i.user.avatar.url)

  with open("gm.json") as file:
    user_data = json.load(file)

  server_id = i.guild.id
  server_data = [ud for ud in user_data
                 if ud['server_id'] == server_id]  #Sorts data for the server
  sorted_data = sorted(server_data, key=lambda x: x["count"],
                       reverse=True)  #sorts server data into top 10 by count

  data_len = len(sorted_data)
  if data_len > 10:  #Checks if file has more than 10 users
    data_len = 10
  elif data_len == 0:
    embed.add_field(name="No records yet",
                    value="Setup GM bot with `/setup` command")

  # Add each user to the leaderboard
  for x in range(data_len):  # runs upto 10 if there are 10 or more users
    user_name = bot.get_user(sorted_data[x]["user_id"])
    level = sorted_data[x]["level"]
    count = sorted_data[x]["count"]
    try:
      embed.add_field(name=f"{x+1}. {user_name.display_name}",
                      value=f'Level: {level}\nTotal GM: {count}',
                      inline=False)
    except:
      embed.add_field(name=f'{x+1}. {sorted_data[x]["user_id"]}',
                      value=f'Level: {level}\nTotal GM: {count}',
                      inline=False)

  await i.response.send_message(embed=embed)  #Displays leaderboard


# ------------------------------------------
# # Assigning Levels by total Count
# new_level = math.floor(math.log(count, 365) * 10)
# if level < new_level:
#     user_data[index]["level"] += 1
#     embed.add_field(name=f"Congrats! You're now level {new_level}", value=" ")

#=========Setup command


@bot.tree.command(name="setup", description="Setup GM Bot or View GM setup")
async def setup(i: discord.Interaction,
                gm_channel: discord.TextChannel = None):
  if i.user.guild_permissions.administrator:
    embed = Embed(title="GM Setup", color=Color.from_str(gm_color))
    with open("src/gm_channel.json") as f:
      data = json.load(f)
    gm_channel_present = False
    for x in range(len(data)):  #Checks if server is already present in data
      if i.guild_id == data[x]["server_id"]:
        gm_channel_present = True
        break

    if gm_channel_present:  #Shows channel if already setup

      yes_button = Button(label="Yes", style=discord.ButtonStyle.green)
      no_button = Button(label="No", style=discord.ButtonStyle.red)

      views = View()
      views.add_item(yes_button)
      views.add_item(no_button)

      embed.description = f'GM channel is set to {bot.get_channel(data[x]["gm_channel"]).mention}\n Do you want to change the channel?'

      await i.response.send_message(embed=embed, view=views, ephemeral=True)

      async def yes_callback(yes_intr: discord.Interaction):
        embed.description = "Setting up..."
        embed.set_thumbnail(
          url=
          "https://i.pinimg.com/originals/82/a1/47/82a1470954fd17ae803d1a6b1d6b0bca.gif"
        )
        await i.edit_original_response(embed=embed)
        embed.set_thumbnail(url=None)
        await asyncio.sleep(3)
        try:
          del data[x]
          with open("src/gm_channel.json", "w") as f:
            json.dump(data, f)

        except:
          embed.description = "Unable to remove server"
          await i.edit_original_response(embed=embed, ephemeral=True)
        else:
          embed.description = "Channel has been removed!\nTo set a new channel run `/setup` command again"
          await i.edit_original_response(embed=embed, view=None)

      async def no_callback(no_intr: discord.Interaction):
        embed.description = "Command Terminated!"
        await i.edit_original_response(embed=embed, view=None)

      yes_button.callback = yes_callback
      no_button.callback = no_callback

    else:  #Shows setup guide if not setup
      if gm_channel == None:
        embed.description = "GM channel is not set up for this server. Follow the instructions below to setup."
        embed.add_field(
          name="Add bot to channel",
          value=
          "`Edit Channel` > `Permissions` > `Add member or roles` > `Select bot`\n",
          inline=False)
        embed.add_field(
          name="Enter GM Channel in the command",
          value=
          "`/setup` `gm_channel:#channel-name`\neg. `/setup` `gm_channel:#gm-chat`",
          inline=False)
        await i.response.send_message(embed=embed, ephemeral=True)
        return

      embed.description = "Setting up GM Channel..."
      embed.set_thumbnail(
        url=
        "https://i.pinimg.com/originals/82/a1/47/82a1470954fd17ae803d1a6b1d6b0bca.gif"
      )
      await i.response.send_message(embed=embed, ephemeral=True)
      embed.set_thumbnail(url=None)
      await asyncio.sleep(3)

      new_data = {"server_id": i.guild_id, "gm_channel": gm_channel.id}
      data.append(new_data)
      try:  #Adds new data to JSON
        with open("src/gm_channel.json", "w") as g:
          json.dump(data, g)
      except:
        embed.description = "Unable to set GM channel"
        await i.edit_original_response(embed=embed)
      else:
        embed.description = f"GM Channel is set.\nMake sure the bot has permission to send messages in {gm_channel.mention}"
        await i.edit_original_response(embed=embed)
        print("New Guild Added")
  else:  #If missing perms
    await i.response.send_message("**Missing Permissions:** Administrator")


#---------- Reset Command
@bot.tree.command(name="reset", description="Reset GM channel and stats")
async def reset(i: discord.Interaction):
  if i.user.guild_permissions.administrator:
    embed = Embed(title="GM Reset",
                  description="Searching...",
                  color=Color.from_str(gm_color))
    embed.set_thumbnail(
      url=
      "https://i.pinimg.com/originals/82/a1/47/82a1470954fd17ae803d1a6b1d6b0bca.gif"
    )

    await i.response.send_message(embed=embed, ephemeral=True)
    await asyncio.sleep(3)
    embed.set_thumbnail(url=None)

    server_id = i.guild_id
    with open("src/gm_channel.json") as f:
      data = json.load(f)
    for x in range(len(data)):
      server_found = False
      if server_id == data[x]["server_id"]:
        server_found = True
        index = x
        break

    if server_found:
      yes_button = Button(label="Yes", style=discord.ButtonStyle.green)
      no_button = Button(label="No", style=discord.ButtonStyle.red)

      async def yes_callback(yes_intr: discord.Interaction):
        embed.clear_fields()
        try:
          del data[x]
          with open("src/gm_channel.json", "w") as f:
            json.dump(data, f)
          with open("gm.json") as f:
            gm_data = json.load(f)
          gm_data = [x for x in gm_data if x["server_id"] != server_id]

          with open("gm.json", "w") as g:
            json.dump(gm_data, g, indent=4)

        except:
          await yes_intr.response.send_message("Unable to remove server",
                                               ephemeral=True)
        else:
          embed.description = "Channel has been removed! To set a new channel run `/setup` command again"
          await i.edit_original_response(embed=embed, view=None)

      async def no_callback(no_intr: discord.Interaction):
        embed.description = "Command Terminated.."
        embed.clear_fields()
        await i.edit_original_response(embed=embed, view=None)

      yes_button.callback = yes_callback
      no_button.callback = no_callback

      views = View()
      views.add_item(yes_button)
      views.add_item(no_button)
      gm_channel = bot.get_channel(data[x]["gm_channel"])
      embed.description = f"GM Channel is set to {gm_channel.mention}\nDo you want to remove it?"
      embed.add_field(
        name="Note:",
        value="This will delete all data including your ranks and leaderboard."
      )

      await i.edit_original_response(embed=embed, view=views)
    else:
      embed.description = "Server is not yet setup. Run `/setup` command to configure"
      await i.edit_original_response(embed=embed)

  else:
    await i.response.send_message("**Missing Permissions:** Administrator",
                                  ephemeral=True)


#---------- Server List
#shows how many servers the bot is in
@bot.tree.command(name="server-list",
                  description="Shows list of all the servers the bot is in")
async def server_list(i: discord.Interaction):
  if i.user.id == bot_master:
    servers = bot.guilds  #Gets all the servers the bot is in
    embed = Embed(title="Server list",
                  color=Color.from_str(gm_color))
    
    total_users = 0
    for server in servers:  #Adds them all to separate fields
      total_users = total_users + server.member_count
      embed.add_field(name=f"{server.name}",
                      value=f"Server ID `{server.id}`\nMember Count: `{server.member_count}`",
                      inline=False)
      
    embed.description=f"The bot is in {len(servers)} servers with total user count of {total_users}."
    await i.response.send_message(embed=embed)
  else:
    await i.response.send_message(
      "This command can be only used by the bot dev.")

#Bot Updates
@bot.tree.command(name="updates", description="Shows the recent bot update")
async def updates(i: discord.Interaction):
  channel = bot.get_channel(1116620807821611058)
  msg = await channel.fetch_message(channel.last_message_id)
  try:
    img = msg.attachments[0].url
  except:
    img = None

  em = discord.Embed(description=f"## PATCH NOTES\n\n{msg.content}",
                     color=discord.Color.from_str(gm_color))
  em.set_image(url=img)

  await i.response.send_message(embed=em)


#Broadcast Bot Updates to all GM Channels
@bot.tree.command(name="broadcast", description="Broadcast bot updates to all GM channels")
async def broadcast(i:discord.Interaction):
  if i.user.id == bot_master: #If command user is the bot master
    await i.response.send_message("`(-)` Initiating broadcast....") # Visual jff
    channel = bot.get_channel(1116620807821611058) # Bot update channel on support server
    msg = await channel.fetch_message(channel.last_message_id) # Fetches the last message on update channel
    try:
      img = msg.attachments[0].url #Fetches image if available
    except:
      img = None
    em = discord.Embed(description=f"## BOT UPDATES\n\n{msg.content}",
                      color=discord.Color.from_str(gm_color))
    em.set_image(url=img) #Update Embed

    await i.edit_original_response(content="`(\)` Opening database `gm_channel.json` ...") #Visual jff

    with open("src\gm_channel.json") as f: #Opening database
      data = json.load(f)

    await i.edit_original_response(content=f"`(|)` Sending Updates to {len(data)} servers...") #Visual jff

    for x in range(len(data)): #Going through all channels
      ch = bot.get_channel(data[x]["gm_channel"])

      try: #Checks if the bot can fetch the server
        server_name = (bot.get_guild(data[x]['server_id'])).name
      except:
        server_name = data[x]['server_id']

      try: #Sends embed to the channel
        await ch.send(embed=em) #Sending embed to gm channel
      except:
        await i.channel.send(f"Unable to find server. `ID: {server_name}`")
      else:
        await i.channel.send(f"Message was sent to channel `#{ch.name}` of server `{server_name}`.")
    await i.edit_original_response(content=f"`(/)` Send updates to all {len(data)} servers")
  
  else:
    await i.response.send_message("You are not allowed to use this command!")
  



#PingPong!
@bot.command()
async def ping(ctx: commands.Context):
  em = Embed(title="Pinging...", color=Color.from_str(gm_color))

  # Get the bot's current latency
  start_time = ctx.message.created_at
  message = await ctx.send(embed=em)  #sending initial Embed
  end_time = message.created_at
  latency = (end_time - start_time).total_seconds() * 1000
  em.title = "Pong!"
  em.color = Color.from_str(gm_color)
  em.description = f"Latency: {latency:.2f}ms \nAPI Latency: {round(bot.latency * 1000, 2)}ms"
  em.set_thumbnail(
    url=
    "https://i.pinimg.com/originals/a9/68/27/a96827aa75c09ba6c6dcf38b8f6daa90.gif"
  )
  await message.edit(embed=em)


# ------- Help command --------


@bot.tree.command(name="help", description="Help Command")
async def help(i: discord.Interaction):
  em = Embed(title="GM Help", color=Color.from_str(gm_color))
  em.add_field(name="/help", value="Shows you this", inline=False)
  em.add_field(name="/rank", value="Shows your GM stats", inline=False)
  em.add_field(name="/leaderboard",
               value="Shows top 10 Members who say GM",
               inline=False)
  em.set_thumbnail(url=gm_logo)
  await i.response.send_message(embed=em)

  if i.user.guild_permissions.administrator:  #Checks if user is an Admin
    emd = Embed(title="Admin Commands", color=Color.from_str(gm_color))
    emd.add_field(name="/setup",
                  value="Setup GM Bot or View GM Channel",
                  inline=False)
    emd.add_field(name="/reset",
                  value="Reset all stats and data",
                  inline=False)
    emd.add_field(name="@GM Bot ping", value="Check bot latency", inline=False)
    emd.set_thumbnail(url=gm_logo)
    await i.channel.send(embed=emd)


#----run token---
bot.run(token)

#---------------------------
