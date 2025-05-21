
import discord
from discord.ext import commands
from discord import app_commands
import json
import os

CONFIG_FILE = "verify_config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

class VerifySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()

    @app_commands.command(name="verify", description="Verify a new member.")
    async def verify(self, interaction: discord.Interaction):
        verify_channel_id = self.config.get("verify_channel_id")
        if not verify_channel_id:
            await interaction.response.send_message("No verify channel has been set. Use /verify setchannel to set one.", ephemeral=True)
            return

        verify_channel = interaction.guild.get_channel(verify_channel_id)
        if not verify_channel:
            await interaction.response.send_message("The configured verify channel no longer exists. Please set it again.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Verify",
            description="Click the button below to verify.",
            color=0xFF69B4
        )
        embed.set_footer(text="WE'RE ALL IN LOVE 2025")
        await verify_channel.send(embed=embed, view=VerifyButtons())

        await interaction.response.send_message("Verification embed sent!", ephemeral=True)

    @app_commands.command(name="setchannel", description="Set the verification channel.")
    @app_commands.describe(channel="The channel to use for verification.")
    async def setchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to do this.", ephemeral=True)
            return

        self.config["verify_channel_id"] = channel.id
        save_config(self.config)

        await interaction.response.send_message(f"Verify channel set to {channel.mention}", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.tree.add_command(self.verify)
        self.bot.tree.add_command(self.setchannel)

class VerifyButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Approve", style=discord.ButtonStyle.success, custom_id="approve"))
        self.add_item(discord.ui.Button(label="Deny", style=discord.ButtonStyle.danger, custom_id="deny"))

async def setup(bot):
    await bot.add_cog(VerifySystem(bot))
