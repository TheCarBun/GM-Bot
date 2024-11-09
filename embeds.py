import discord
from discord.ext import commands
from discord import Embed, Color
from config import *
from math import ceil
import json

#============================================

#-------------- Embed Template -------------
async def embed_template():
  embed = Embed(
    color=Color.from_str(gm_color)
  )
  return embed

#----------------- On Ready -----------------
async def on_ready_embed(bot:commands.Bot):
  embed = Embed(
      title="GM Bot is Online!",
      color=Color.from_str(gm_color),
  )
  embed.add_field(name="Bot ID :", value=f"{bot.user.id}", inline=False)
  embed.add_field(name="Bot :", value=f"{bot.user.mention}", inline=False)
  embed.add_field(name="Ping :", value=f"{round(bot.latency,2)} ms", inline=False)
  embed.set_thumbnail(url= on_ready_gif)
  return embed

#----------------- On Exception -----------------
async def on_exception_embed(message:str):
  embed = Embed(
      title="Bot raised an Exception",
      description= message,
      color=Color.red(),
  )
  return embed

#--------------- GM Embed ----------------
async def gm_embed(user:discord.User):
  embed = discord.Embed(title=f"Good Morning {user.display_name if user.display_name else user.name}!!",
                        color=discord.Color.from_str(gm_color))  #Base Embed
  if user.avatar is not None:
    embed.set_thumbnail(url=user.avatar.url)
  else:
    embed.set_thumbnail(url=user.default_avatar.url)
  return embed

#--------------- Ping Embed ----------------
async def ping_embed():
  embed = discord.Embed(title="Pinging...",
                        color=discord.Color.from_str(gm_color))  #Base Embed
  embed.set_thumbnail(url= loading_gif)
  return embed

#--------------- Rank Embed ----------------
async def rank_embed(user:discord.User):
  embed= Embed(title=f"{user.name}'s GM Rank", color=Color.from_str(gm_color))
  embed.set_thumbnail(url=user.avatar.url)
  return embed

#--------------- Vote Embed ----------------
async def vote_embed():
  embed= Embed(
    title="✨ Support us on top.gg!", 
    url="https://top.gg/bot/1105338570178310145/vote",
    description= "Your support means the world to us! 💗\nEvery vote on top.gg motivates us to keep improving and adding new features. \nThank you for being such an amazing user!!",
    color=Color.from_str(gm_color))
  embed.set_image(url="https://imgur.com/9czgbOd.png")
  return embed

#--------------- Setup Embeds ----------------

#Successfully sent message to #gm-chat
async def success_embed():
  embed = Embed(title="GM Setup Success",
                  description="This channel is successfully set as GM Chat\nTry saying `GM`.",
                  color=Color.from_str(gm_color))
  embed.set_thumbnail(url=gm_logo)
  return embed

#Failed to send message to #gm-chat
async def failed_embed(gm_channel:discord.TextChannel):
  embed = Embed(title="GM Setup Error!",
                  description=f"GM Bot does not have permission to send message on {gm_channel.mention}\nPlease add GM Bot to the channel and enable the following permissions for it:\n- View Channel\n- Send Messages\n- Read Message History",
                  color=Color.from_str(gm_color))
  embed.set_thumbnail(url=gm_logo)
  return embed

#--------------- Reset Embed ----------------
async def reset_embed():
  embed = Embed(title="GM Reset",
                  description="Searching...",
                  color=Color.from_str(gm_color))
  embed.set_thumbnail(url=loading_gif)
  return embed

#--------------- Server List Embed ----------------

# Helper function to create paginated embeds for Server List
async def create_paginated_embeds(servers):
    pages = []
    chunk_size = 10  # display 10 servers per page
    total_pages = ceil(len(servers) / chunk_size)  # Calculate total pages
    
    for page_num in range(total_pages):
        embed = discord.Embed(title="GM Bot - Server List", color=discord.Color.from_str(gm_color))
        embed.set_thumbnail(url=gm_logo)
        
        # Slice the server list into chunks of 10 for each page
        server_chunk = servers[page_num * chunk_size:(page_num + 1) * chunk_size]
        total_members = 0
        total_users = 0
        
        for server in server_chunk:
            total_members += server.member_count
            try:
                with open('database/gm.json') as f:
                    gm_data = json.load(f)
                user_count = sum(1 for user in gm_data if user['server_id'] == server.id)
                total_users += user_count
            except Exception as e:
                print(f"Error: {e}")  # Handle your error logging here

            # Add the server details to the embed field
            embed.add_field(
                name=f"{server.name}", 
                value=(
                    f"Server ID `{server.id}`\n"
                    f"Member Count: `{server.member_count}`\n"
                    f"User Count: `{user_count}`"
                ),
                inline=False
            )

        embed.description = f"**Total Servers:** `{len(servers)}`\n**Total Members:** `{total_members}`\n**Total Users:** `{total_users}`"
        embed.set_footer(text=f"Page {page_num + 1}/{total_pages}")
        pages.append(embed)

    return pages

#--------------- Broadcast Embed ----------------
async def broadcast_embed(msg:discord.Message, img:str):
  embed = Embed(description=f"## BOT UPDATES\n\n{msg.content}",
                        color=discord.Color.from_str(gm_color))
  
  embed.set_image(url=img)
  return embed

#--------------- Help Embed ----------------
async def help_embed():
  embed = Embed(title="GM Help", color=Color.from_str(gm_color))
  embed.add_field(name="/help", value="Shows you this", inline=False)
  embed.add_field(name="/rank", value="Shows your GM stats", inline=False)
  embed.add_field(name="/leaderboard",
               value="Shows top 10 Members who say GM",
               inline=False)
  embed.add_field(name="/ping", value="Check bot latency", inline=False)
  embed.set_thumbnail(url=gm_logo)
  return embed

#--------------- Admin Help Embed ----------------
async def admin_help_embed(user:discord.User):
  embed = Embed(title="Admin Commands", color=Color.from_str(gm_color))
  embed.add_field(name="/setup",
                value="Setup GM Bot or View GM Channel",
                inline=False)
  embed.add_field(name="/reset",
                value="Reset all stats and data",
                inline=False)
  if user.avatar is not None:
    embed.set_thumbnail(url=user.avatar.url)
  return embed
#====================== Log Embeds =========================

#------------ On Server Join Log -------------
async def on_join_embed(guild:discord.Guild):
  embed = Embed(
    title="Joined new Server",
    description=f"**Server Name:** {guild.name}\n**Description:** {guild.description}",
    color=Color.from_str(gm_color)
  )
  embed.add_field(name="Server ID", value=f"{guild.id}", inline=False)
  if guild.owner is not None:
    embed.add_field(name="Server Owner", value=f"**@{guild.owner.name}**\nID: ```<@{guild.owner_id}>```", inline=False)
  embed.add_field(name="Created at", value=f"<t:{int(guild.created_at.timestamp())}:f>", inline=False)
  embed.add_field(name="Member Count", value=f"{guild.member_count}", inline=False)

  # Checks if Server Banner URL is available
  if guild.banner is not None:
    embed.set_image(url=guild.banner.url)

  # Checks if Server Icon URL is available
  if guild.icon is not None:
    embed.set_thumbnail(url=guild.icon.url)

  # Checks if Server invites are available
  try:
    invites = ""
    for invite in await guild.invites():
      invites = invites+ f"https://discord.gg/{invite.code}\n"
  except discord.Forbidden as e:
    embed.add_field(name="No Invite links", value=f"Missing Permissions", inline=False)
    print(e)
  else:
    if len(invites) < 1024:
      embed.add_field(name="Available Invite links", value=f"{invites}", inline=False)

  return embed

#------------ On Server Leave -----------
async def left_guild_embed(guild:discord.Guild, user_count:int):
  embed = Embed(
  title="Bot left a Server",
  description=f"**Server Name:** {guild.name}\n**Description:** {guild.description}",
  color=Color.from_str(gm_color)
  )
  embed.add_field(name="Server ID", value=f"{guild.id}", inline=False)
  if guild.owner is not None:
    embed.add_field(name="Server Owner", value=f"**@{guild.owner.name}**\nID: ```<@{guild.owner_id}>```", inline=False)
  embed.add_field(name="Created at", value=f"<t:{int(guild.created_at.timestamp())}:f>", inline=False)
  embed.add_field(name="Member Count", value=f"{guild.member_count}", inline=False)
  embed.add_field(name="User Count", value=f"{user_count} users")

  # Checks if Server Banner URL is available
  if guild.banner is not None:
    embed.set_image(url=guild.banner.url)

  # Checks if Server Icon URL is available
  if guild.icon is not None:
    embed.set_thumbnail(url=guild.icon.url)
  
  return embed


#------------ New Guild Log ------------
async def new_guild_embed(guild:discord.Guild):
  embed = Embed(
    title= "New Guild Added",
    color= Color.from_str(gm_color)
  )
  embed.add_field(name="Server", value=f"{guild.name}", inline=False)
  if guild.owner is not None:
    embed.add_field(name="Server Owner", value=f"{guild.owner.name}", inline=False)
  # Checks if Server Banner URL is available
  if guild.banner is not None:
    embed.set_image(url=guild.banner.url)

  # Checks if Server Icon URL is available
  if guild.icon is not None:
    embed.set_thumbnail(url=guild.icon.url)
  
  # Checks if Server invites are available
  try:
    invites = ""
    for invite in await guild.invites():
      invites = invites+ f"https://discord.gg/{invite.code}\n"
  except discord.Forbidden as e:
    embed.add_field(name="Available Invite links", value=f"{e}", inline=False)
    print(e)
  else:
    if len(invites) < 1024:
      embed.add_field(name="Available Invite links", value=f"{invites}", inline=False)

  return embed

#------------ New user Log ------------
async def new_user_embed(user:discord.Member, guild:discord.Guild, count:int):
  embed = Embed(
    title= "New User Added",
    color= Color.from_str(gm_color)
  )
  embed.add_field(name="Server", value=f"{guild.name}", inline=False)
  embed.add_field(name="Username", value=f"{user.name}", inline=False)
  embed.add_field(name="Total Users", value=f"{count}", inline=False)
  # Checks if Server Banner URL is available
  if user.banner is not None:
    embed.set_image(url=user.banner.url)

  # Checks if Server Icon URL is available
  if user.avatar is not None:
    embed.set_thumbnail(url=user.avatar.url)

  return embed


#------------ Server Reset Log ------------
async def server_reset_embed(user:discord.Member, guild:discord.Guild):
  embed = Embed(
    title= "Server Reset",
    color= Color.from_str(gm_color)
  )
  embed.add_field(name="Server", value=f"{guild.name}", inline=False)
  embed.add_field(name="Command User", value=f"{user.name}", inline=False)
  # Checks if Server Banner URL is available
  if guild.banner is not None:
    embed.set_image(url=guild.banner.url)

  # Checks if Server/User Icon URL is available
  if guild.icon is not None:
    embed.set_thumbnail(url=guild.icon.url)
  elif user.avatar is not None:
    embed.set_thumbnail(url=user.avatar.url)

  return embed
