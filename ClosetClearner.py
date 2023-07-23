import interactions
from interactions import slash_command, slash_option, SlashContext, OptionType, listen
import modules.getVideos as getVideos

import asyncio
from dotenv import dotenv_values
import datetime

TOKEN = dotenv_values(".env")['TOKEN']

rules = ['Dont send direct hate speech &/or toxicity to anyone within this discord.',
         'Dont ping people for no given reason.',
         'Dont spam text, emojis, meme text blocks, etc.',
         'Dont send NSFW Content as it is NOT allowed within the discord server.',
         'Dont leak any of your personal information within this discord. This includes, phone numbers, addresses, names, emails, etc.',
         'Any form of racism whether in memes or messages will not be tolerated'
         'Dont advertise your channel or Discord Server anywhere! This applies to DM\'s as well.',
         'Do not make alt accounts to evade being banned / punished.']

print("initialising bot")
bot = interactions.Client(token=TOKEN)
print("finished")


# global variables here
@interactions.listen()
async def on_startup():
    print("\nBOT STATUS: ONLINE\n")
    await bot.change_presence(
                        status=interactions.Status.AFK,
                        activity=interactions.Activity(
                                            name="Hey! :)",
                                            type=interactions.ActivityType.PLAYING
                        )
    )
    
    channel = await bot.fetch_channel(1132373526087729333)
    await channel.send(f"----------------\n{str(datetime.datetime.now())}\nBot Online.")

    asyncio.create_task(announceNewUpload())

async def announceNewUpload():
    error = False

    try:
        pastVideo = getVideos.getLatestVideo('UCwdILK9zOMQJViJ40ngJ8Rg')
        latestVideo = None
    except:
        pastVideo = None
        latestVideo = None

    while True:
        try:
            if pastVideo != latestVideo:
                error = False

                embedVar = interactions.Embed(title="**Kay posted a new video!**", images=[latestVideo[2]], description=f"{latestVideo[0]}\n\u200B", color=0x00d5ff)
                embedVar.add_field(name="Video link:", value=latestVideo[1], inline=True)

                channel = await bot.fetch_channel(1132322188763090954)
                await channel.send(embed=embedVar)

            pastVideo = getVideos.getLatestVideo('UCwdILK9zOMQJViJ40ngJ8Rg')
            await asyncio.sleep(20)

            latestVideo = getVideos.getLatestVideo('UCwdILK9zOMQJViJ40ngJ8Rg')
            
            
        except Exception as e:
            if error == False:
                print(f"Exception occured on announceNewUpload(). Error:\n{e}\n\nWaiting until midnight before continuing")
                channel = await bot.fetch_channel(1132373526087729333)
                await channel.send(f"----------------\nError occured on {str(datetime.datetime.now())}:\n\nThere was an error retrieving data from YouTube. This is most likely caused by the quota limit being reached for the day.\nAs a result, YouTube upload notifications won't be available for a day.")

                error = True
            else:
                await asyncio.sleep(86400)

                await channel.send("----------------\nGood Morning!\n A day has cleared. Resuming YouTube upload notifications.")
                error = False


@slash_command(
        name="rule",
        description="Repeat a rule listed in the rules channel.",
        )

@slash_option(
    name="number",
    description="Rule number to send (1-8)",
    required=True,
    opt_type=OptionType.INTEGER
)
async def listRule(ctx: SlashContext, number: int):
    if number > 8 or number < 1:
        await ctx.respond(":x: Please enter a number between 1 and 8.", ephemeral=True)
    else:
        number = number - 1

        embedVar = interactions.Embed(title=f"**Rule {number+1}**", description=f"### ```{rules[number]}```", color=0x00d5ff)
        await ctx.respond(embed=embedVar)



bot.start(TOKEN)