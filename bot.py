import discord
from discord.ext import commands
from config import *
from logs import *
from embeds import *
import os, traceback
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned,
                   intents=intents)


#---------------------------------
# On Ready ---------
@bot.event
async def on_ready():
  ch = bot.get_channel(on_log_ch)  #gets log channel
  print("GM Bot is online!")
  embed = await on_ready_embed(bot)

  for file in os.listdir('./cogs'): # Loading Cogs
    if file.endswith('.py') and file != '__init__.py':
      try:
        await bot.load_extension("cogs."+file[:-3])
        print(f"{file} Loaded successfully.")
      except:
        print(f"Unable to load {file[:-3]}.")
        print(traceback.format_exc())

  try: #Syncing all commands
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
    print(f"{bot.user} is Online!")
    embed.add_field(name='Number of synced commands', value=f'{len(synced)}')
    await ch.send(embed=embed)  #Sends in support server

  except Exception as e:
    print("(-_-) Exception raised when Syncing commands: ",e)
    await log_exception(bot, e)

@bot.event
async def on_error(event, *args, **kwargs):
  message = args[0] #Gets the message object
  print(traceback.format_exc())
  await log_exception(bot, message)


# On Guild Join -------
@bot.event
async def on_guild_join(guild:discord.Guild):
  await log_on_join(bot, guild) #log guild join

# On Guild Leave ------
@bot.event
async def on_guild_remove(guild:discord.Guild):
  try:
    #delete server from gm 
    with open('database/gm_channel.json') as f:
      server_data = json.load(f)
    updated_gm_ch = [server for server in server_data if server['server_id'] != guild.id]
  except Exception as e:
    print(f"Error: {e}")
  
  try:
    #dump to gm_channel.json
    with open('database/gm_channel.json', 'w') as fl:
      json.dump(updated_gm_ch, fl)
  except Exception as e:
    print(f"Error writing file gm_channel.json : {e}")


  try:
    #delete gm data
    with open('database/gm.json') as f:
      gm_data = json.load(f)
    old_user_count = len(gm_data)
    updated_gm = [user for user in gm_data if user["server_id"] != guild.id]
    new_user_count = len(updated_gm)
  except Exception as e:
    print(f"Error: {e}")
  
  try:
    #dump to update
    with open('database/gm.json', 'w') as fl:
      json.dump(updated_gm, fl)
  except Exception as e:
    print(f"Error writing file gm.json : {e}")

  user_count = old_user_count - new_user_count
  await log_on_leave(bot, guild, user_count)

# -------------------------------------

#PingPong!
@bot.tree.command(name="ping", description="Shows bot's latency")
async def ping(i:discord.Interaction):
  await i.response.defer()
  em = await ping_embed()

  # Get the bot's current latency
  start_time = i.created_at
  message = await i.channel.send(embed=em)  #sending initial Embed
  end_time = message.created_at
  latency = (end_time - start_time).total_seconds() * 100
  em.title = "Pong!"
  em.color = Color.from_str(gm_color)
  em.description = f"Latency: {latency:.2f}ms \nAPI Latency: {round(bot.latency*100, 2)}ms"
  em.set_thumbnail(
      url=
      "https://i.pinimg.com/originals/a9/68/27/a96827aa75c09ba6c6dcf38b8f6daa90.gif"
  )
  await message.delete()
  await i.edit_original_response(embed=em)


# ------- Help command --------
# bot.remove_command('help')
@bot.tree.command(name="help", description="Help Command")
async def help(i: discord.Interaction):
  em = await help_embed()
  await i.response.send_message(embed=em)

  if i.user.guild_permissions.administrator:  #Checks if user is an Admin
    emd = await admin_help_embed(i.user)
    await i.channel.send(embed=emd)

bot.run(os.getenv('TOKEN'))