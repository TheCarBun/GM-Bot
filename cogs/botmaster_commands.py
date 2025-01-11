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

  # Command to change GM stats of a user
  @commands.hybrid_command(name="stat-edit", with_app_command=True)
  async def stat_edit(
    self,
    ctx: commands.Context,
    user: discord.User = None,
    count: int = None,
    streak: int = None,
    last_used: str = None
  ):
    if ctx.author.id != bot_master:
      await ctx.interaction.response.send_message("This command can only be used by the bot dev.")
      return

    # Default user to the command invoker if not provided
    user = user or ctx.author
    server_id = ctx.guild.id

    # Return early if no count, streak, or last_used is provided
    if count is None and streak is None and last_used is None:
      embed = discord.Embed(
        title="Invalid Parameters",
        description="You must provide at least one parameter (`count`, `streak`, or `last_used`) to modify.",
        color=discord.Color.red()
      )
      embed.set_thumbnail(url=user.avatar.url)
      await ctx.interaction.response.send_message(embed=embed)
      return

    try:
      embed = discord.Embed(
        title="Updating GM Stats",
        description=f"Processing data for {user.mention} in **{ctx.guild.name}**.",
        color=discord.Color.blue()
      )
      embed.set_thumbnail(url=user.avatar.url)
      await ctx.interaction.response.send_message(embed=embed)

      # Load the JSON database
      with open("database/gm.json", "r") as file:
        gm_data = json.load(file)

      # Search for the user in the database
      user_data = next(
        (data for data in gm_data if data["user_id"] == user.id and data["server_id"] == server_id), None
      )

      if user_data:
        # Handle count and streak updates
        if count is not None:
          user_data["count"] = count
        if streak is not None:
          user_data["streak"] = streak

        # Handle last_used update
        if last_used:
          # Convert user-friendly input to ISO format
          user_data["last_used"] = await process_timestamp_input(last_used)

        # Write the updated data back to the JSON file
        with open("database/gm.json", "w") as file:
          json.dump(gm_data, file, indent=4)

        # Confirmation message
        embed.title = "GM Stats Updated"
        embed.description = f"Successfully updated stats for {user.mention}."
        if count is not None or streak is not None:
          embed.add_field(
            name="New Stats",
            value=f"**Count:** {user_data['count']}\n**Streak:** {user_data['streak']}",
            inline=False
          )
        if last_used:
          embed.add_field(
            name="New Timestamp",
            value=f"`{user_data['last_used']}`",
            inline=False
          )
        embed.color = discord.Color.green()
      else:
        # User not found in the database
        embed.title = "User Not Found"
        embed.description = f"{user.mention} does not exist in the database for this server."
        embed.color = discord.Color.red()

      # Send the final embed
      await ctx.interaction.edit_original_response(embed=embed)

    except FileNotFoundError:
      embed = discord.Embed(
        title="Database Error",
        description="The database file `gm.json` could not be found.",
        color=discord.Color.red()
      )
      await ctx.interaction.edit_original_response(embed=embed)

    except json.JSONDecodeError:
      embed = discord.Embed(
        title="Database Error",
        description="The database file `gm.json` is corrupted or contains invalid JSON.",
        color=discord.Color.red()
      )
      await ctx.interaction.edit_original_response(embed=embed)

    except Exception as e:
      embed = discord.Embed(
        title="Unexpected Error",
        description=f"An unexpected error occurred: `{e}`",
        color=discord.Color.red()
      )
      await ctx.interaction.edit_original_response(embed=embed)

# Helper function to process last_used input
async def process_timestamp_input(timestamp: str) -> str:
    """
    Converts user-friendly timestamp input into an ISO 8601 formatted string.
    Accepts formats like 'YYYY-MM-DD', 'today', 'yesterday', or 'X days ago'.
    """
    try:
      # Handle relative dates
      if timestamp.lower() == "today":
        return datetime.now().isoformat()  # UTC time
      elif timestamp.lower() == "yesterday":
        return (datetime.now() - timedelta(days=1)).isoformat()
      elif "days ago" in timestamp.lower():
        days = int(timestamp.split()[0])  # Extract the number of days
        return (datetime.now() - timedelta(days=days)).isoformat()

      # Handle specific date (YYYY-MM-DD)
      return datetime.strptime(timestamp, "%Y-%m-%d").isoformat()
    except Exception as e:
      raise ValueError(f"Invalid timestamp format: {timestamp}. Use 'YYYY-MM-DD', 'today', 'yesterday', or 'X days ago'.")

async def setup(bot:commands.Bot):
  await bot.add_cog(MasterCommands(bot))