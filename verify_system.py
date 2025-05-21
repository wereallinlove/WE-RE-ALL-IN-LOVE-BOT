
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

class VerifyButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Approve", style=discord.ButtonStyle.success, custom_id="approve"))
        self.add_item(discord.ui.Button(label="Deny", style=discord.ButtonStyle.danger, custom_id="deny"))

class VerifySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()

    @app_commands.command(name="verifychannel", description="Set the verify channel by ID.")
    @app_commands.describe(channel_id="The ID of the channel to use for verification.")
    async def verifychannel(self, interaction: discord.Interaction, channel_id: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to do this.", ephemeral=True)
            return

        channel = interaction.guild.get_channel(int(channel_id))
        if channel is None:
            await interaction.response.send_message("Invalid channel ID.", ephemeral=True)
            return

        self.config["verify_channel_id"] = int(channel_id)
        save_config(self.config)

        embed = discord.Embed(
            title="Verify",
            description="Click the button below to verify.",
            color=0xFF69B4
        )
        embed.set_footer(text="WE'RE ALL IN LOVE 2025")
        await channel.send(embed=embed, view=VerifyButtons())

        await interaction.response.send_message(f"Verify message sent in {channel.mention}", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.tree.add_command(self.verifychannel)

async def setup(bot):
    await bot.add_cog(VerifySystem(bot))
