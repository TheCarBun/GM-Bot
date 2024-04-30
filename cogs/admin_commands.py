import discord
from discord.ext import commands
from discord.ui import Button, View
from config import *
from logs import *
from embeds import *
import json, asyncio

class AdminCommands(commands.Cog):
  def __init__(self, bot:commands.Bot):
    self.bot = bot

#--------- Setup Command
  @commands.hybrid_command(name='setup', with_app_command=True)
  async def setup(self, ctx:commands.Context, gm_channel: discord.TextChannel = None):
    """Setup GM Bot or view the setup process"""
    if ctx.author.guild_permissions.administrator:
      embed = Embed(title="GM Setup", color=Color.from_str(gm_color))
      with open("D:\VSCodePrograms\python\Discord Bot\GM Bot\database\gm_channel.json") as f:
        data = json.load(f)
      gm_channel_present = False
      for x in range(len(data)):  #Checks if server is already present in data
        if ctx.guild.id == data[x]["server_id"]:
          gm_channel_present = True
          break

      if gm_channel_present:  #Shows channel if already setup

        yes_button = Button(label="Yes", style=discord.ButtonStyle.green)
        no_button = Button(label="No", style=discord.ButtonStyle.red)

        views = View()
        views.add_item(yes_button)
        views.add_item(no_button)

        embed.description = f'GM channel is set to {self.bot.get_channel(data[x]["gm_channel"]).mention}\n Do you want to change the channel?'

        await ctx.interaction.response.send_message(embed=embed, view=views, ephemeral=True)

        async def yes_callback(yes_intr: discord.Interaction):
          embed.description = "Setting up..."
          embed.set_thumbnail(url=loading_gif)
          await ctx.interaction.edit_original_response(embed=embed)
          
          embed.set_thumbnail(url=None)
          await asyncio.sleep(3)
          try:
            del data[x]
            with open("D:\VSCodePrograms\python\Discord Bot\GM Bot\database\gm_channel.json", "w") as f:
              json.dump(data, f)

          except:
            embed.description = "Unable to remove server"
            await ctx.interaction.edit_original_response(embed=embed, ephemeral=True)
          else:
            embed.description = "Channel has been removed!\nTo set a new channel run `/setup` command again"
            await ctx.interaction.edit_original_response(embed=embed, view=None)

        async def no_callback(no_intr: discord.Interaction):
          embed.description = "Command Terminated!"
          await ctx.interaction.edit_original_response(embed=embed, view=None)

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
          await ctx.interaction.response.send_message(embed=embed, ephemeral=True)
          return

        embed.description = "Setting up GM Channel..."
        embed.set_thumbnail(
            url=
            "https://i.pinimg.com/originals/82/a1/47/82a1470954fd17ae803d1a6b1d6b0bca.gif"
        )
        await ctx.interaction.response.send_message(embed=embed, ephemeral=True)
        embed.set_thumbnail(url=None)
        await asyncio.sleep(3)

        new_data = {"server_id": ctx.interaction.guild_id, "gm_channel": gm_channel.id}
        data.append(new_data)
        try:  #Adds new data to JSON
          with open("D:\VSCodePrograms\python\Discord Bot\GM Bot\database\gm_channel.json", "w") as g:
            json.dump(data, g)
        except:
          embed.description = "Unable to set GM channel"
          await ctx.interaction.edit_original_response(embed=embed)
        else:
          embed.description = f"GM Channel is set.\nMake sure the bot has permission to send messages in {gm_channel.mention}"
          await ctx.interaction.edit_original_response(embed=embed)
          await log_new_guild(self.bot, ctx.author.guild)
    else:  #If missing perms
      await ctx.interaction.response.send_message("**Missing Permissions:** Administrator")


#---------- Reset Command
  @commands.hybrid_command(name='reset', with_app_command=True)
  async def reset(self, ctx:commands.Context):
    """Resets GM Channel and all stats"""
    if ctx.author.guild_permissions.administrator:
      embed = await reset_embed()

      await ctx.interaction.response.send_message(embed=embed, ephemeral=True)
      await asyncio.sleep(3)
      embed.set_thumbnail(url=None)

      server_id = ctx.guild.id
      with open("D:\VSCodePrograms\python\Discord Bot\GM Bot\database\gm_channel.json") as f:
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
            with open("D:\VSCodePrograms\python\Discord Bot\GM Bot\database\gm_channel.json", "w") as f:
              json.dump(data, f)
            with open("../database/gm.json") as f:
              gm_data = json.load(f)
            gm_data = [x for x in gm_data if x["server_id"] != server_id]

            with open("../database/gm.json", "w") as g:
              json.dump(gm_data, g, indent=4)

          except:
            await yes_intr.response.send_message("Unable to remove server",
                                                ephemeral=True)
          else:
            embed.description = "Channel has been removed! To set a new channel run `/setup` command again"
            await log_reset(self.bot, ctx.author.guild, ctx.author)
            await ctx.interaction.edit_original_response(embed=embed, view=None)

        async def no_callback(no_intr: discord.Interaction):
          embed.description = "Command Terminated.."
          embed.clear_fields()
          await ctx.interaction.edit_original_response(embed=embed, view=None)

        yes_button.callback = yes_callback
        no_button.callback = no_callback

        views = View()
        views.add_item(yes_button)
        views.add_item(no_button)
        gm_channel = self.bot.get_channel(data[x]["gm_channel"])
        embed.description = f"GM Channel is set to {gm_channel.mention}\nDo you want to remove it?"
        embed.add_field(
            name="Note:",
            value=
            "This will delete all data including your ranks and leaderboard.")

        await ctx.interaction.edit_original_response(embed=embed, view=views)
      else:
        embed.description = "Server is not yet setup. Run `/setup` command to configure"
        await ctx.interaction.edit_original_response(embed=embed)

    else:
      await ctx.interaction.response.send_message("**Missing Permissions:** Administrator",
                                    ephemeral=True)

async def setup(bot:commands.Bot):
  await bot.add_cog(AdminCommands(bot))