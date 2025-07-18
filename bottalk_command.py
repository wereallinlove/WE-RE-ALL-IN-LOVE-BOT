import discord
from discord import app_commands
from discord.ext import commands

class BotTalk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bottalk", description="Make the bot send a message in a channel.")
    @app_commands.describe(channel="Channel to send the message in", message="Message to send")
    async def bottalk(self, interaction: discord.Interaction, channel: discord.TextChannel, message: str):
        allowed_role_id = 1395157495873540278

        # Check if the user has the required role
        if not any(role.id == allowed_role_id for role in interaction.user.roles):
            await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
            return

        try:
            await channel.send(message)
            await interaction.response.send_message(f"✅ Message sent to {channel.mention}", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to send messages in that channel.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Failed to send message: `{str(e)}`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BotTalk(bot))
