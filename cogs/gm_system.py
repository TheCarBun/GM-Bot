import discord
from discord.ext import commands
from datetime import datetime, timedelta
from config import *
from logs import *
from embeds import *
import json

class GmSystem(commands.Cog):
  def __init__(self, bot:commands.Bot):
    self.bot = bot
    
  @commands.Cog.listener()
  async def on_message(self, message:discord.Message):
    user = message.author  # User
    if user.bot:  # Checks if user is a bot
      return

    # initializing variables ...
    user_guild = message.guild.id  # Server ID
    msg_time = datetime.now()  # Time when message was sent
    gm_msg = message.content.lower()  # Gets message
    embed = await gm_embed(user) # Base embed

    with open("D:\VSCodePrograms\python\Discord Bot\GM Bot\database\gm_channel.json") as gmchjson:  #JSON Where GM Channel is stored
      gm_ch_data = json.load(gmchjson)

    gm_json_len = len(gm_ch_data)
    gm_ch_present = False
    for x in range(gm_json_len):  #Checks if the server has a GM Channel
      if message.guild.id == gm_ch_data[x]["server_id"]:
        gm_ch_present = True
        gm_index = x
        break

    if gm_ch_present:  #If there is a GM channel
      gm_ch = self.bot.get_channel(
          gm_ch_data[gm_index]["gm_channel"])  # initializes GM Channel

      if message.channel == gm_ch and "gm" in gm_msg:  # Checks channel and message
        with open("D:\VSCodePrograms\python\Discord Bot\GM Bot\database\gm.json") as gmjson:  # Opens JSON where it stores user stats
          user_data = json.load(gmjson)

        data_len = len(user_data)
        user_not_present = False

        for x in range(data_len):  # Checks ID of all users from JSON
          if user.id == user_data[x]["user_id"] and user_data[x][
              "server_id"] == user_guild:  # Checks if user is present in JSON
            user_not_present = False
            index = x  #Saves index of the user from JSON
            break
          else:
            user_not_present = True

        if user_not_present:  # If user is not present in JSON
          new_data = {
              "server_id": user_guild,
              "user_id": user.id,
              "count": 1,
              "streak": 1,
              "last_used": msg_time.isoformat(),
              "level": 1
          }
          user_data.append(new_data)  #adds new data to JSON
          try:
            with open("D:\VSCodePrograms\python\Discord Bot\GM Bot\database\gm.json", "w") as g:
              user_data = json.dump(user_data, g)  #Dumps all data to JSON
          except:
            print("Dumping error")
          else:
            await log_new_user(self.bot, user, message.guild)

            embed.description = f'This is your first GM!\nSend GM everyday to maintain your streak!!'
            embed.color = discord.Color.from_str(gm_color)
            embed.set_author(name="Level 1", icon_url=gm_logo)

        else:  # If user is present in JSON

          #Initializes variables which will be needed later
          last_used = datetime.fromisoformat(user_data[index]["last_used"])
          time_diff = msg_time - last_used
          count = user_data[index]["count"]
          embed.set_footer(text="GM everyday to continue your streak!",
                          icon_url=gm_logo)

          if time_diff < timedelta(hours=gm_time-1, minutes=59,
                                  seconds=59):  #If 20 hours have not passed yet
            rem_time = timedelta(hours=gm_time) - time_diff
            rem_time_h = int(rem_time.total_seconds() // 3600)
            rem_time_m = int((rem_time.total_seconds() % 3600) // 60)
            embed.description = f"You can say GM again after {rem_time_h} hours and {rem_time_m} mins."  #Specifies time they can say GM again which is after 20 hours have passed
          else:  #If 20 hours have passed till last said GM
            user_data[index]["count"] += 1
            user_data[index]["last_used"] = msg_time.isoformat()
            level = user_data[index]["level"]

            if time_diff >= timedelta(hours=gm_time) and time_diff < timedelta(
                hours=streak_time-1, minutes=59):  #If Streak Continues
              user_data[index]["streak"] += 1
              embed.description = f'You\'ve said GM **{user_data[index]["streak"]}** times in a row and a total of **{user_data[index]["count"]}** times!'

            else:  # If Streak ends
              user_data[index]["streak"] = 1
              embed.description = f'Your Streak has started again!\nYou\'ve said GM **{user_data[index]["count"]}** times in total!'

            count = user_data[index]["count"]
            if count == 3:
              user_data[index]["level"] = 2
              embed.add_field(name="Congrats! You're now level 2", value=" ")
            elif count == 7:
              user_data[index]["level"] = 3
              embed.add_field(name="Congrats! You're now level 3", value=" ")
            elif count == 14:
              user_data[index]["level"] = 4
              embed.add_field(name="Congrats! You're now level 4", value=" ")
            elif count == 25:
              user_data[index]["level"] = 5
              embed.add_field(name="Congrats! You're now level 5", value=" ")
            elif count == 47:
              user_data[index]["level"] = 6
              embed.add_field(name="Congrats! You're now level 6", value=" ")
            elif count == 80:
              user_data[index]["level"] = 7
              embed.add_field(name="Congrats! You're now level 7", value=" ")
            elif count == 135:
              user_data[index]["level"] = 8
              embed.add_field(name="Congrats! You're now level 8", value=" ")
            elif count == 223:
              user_data[index]["level"] = 9
              embed.add_field(name="Congrats! You're now level 9", value=" ")
            else:
              pass

          level = user_data[index]["level"]
          # Assigning Level to embed
          embed.set_author(name=f"Level {level}", icon_url=gm_logo)

          with open("D:\VSCodePrograms\python\Discord Bot\GM Bot\database\gm.json", "w") as file:
            json.dump(user_data, file)  #Stores all new data
        await message.channel.send(embed=embed)
    await self.bot.process_commands(message
                              )  # To enable the bot to read other commands

async def setup(bot:commands.Bot):
    await bot.add_cog(GmSystem(bot))
