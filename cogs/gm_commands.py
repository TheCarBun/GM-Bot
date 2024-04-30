# Commands: 1. Rank | 2. Leaderboard | 3. Bot updates

import discord
from discord.ext import commands
from discord.ui import Button, View
from config import *
from logs import *
from embeds import *
import json, asyncio

class GmCommands(commands.Cog):
  def __init__(self, bot:commands.Bot):
    self.bot = bot

# Rank Command
  @commands.hybrid_command(name='rank', with_app_command=True)
  async def rank(self, ctx:commands.Context, user: discord.User = None):
    """Check your rank or any other member's rank"""
    if user == None:  # If no user is entered, it will return stats of the user who invoked command
      user = ctx.author

    embed = await rank_embed(user)

    with open("D:\VSCodePrograms\python\Discord Bot\GM Bot\database\gm_channel.json") as gm:
      gm_data = json.load(gm)

    gm_channel_present = False  # Checks if the server is present in data
    for x in range(len(gm_data)):
      if gm_data[x]["server_id"] == ctx.guild.id:
        gm_channel_present = True
        break

    if gm_channel_present:  #If server is present, means bot is setup

      with open("D:\VSCodePrograms\python\Discord Bot\GM Bot\database\gm.json") as file:
        user_data = json.load(file)

      server_id = ctx.guild.id
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
        embed.set_author(name=f"Rank #{x+1}", icon_url=gm_logo)
      await ctx.interaction.response.send_message(embed=embed)

    else:  #If the bot is not yet setup
      await ctx.interaction.response.send_message(
          "GM Channel is not set up. Run the command `/setup` to enable gm count!"
      )
  
# --------------- Leaderboard Command
  @commands.hybrid_command(name="leaderboard", with_app_command=True)
  async def lb(self, ctx:commands.Context):
    """Shows top 10 members of the server"""
    embed = Embed(title="GM Leaderboard :", color=Color.from_str(gm_color))

    with open("D:\VSCodePrograms\python\Discord Bot\GM Bot\database\gm.json") as file:
      user_data = json.load(file)

    server_id = ctx.guild.id
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
      user_name = self.bot.get_user(sorted_data[x]["user_id"])
      count = sorted_data[x]["count"]
      try:  #Checks if the user can be mentioned
        embed.add_field(name=f"{x+1}. {user_name.display_name}",
                        value=f'Total GM: {count}',
                        inline=False)
      except:  #displays ID if can't mention
        embed.add_field(name=f'{x+1}. {sorted_data[x]["user_id"]}',
                        value=f'Total GM: {count}',
                        inline=False)

    await ctx.interaction.response.send_message(embed=embed)  #Displays leaderboard

  #Bot Updates
  @commands.hybrid_command(name="updates", with_app_command=True)
  async def updates(self, ctx:commands.Context):
    """Shows most recent bot update"""
    channel = self.bot.get_channel(1116620807821611058)
    msg = await channel.fetch_message(channel.last_message_id)
    try:
      img = msg.attachments[0].url
    except:
      img = None

    em = discord.Embed(description=f"## PATCH NOTES\n\n{msg.content}",
                      color=discord.Color.from_str(gm_color))
    em.set_image(url=img)

    await ctx.interaction.response.send_message(embed=em)


async def setup(bot:commands.Bot):
  await bot.add_cog(GmCommands(bot))