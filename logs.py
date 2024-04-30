import discord, json
from discord.ext import commands
from config import *
from embeds import *

async def log_on_join(bot:commands.Bot, guild:discord.Guild):
  log_channel = bot.get_channel(log_ch)
  print(f"Bot has joined new server: {guild.name}") # print to console
  await log_channel.send(embed=await on_join_embed(guild))

async def log_exception(bot:commands.Bot, exception:Exception):
  log_channel = bot.get_channel(log_ch)
  print(f"Bot raised an Exception: {exception}") # print to console
  await log_channel.send(embed=await on_exception_embed(exception))

async def log_new_guild(bot:commands.Bot, guild:discord.Guild):
  log_channel = bot.get_channel(log_ch)
  print("New Guild Added") # print to console
  await log_channel.send(embed=await new_guild_embed(guild))

async def log_new_user(bot:commands.Bot, user:discord.User, guild:discord.Guild):
  with open("./database/gm.json") as gm_data:
    user_data = json.load(gm_data)
  count = 0
  for x in range(len(user_data)):
      if user_data[x]['server_id'] == guild.id:
          count = count + 1
  
  log_channel = bot.get_channel(log_ch)
  print("New User Added") # print to console
  await log_channel.send(embed=await new_user_embed(user, guild, count))

async def log_reset(bot:commands.Bot, guild:discord.Guild, user:discord.User):
  log_channel = bot.get_channel(log_ch)
  print(f"Server data was reset: {guild.name}") # print to console
  await log_channel.send(embed=await server_reset_embed(user, guild))