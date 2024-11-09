import discord
from discord.ext import commands
from discord.ui import Button, View
from config import *
from logs import *
from embeds import *
import json, asyncio
from datetime import datetime

class HelpCommand(commands.Cog):
  def __init__(self, bot:commands.Bot):
    self.bot = bot

# help Command
  @commands.hybrid_command(name='help', with_app_command=True)
  async def help(self, ctx:commands.Context):
    """Help command"""
    em = await help_embed()
    await ctx.interaction.response.send_message(embed=em)

    if ctx.interaction.user.guild_permissions.administrator:  #Checks if user is an Admin
      emd = await admin_help_embed(ctx.interaction.user)
      await ctx.interaction.channel.send(embed=emd)


async def setup(bot:commands.Bot):
  await bot.add_cog(HelpCommand(bot))