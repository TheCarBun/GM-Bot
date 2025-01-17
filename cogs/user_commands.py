# Commands::
# 1.Info | 2.Leaderboard | 3.Streaks-Leaderboard | 4.Bot updates | 5.Vote | 6.Ping

import discord
from discord.ext import commands
from discord.ui import Button, View
from config import *
from logs import *
from embeds import *
import json, asyncio
from datetime import datetime

class GmCommands(commands.Cog):
  def __init__(self, bot:commands.Bot):
    self.bot = bot

# Info Command ----
  @commands.hybrid_command(name='info', with_app_command=True)
  async def info(self, ctx:commands.Context, user: discord.User = None):
    """Check your info or any other member's info"""
    if user == None:  # If no user is entered, it will return stats of the user who invoked command
      user = ctx.author

    embed = await rank_embed(user)

    with open("database/gm_channel.json") as gm:
      gm_data = json.load(gm)

    gm_channel_present = False  # To check if the server is present in data
    for x in range(len(gm_data)):
      if gm_data[x]["server_id"] == ctx.guild.id:
        gm_channel_present = True
        break

    if gm_channel_present:  #If server is present, means bot is setup

      with open("database/gm.json") as file:
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
        last_used = int(datetime.fromisoformat(sorted_data[index]["last_used"]).timestamp())
        level = sorted_data[index]["level"]
        embed.description = f"**LEVEL:** {level}\n**Total GMs:** {count}\n**Current Streak:** {streak}\n**Last GM:** <t:{last_used}:R>"
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

    with open("database/gm.json") as file:
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

# --------------- Streaks Leaderboard Command
  @commands.hybrid_command(name="streaks-leaderboard", with_app_command=True)
  async def streaks_lb(self, ctx:commands.Context):
    """Shows top 10 members with highest streaks in the server"""
    embed = Embed(title="GM Streaks Leaderboard :", color=Color.from_str(gm_color))

    with open("database/gm.json") as file:
      user_data = json.load(file)

    server_data = [ud for ud in user_data
                 if ud['server_id'] == ctx.guild.id]  #Sorts data for the server
    sorted_data = sorted(server_data, key=lambda x: x["streak"],
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
      streak = sorted_data[x]["streak"]
      last_used = datetime.fromisoformat(sorted_data[x]["last_used"])
      try:  #Checks if the user can be mentioned
        embed.add_field(name=f"{x+1}. {user_name.display_name}",
                        value=f'Streaks: {streak}\nLast GM Time: <t:{int(last_used.timestamp())}:R>',
                        inline=False)
      except:  #displays ID if can't mention
        embed.add_field(name=f'{x+1}. {sorted_data[x]["user_id"]}',
                        value=f'Streaks: {streak}\nLast GM Time: <t:{int(last_used.timestamp())}:R>',
                        inline=False)

    await ctx.interaction.response.send_message(embed=embed)  #Displays leaderboard

  # Bot Updates ----
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

  # Vote command ----
  @commands.hybrid_command(name="vote", with_app_command=True)
  async def vote(self, ctx:commands.Context):
    """Displays a link to Vote for the bot

    Args:
        ctx (commands.Context): message context
    """
    embed = await vote_embed()
    view = discord.ui.View()
    vote_button = discord.ui.Button(
      label="Vote for Us on top.gg!",
      style=discord.ButtonStyle.link,
      url="https://top.gg/bot/1105338570178310145/vote"
      )
    view.add_item(vote_button)
    await ctx.interaction.response.send_message(embed=embed, view=view)

  #PingPong!
  @commands.hybrid_command(name="ping", with_app_command=True)
  async def ping(self, ctx:commands.Context):
    """Check Bot's Latency

    Args:
        ctx (commands.Context): message context
    """
    await ctx.interaction.response.defer()
    em = await ping_embed()

    # Get the bot's current latency
    start_time = ctx.interaction.created_at
    message = await ctx.interaction.channel.send(embed=em)  #sending initial Embed
    end_time = message.created_at
    latency = (end_time - start_time).total_seconds() * 100
    em.title = "Pong!"
    em.color = Color.from_str(gm_color)
    em.description = f"Latency: {latency:.2f}ms \nAPI Latency: {round(self.bot.latency*100, 2)}ms"
    em.set_thumbnail(
        url=
        "https://i.pinimg.com/originals/a9/68/27/a96827aa75c09ba6c6dcf38b8f6daa90.gif"
    )
    await message.delete()
    await ctx.interaction.edit_original_response(embed=em)

#--------- Emoji with Webhooks for non nitro users -------
  @commands.hybrid_command(name="emoji", with_app_command=True)
  async def emoji(self, ctx:commands.Context, emoji:str, message:str="", emoji_in_end:bool=True):
    """
      Sends an emoji from the server using a webhook.
      - emoji: Name of the emoji to send.
      - message: Optional message to send alongside the emoji.
      - emoji_in_end: If True, appends the emoji at the end of the message.
    """
    emoji = emoji.lower()
    try:
      # Find the emoji in the server
      for emj in ctx.guild.emojis:
        if emj.name.lower() == emoji:
          server_emoji = self.bot.get_emoji(emj.id)
          break

      if not server_emoji:
        await ctx.interaction.response.send_message(
            "❌ Emoji not found in this server.", ephemeral=True
        )
        return

      # Get or create a webhook in the channel
      webhooks_available = await ctx.channel.webhooks()
      webhook = webhooks_available[0] if webhooks_available else await ctx.channel.create_webhook(name="Emoji Webhook")

      # Prepare the content with emoji
      content = f"{message}{server_emoji}" if emoji_in_end else f"{server_emoji}{message}"
      
      # Send the message using the webhook
      await webhook.send(
          content=content,
          username=ctx.author.display_name,
          avatar_url=ctx.author.avatar.url if ctx.author.avatar else None
      )
      
      # Send a success response
      await ctx.interaction.response.send_message(
          "✅ Emoji sent successfully!", ephemeral=True
      )
    
    except Exception as e:
      # Handle unexpected errors
      await ctx.interaction.response.send_message(
          f"❌ ERROR!!", ephemeral=True
      )
    
    finally:
      # Optional: Delete webhook if it was created just for this message
      if not webhooks_available and webhook:
        await webhook.delete(reason="Clean up temporary webhook.")

async def setup(bot:commands.Bot):
  await bot.add_cog(GmCommands(bot))