import discord
from discord.ext import commands
import youtube_dl

bot = commands.Bot(command_prefix='!')
client = discord.Client()

queue = []

#play command
@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        return await ctx.send("Nie jestes podlaczony do zadnego kanalu glosowego.")
    vc = await voice_channel.connect()

    if "playlist" in url:
        playlist = youtube_dl.YoutubeDL({}).extract_info(url, download=False)
        for video in playlist['entries']:
            url2 = video['url']
            source = await discord.FFmpegAudio.from_probe(url2, **FFMPEG_OPTIONS)
            queue.append((source, video))
        await ctx.send(f"Dodano {playlist['title']} do kolejki.")
    else:
        with youtube_dl.YoutubeDL({'format':'bestaudio'}) as ydl:
          info = ydl.extract_info(url, download=False)
          url2 = info['formats'][0]['url']
          source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        if not queue:
          vc.play(source)
          await ctx.send(f"Aktualnie grane {info['title']}")
        else:
          queue.append((source,info))
          await ctx.send(f"Dodano {info['title']} do kolejki.")
        
    if len(queue) == 1:
        source, info = queue[0]
        vc.play(source)
        await ctx.send(f"Aktualnie grane {info['title']}")

#skip command
@bot.command()
async def skip(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        if queue:
            source, info = queue.pop(0)
            voice_client.play(source)
            await ctx.send(f"Aktualnie grane {info['title']} z kolejki.")
    else:
        await ctx.send("Nie ma żadnych piosenek w kolejce.")

#stop command  
@bot.command()
async def stop(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    await voice_client.disconnect()

#help command
@bot.command()
async def help(ctx):
    ctx.send(f"Bot posiada aktualnie tylko komendy play i stop.")


bot.run('MTA4MTk3NDAwMjY4NTMyNTQzMw.Gi0Jld.Ifcj3sVSSiMCHX4ZWzgX5PLcVJJMM5-A77cqRs')
