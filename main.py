import discord
from discord.ext import commands
from discord import app_commands
import os
from datetime import datetime

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Server + Channel + Role IDs
APPROVER_ROLE_ID = 1372695389555130420
VERIFIED_ROLE_ID = 1371885746415341648
VERIFY_CHANNEL_ID = 1372762677868498994
LOVELETTER_CHANNEL_ID = 1372782806446506047
PIN_CHANNEL_ID = 1372918174877614100
PIN_ROLE_ID = 1372919338776133723

LOVELETTER_IMAGE_URL = "https://media.tenor.com/Ln9wPaZ0N5sAAAAM/hearts-love.gif"

bot.tree.synced = False

class ApproveDenyView(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success, custom_id="approve_button")
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        approver_role = interaction.guild.get_role(APPROVER_ROLE_ID)
        if approver_role not in interaction.user.roles:
            await interaction.response.send_message("You don't have permission to approve members.", ephemeral=True)
            return

        role = interaction.guild.get_role(VERIFIED_ROLE_ID)
        if role:
            await self.member.add_roles(role)
            await interaction.response.send_message(f"{self.member.mention} has been approved and given the role.")

            approved_embed = discord.Embed(
                title="✅ Member Approved",
                description=f"{self.member.mention} has been approved by {interaction.user.mention}.",
                color=discord.Color.green()
            )
            await interaction.channel.send(embed=approved_embed)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger, custom_id="deny_button")
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        approver_role = interaction.guild.get_role(APPROVER_ROLE_ID)
        if approver_role not in interaction.user.roles:
            await interaction.response.send_message("You don't have permission to deny members.", ephemeral=True)
            return

        await self.member.kick(reason="Denied by approver")
        await interaction.response.send_message(f"{self.member.mention} has been denied and kicked.")

        denied_embed = discord.Embed(
            title="❌ Member Denied",
            description=f"{self.member.mention} was denied access by {interaction.user.mention}.",
            color=discord.Color.red()
        )
        await interaction.channel.send(embed=denied_embed)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}!")
    if not bot.tree.synced:
        try:
            await bot.tree.sync()  # Global sync instead of guild-only
            bot.tree.synced = True
            print("✅ Slash commands globally synced.")
        except Exception as e:
            print(f"Sync failed: {e}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(VERIFY_CHANNEL_ID)
    guild = member.guild

    if channel:
        current_year = datetime.now().year
        embed = discord.Embed(
            title="New Member Joined",
            description=f"{member.mention} has joined the server.\n\nPlease approve or deny access.",
            color=discord.Color.from_rgb(255, 105, 180)
        )

        if guild.icon:
            embed.set_image(url=guild.icon.url)

        embed.set_footer(text=f"WE'RE ALL IN LOVE {current_year}")

        view = ApproveDenyView(member)
        await channel.send(embed=embed, view=view)

@bot.tree.command(name="loveletter", description="Send an anonymous love letter to someone")
@app_commands.describe(user="The person you want to send the letter to", message="The note to send anonymously")
async def loveletter(interaction: discord.Interaction, user: discord.User, message: str):
    current_year = datetime.now().year
    embed = discord.Embed(
        title="💌 Love Letter",
        description=f"*{message}*\n\nTo: {user.mention}",
        color=discord.Color.from_rgb(255, 80, 160)
    )
    embed.set_image(url=LOVELETTER_IMAGE_URL)
    embed.set_footer(text=f"WE'RE ALL IN LOVE {current_year}")

    channel = bot.get_channel(LOVELETTER_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Your love letter was sent anonymously. 💌", ephemeral=True)
    else:
        await interaction.response.send_message("Couldn't find the love letter channel.", ephemeral=True)

@bot.tree.command(name="pin", description="Post a memory (image or video) to the pins channel.")
@app_commands.describe(caption="Optional caption for the memory")
async def pin(interaction: discord.Interaction, caption: str = None):
    if PIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    if not interaction.attachments:
        await interaction.response.send_message("You must attach an image or video to pin.", ephemeral=True)
        return

    file = interaction.attachments[0]
    current_year = datetime.now().year

    embed = discord.Embed(
        title="New Pin",
        color=discord.Color.from_rgb(255, 100, 180)
    )

    if caption:
        embed.description = f"*{caption}*"

    embed.set_image(url=file.url)
    embed.add_field(name="Submitted by", value=interaction.user.mention, inline=False)
    embed.set_footer(text=f"WE'RE ALL IN LOVE {current_year}")

    channel = bot.get_channel(PIN_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
        await interaction.response.send_message("Your memory was pinned. 📌", ephemeral=True)
    else:
        await interaction.response.send_message("Couldn't find the pin channel.", ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))