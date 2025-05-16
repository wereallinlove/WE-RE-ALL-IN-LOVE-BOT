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

# Fixed IDs
GUILD_ID = 1318298515948048546
APPROVER_ROLE_ID = 1372695389555130420
VERIFIED_ROLE_ID = 1371885746415341648
VERIFY_CHANNEL_ID = 1372762677868498994

# Boost gif with black background assumed
BOOST_IMAGE_URL = "https://i.pinimg.com/originals/d3/c6/8a/d3c68aeb6f9ead3e57f80f12d12304b8.gif"

# Control flag to prevent resyncing on every restart
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
            await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
            bot.tree.synced = True
            print("✅ Slash commands synced.")
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

# Slash command to test the boost embed
@bot.tree.command(name="boost", description="Preview the server boost thank-you embed.")
async def boost(interaction: discord.Interaction):
    current_year = datetime.now().year
    user = interaction.user

    embed = discord.Embed(
        title="Thank you for boosting **WE'RE ALL IN LOVE**",
        description=f"{user.mention} has just boosted the server 🖤🎀",
        color=discord.Color.from_rgb(255, 105, 200)
    )
    embed.set_image(url=BOOST_IMAGE_URL)
    embed.set_footer(text=f"WE'RE ALL IN LOVE {current_year}")

    channel = bot.get_channel(VERIFY_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
        await interaction.response.send_message("✅ Boost preview sent.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Couldn't find the verify channel.", ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))
