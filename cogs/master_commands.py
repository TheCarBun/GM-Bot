import discord
from discord.ext import commands
from discord.ui import Button, View
from config import *
from logs import *
from embeds import *
import json, asyncio

class MasterCommands(commands.Cog):
  def __init__(self, bot:commands.Bot):
    self.bot = bot

  #---------- Server List Command
  # (shows how many servers the bot is in)
  @commands.hybrid_command(name="server-list", with_app_command=True)
  async def server_list(self, ctx:commands.Context):
    """Shows all servers that use GM Bot"""
    if ctx.author.id == bot_master:
      servers = self.bot.guilds  #Gets all the servers the bot is in
      embed = await server_list_embed(servers)
      total_users = 0
      for server in servers:  #Adds them all to separate fields
        total_users = total_users + server.member_count
        embed.add_field(
            name=f"{server.name}",
            value=
            f"Server ID `{server.id}`\nMember Count: `{server.member_count}`",
            inline=False)
      embed.description = f"# The bot is in `{len(servers)}` servers with total user count of `{total_users}`."
      embed.set_thumbnail(url=gm_logo)
      await ctx.interaction.response.send_message(embed=embed)
    else:
      await ctx.interaction.response.send_message(
          "This command can be only used by the bot dev.")


  #Broadcast Bot Updates to all GM Channels
  @commands.hybrid_command(name="broadcast", with_app_command=True)
  async def broadcast(self, ctx:commands.Context):
    """Broadcasts Updates to all GM Channels"""
    if ctx.author.id == bot_master:
      await ctx.interaction.response.send_message("(-) Initiating broadcast....")
      channel = self.bot.get_channel(1116620807821611058)
      msg = await channel.fetch_message(channel.last_message_id)
      try:
        img = msg.attachments[0].url
      except:
        img = None
      em = await broadcast_embed(msg, img)

      try:
          with open("./database/gm_channel.json") as f:
            data = json.load(f)
      except:
          await ctx.channel.send("Unable to open database!")

      await ctx.interaction.edit_original_response(content="(\) Opening")

      for x in range(len(data)):
        ch = self.bot.get_channel(data[x]["gm_channel"])

        try:
          server_name = (self.bot.get_guild(data[x]['server_id'])).name
        except:
          server_name = data[x]['server_id']

        try:
          await ch.send(embed=em)
        except:
          await ctx.channel.send(f"Unable to find server. `ID: {server_name}`")
        else:
          await ctx.channel.send(
              f"Message was sent to channel `#{ch.name}` of server `{server_name}`."
          )
      await ctx.interaction.edit_original_response(content="(✅) Completed")

    else:
      await ctx.interaction.response.send_message("You are not allowed to use this command!")

async def setup(bot:commands.Bot):
  await bot.add_cog(MasterCommands(bot))