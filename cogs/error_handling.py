import discord
from discord.ext import commands
from config import *
from logs import *
from embeds import *

class GMError(commands.Cog):
  def __init__(self, bot:commands.Bot):
    self.bot = bot
    
  @commands.Cog.listener()
  async def on_error(self, error):
    ...


async def setup(bot:commands.Bot):
  await bot.add_cog(GMError(bot))