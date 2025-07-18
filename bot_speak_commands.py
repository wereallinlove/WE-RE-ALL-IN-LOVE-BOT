import discord
from discord.ext import commands
from discord import app_commands

ALLOWED_ROLE_ID = 1395157495873540278  # Only users with this role can use these commands

class BotSpeak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bottalk", description="Make the bot talk in a channel")
    @app_commands.describe(channel="Channel to send the message in", message="Message to send", file="Optional file/image to send")
    async def bottalk(self, interaction: discord.Interaction, channel: discord.TextChannel, message: str, file: discord.Attachment = None):
        # Role check
        if not any(role.id == ALLOWED_ROLE_ID for role in interaction.user.roles):
            await interaction.response.send_message("❌ You don’t have permission to use this command.", ephemeral=True)
            return

        # Prepare file (if any)
        file_to_send = await file.to_file() if file else None

        await channel.send(content=message, file=file_to_send)
        await interaction.response.send_message("✅ Message sent!", ephemeral=True)

    @app_commands.command(name="botreply", description="Make the bot reply to a specific message")
    @app_commands.describe(message_link="Link to the message to reply to", message="Reply message content", file="Optional file/image to attach")
    async def botreply(self, interaction: discord.Interaction, message_link: str, message: str, file: discord.Attachment = None):
        # Role check
        if not any(role.id == ALLOWED_ROLE_ID for role in interaction.user.roles):
            await interaction.response.send_message("❌ You don’t have permission to use this command.", ephemeral=True)
            return

        try:
            parts = message_link.split("/")
            channel_id = int(parts[-2])
            message_id = int(parts[-1])

            channel = await self.bot.fetch_channel(channel_id)
            target_message = await channel.fetch_message(message_id)

            file_to_send = await file.to_file() if file else None

            await target_message.reply(content=message, file=file_to_send)
            await interaction.response.send_message("✅ Reply sent!", ephemeral=True)

        except Exception as e:
            print(f"Error replying to message: {e}")
            await interaction.response.send_message("❌ Failed to reply. Make sure the link is valid.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BotSpeak(bot))