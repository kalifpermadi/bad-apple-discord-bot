import discord
import cv2
import time
import sys

bot = discord.Client(intents=discord.Intents.default())
token = '(insert token here)'
video = cv2.VideoCapture("video.mp4")
totalFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(video.get(cv2.CAP_PROP_FPS) * 8 / 30)
interval = 1 / fps

@bot.event
async def on_ready():
    print('Bad Apple!! is now running!')

@bot.event
async def on_message(message):
    if message.content == "test":
        await message.channel.send("yo")
    
    if message.content == "!play":
        ctx = await message.channel.send("```Processing...```")
        i = 0
        startExecute = time.time()
        for n in range(0, totalFrames * 4, 15):
            n = round(n / 4)
            startTime = time.time()
            video.set(cv2.CAP_PROP_POS_FRAMES, n)
            _, frame = video.read()
            height, width, _ = frame.shape
            
            if width > 72:
                frame = cv2.resize(frame, (72, round(height * 72 / width)), interpolation = cv2.INTER_NEAREST)

            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width, _ = frame.shape

            string = "```"
            brightness = [" ", ".", ",", ":", ";", "+", "*", "?", "@"]
            for row in range(0, height, 2):
                for col in range(0, width):
                    b, g, r = frame[row, col]
                    string += brightness[round(int(b) / 32)]
                string += "\n"

            string += "```"
            await ctx.edit(content=string)
            endTime = time.time()
            delay = interval - (endTime - startTime)

            if delay < 0:
                delay = 0

            i += 1
            print("Frame " + str(i))
            time.sleep(delay)

        finishExecute = time.time()
        executeTime = finishExecute - startExecute
        print("Time: " + str(executeTime) + " seconds")
        
    if message.content == "!stop":
        await message.channel.send("Stopped!")
        sys.exit()
            
bot.run(token)