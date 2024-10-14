import discord
from discord.ext import commands
from discord.ui import Button, View
from config import *
from logs import *
from embeds import *
import json, asyncio
from datetime import datetime, timedelta

class MasterCommands(commands.Cog):
  def __init__(self, bot:commands.Bot):
    self.bot = bot

  # Command to list the servers with pagination
  @commands.hybrid_command(name="server-list", with_app_command=True)
  async def server_list(self, ctx: commands.Context):
    """Shows all servers that use GM Bot"""
    if ctx.author.id == bot_master:
      servers = self.bot.guilds  # Gets all the servers the bot is in
      pages = await create_paginated_embeds(servers)
      
      # If there's only one page, just send it
      if len(pages) == 1:
        await ctx.interaction.response.send_message(embed=pages[0])
      else:
        current_page = 0

        # Define the buttons for pagination
        class PaginationView(View):
          def __init__(self):
            super().__init__()
            self.current_page = current_page

          @discord.ui.button(label="Previous", style=discord.ButtonStyle.green)
          async def previous_button(self, interaction: discord.Interaction, button: Button):
            if self.current_page > 0:
              self.current_page -= 1
              await interaction.response.defer()
              await interaction.message.edit(embed=pages[self.current_page], view=self)

          @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
          async def next_button(self, interaction: discord.Interaction, button: Button):
            if self.current_page < len(pages) - 1:
              self.current_page += 1
              await interaction.response.defer()
              await interaction.message.edit(embed=pages[self.current_page], view=self)

        # Send the first page with the buttons for navigation
        view = PaginationView()
        await ctx.interaction.response.send_message(embed=pages[0], view=view)
    else:
      await ctx.interaction.response.send_message(
          "This command can only be used by the bot dev."
      )
    
  #--------- Count of Users in a Server
  @commands.hybrid_command(name="users-count", with_app_command=True)
  async def users_count(self, ctx:commands.Context, server_id:str):
    """Shows count of users in a server from server id

    Args:
        ctx (commands.Context): discord context
        server_id (int): Server ID
    """
    server_id = int(server_id)
    if ctx.author.id == bot_master:
      embed = await embed_template()
      embed.set_thumbnail(url=gm_logo)

      with open('database/gm_channel.json') as f:
        gm_channel_data = json.load(f)
      server_found = False
      for server in gm_channel_data:
        if server['server_id'] == server_id:
          server_found = True

      if server_found:
        with open('database/gm.json') as file:
          gm_data = json.load(file)
        
        # users who have used GM Bot in the server
        user_count = 0
        active_users = 0
        for user in gm_data:
          if user['server_id'] == server_id:
            user_count += 1

            # Active users(48 hours)
            last_used = datetime.fromisoformat(user['last_used'])
            time_diff = datetime.now() - last_used
            if time_diff < timedelta(hours=48):  #For users who said GM in the last 48 hours
              active_users += 1
        guild = self.bot.get_guild(server_id)
        embed.title = "Users in Server"
        try:
          embed.add_field(
            name='Server Details', 
            value=f'Server Name: {guild.name}\nServer ID: `{guild.id}`\nOwner ID: {guild.owner.global_name}',
            inline=False
            )
        except Exception as e:
          embed.add_field(name="Error", value=f"Cannot fetch server details: {e}")
        try:
          embed.add_field(
            name="Guild Details", 
            value=f"Total Members: {guild.member_count} \nTotal Users: {user_count} \nActive Users: {active_users}"
            )
        except:
          embed.add_field(
            name="Error",
            value="Cannot fetch guild details"
          )
        await ctx.interaction.response.send_message(embed=embed)
      else:
        embed.title= "Server Not Found"
        await ctx.interaction.response.send_message(embed=embed)
    else:
      await ctx.interaction.response.send_message("This command can be only used by the bot dev.")

  #Broadcast Bot Updates to all GM Channels
  @commands.hybrid_command(name="broadcast", with_app_command=True)
  async def broadcast(self, ctx:commands.Context):
    """Broadcasts Updates to all GM Channels
    Add:
    - Find servers from bot.guilds to send the broadcast to"""
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
          with open("database/gm_channel.json") as f:
            data = json.load(f)
      except:
          await ctx.channel.send("Unable to open database!")

      await ctx.interaction.edit_original_response(content="(\) Opening")

      error_count = 0
      success_count = 0
      for x in range(len(data)):
        ch = self.bot.get_channel(data[x]["gm_channel"])

        try:
          server_name = (self.bot.get_guild(data[x]['server_id'])).name
        except:
          server_name = data[x]['server_id']

        try:
          await ch.send(embed=em)
        except:
          error_count += 1
          await ctx.channel.send(f"Unable to find server. `ID: {server_name}`")
        else:
          success_count += 1
          await ctx.channel.send(
              f"Message was sent to channel `#{ch.name}` of server `{server_name}`."
          )
      await ctx.interaction.edit_original_response(content=f"(✅) Completed\nSent to {success_count} servers out of {success_count+error_count} servers")

    else:
      await ctx.interaction.response.send_message("You are not allowed to use this command!")

async def setup(bot:commands.Bot):
  await bot.add_cog(MasterCommands(bot))