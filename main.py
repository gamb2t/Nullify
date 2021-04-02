import discord, asyncio, os, platform, sys, datetime, requests
import config
from discord.ext import commands, tasks
from discord.ext.commands import Bot
intents = discord.Intents.default()  
intents.members = True 

bot = Bot(command_prefix=config.BOT_PREFIX, intents=intents)
start_time = datetime.datetime.utcnow() #업타임 보기 전용 스타트타임
bot.remove_command("help")

@bot.event
async def on_ready():
    bot.loop.create_task(status_task())
    print(f"{bot.user.name}으로 로그인됨")
    print(f"Discord.py API 버전: {discord.__version__}")
    print(f"Python 버전: {platform.python_version()}")
    print(f"서버 정보: {platform.system()} {platform.release()} ({os.name})")
    print("---------------------------------------------")
async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game("[.] | Expect the Unexpected"))

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

@bot.command()
async def invite(ctx):
    embed = discord.Embed(
                title="봇 초대 링크",
                description="봇 초대 링크 여기다가",
                color=config.success
               )
    embed.set_thumbnail(url="봇 프로필")
    embed.set_footer(text="gamb1t")
    await ctx.send(embed=embed)
    
@bot.command()
async def info(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="봇 정보",
        description=f"Discord.py API 버전: {discord.__version__}\nPython 버전: {platform.python_version()}\n호스팅 정보: {platform.system()} | {platform.release()} ({os.name})"
    )
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0xffffff, timestamp=ctx.message.created_at)
    embed.description = f"````Help - 이 페이지를 보여줍니다\n`ban - 사용자를 밴 합니다\n`kick - 사용자를 강퇴합니다\n`warn - 사용자에게 dm으로 경고를 보냅니다\n`purge - 메시지 청소를 합니다\n`serverinfo - 서버 정보를 보여줍니다\n`invite - 봇 초대 링크를 보여줍니다```"
    await ctx.send(embed=embed)

@bot.command()
async def purge(ctx, number):
    await ctx.message.delete()
    if ctx.message.author.guild_permissions.administrator:
        try:
            number = int(number)
        except:
            embed = discord.Embed(
                title="⚠️ 에러",
                description=f"`{number}` 는 유효한 숫자가 아닙니다.",
                color=config.error
            )
            await ctx.send(embed=embed)
            return
        if number < 1:
            embed = discord.Embed(
                title="⚠️ 에러",
                description=f"`{number}` 는 유효한 숫자가 아닙니다.",
                color=config.error
            )
            await ctx.send(embed=embed)
            return
        purged_messages = await ctx.message.channel.purge(limit=number)
        embed = discord.Embed(
            title="✅ 청소완료",
            description=f"메시지 **{len(purged_messages)}** 개 정리 완료!",
            color=config.success
        )
        await ctx.send(embed=embed, delete_after=5.0)

@bot.command()
async def warn(ctx, member: discord.Member, *args):
    await ctx.message.delete()
    if ctx.message.author.guild_permissions.administrator:
        reason = " ".join(args)
        embed = discord.Embed(
            title="✅ 경고 완료",
            description=f"**{member}**가 경고를 받음",
            color=config.success
        )
        embed.add_field(
            name="사유:",
            value=reason
        )
        await ctx.send(embed=embed)
        try:
            await member.send(f"**{ctx.message.author}**에게서 경고를 받았습니다!\n사유: {reason}")
        except:
            pass
    else:
        embed = discord.Embed(
            title="⚠️에러",
            description="명령어를 쓸 수 없습니다(권한부족)",
            color=config.error
        )
        await ctx.send(embed=embed)

@bot.command()
async def ban(ctx, member: discord.Member, *args):
    await ctx.message.delete()
    if ctx.message.author.guild_permissions.administrator:
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="⚠️ 에러",
                    description="해당 사용자는 관리자 권한을 가지고 있습니다.",
                    color=config.error
                )
                await ctx.send(embed=embed)
            else:
                reason = " ".join(args)
                await member.ban(reason=reason)
                embed = discord.Embed(
                    title="✅사용자 밴 완료",
                    description=f"💀 R.I.P **{member}**",
                    color=config.success
                )
                embed.add_field(
                    name="사유:",
                    value=reason
                )
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                title="✅사용자 밴 완료",
                    description=f"💀 R.I.P **{member}**",
                    color=config.success
                )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="⚠️ 에러",
            description="명령어를 쓸 수 없습니다(권한부족)",
            color=config.error
        )
        await ctx.send(embed=embed)

@bot.command(aliases=["guildinfo"])
async def serverinfo(ctx):
    await ctx.message.delete()
    date_format = "%Y.%m.%d %I:%M %p"
    
    member_count = ctx.guild.member_count
    embed = discord.Embed(title=f"{ctx.guild.name}",
        description=f"서버인원: {member_count}명\n",
        timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="서버생성일", value=f"{ctx.guild.created_at.strftime(date_format)}")
    embed.add_field(name="서버 주인", value=f"{ctx.guild.owner}")
    embed.add_field(name="서버 지역", value=f"{ctx.guild.region}")
    embed.add_field(name="서버 ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    await ctx.send(embed=embed)

@bot.command()
async def kick(ctx, member: discord.Member, *args):
    await ctx.message.delete()
    if ctx.message.author.guild_permissions.kick_members:
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="⚠️ 에러",
                description="해당 사용자는 관리자 권한을 가지고 있습니다.",
                color=config.error
            )
            await ctx.send(embed=embed)
        else:
            try:
                reason = " ".join(args)
                await member.kick(reason=reason)
                embed = discord.Embed(
                    title="✅ 추방 완료",
                    description=f"💀 R.I.P **{member}**",
                    color=config.success
                )
                embed.add_field(
                    name="사유:",
                    value=reason
                )
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="✅ 추방 완료",
                    description=f"💀 R.I.P **{member}**",
                    color=config.success
                )
                await ctx.message.channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title="⚠️ 에러",
            description="명령어를 쓸 수 없습니다(권한부족)",
            color=config.error
        )
        await ctx.send(embed=embed)

bot.run(config.TOKEN)
