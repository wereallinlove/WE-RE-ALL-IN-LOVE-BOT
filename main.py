import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

ADMIN_CHANNEL_ID = 1318298515948048549
APPROVED_ROLE_NAME = "WE'RE ALL IN LOVE"
VOICE_CHANNEL_ID = 137188628201131223

# Load Bell Command at Startup
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bell_every_hour.start()

@bot.event
async def on_member_join(member):
    await asyncio.sleep(1)
    channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if not channel:
        print("Admin channel not found.")
        return

    embed = discord.Embed(
        title="WE'RE ALL IN LOVE",
        description=f"{member.mention} joined\n\n**Grant them access to WE'RE ALL IN LOVE?**",
        color=discord.Color.magenta()
    )

    class ApproveButton(View):
        @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
        async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
            if ".approve" not in [role.name for role in interaction.user.roles]:
                await interaction.response.send_message("You don't have permission to approve.", ephemeral=True)
                return

            role = discord.utils.get(member.guild.roles, name=APPROVED_ROLE_NAME)
            if role:
                await member.add_roles(role)
                await interaction.response.send_message(f"{member.mention} has been approved.", ephemeral=False)
            else:
                await interaction.response.send_message("Role not found.", ephemeral=True)

    await channel.send(embed=embed, view=ApproveButton())

@bot.command()
@commands.has_role(".admin")
async def bell(ctx):
    vc = ctx.author.voice
    if not vc:
        await ctx.send("You must be in a voice channel.")
        return
    
    try:
        voice = await vc.channel.connect()
        voice.play(discord.FFmpegPCMAudio("bell.mp3"))
        while voice.is_playing():
            await asyncio.sleep(1)
        await voice.disconnect()
    except Exception as e:
        await ctx.send(f"Error: {e}")

@tasks.loop(minutes=60)
async def bell_every_hour():
    await bot.wait_until_ready()
    guild = bot.guilds[0]
    channel = guild.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            voice = await channel.connect()
            voice.play(discord.FFmpegPCMAudio("bell.mp3"))
            while voice.is_playing():
                await asyncio.sleep(1)
            await voice.disconnect()
        except Exception as e:
            print(f"Hourly bell error: {e}")

# Make sure to run the bot using an environment variable
import os
bot.run(os.getenv("DISCORD_TOKEN"))
