import discord
from discord import app_commands
from discord.ext import commands

class BotSpeak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    allowed_role_id = 1395157495873540278

    async def has_permission(self, interaction: discord.Interaction):
        return any(role.id == self.allowed_role_id for role in interaction.user.roles)

    @app_commands.command(name="bottalk", description="Make the bot send a message in a channel.")
    @app_commands.describe(channel="Channel to send the message in", message="Message to send")
    async def bottalk(self, interaction: discord.Interaction, channel: discord.TextChannel, message: str):
        if not await self.has_permission(interaction):
            await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
            return

        files = []
        for attachment in interaction.attachments:
            f = await attachment.to_file()
            files.append(f)

        await channel.send(content=message, files=files)
        await interaction.response.send_message(f"✅ Message sent to {channel.mention}", ephemeral=True)

    @app_commands.command(name="botreply", description="Make the bot reply to a specific message.")
    @app_commands.describe(message_link="Link to the message to reply to", message="Message to send as a reply")
    async def botreply(self, interaction: discord.Interaction, message_link: str, message: str):
        if not await self.has_permission(interaction):
            await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
            return

        try:
            parts = message_link.strip().split("/")
            if len(parts) < 3:
                raise ValueError("Invalid message link.")

            guild_id = int(parts[-3])
            channel_id = int(parts[-2])
            msg_id = int(parts[-1])

            channel = self.bot.get_channel(channel_id)
            if not isinstance(channel, discord.TextChannel):
                raise ValueError("Channel not found or not text.")

            original_message = await channel.fetch_message(msg_id)

            files = []
            for attachment in interaction.attachments:
                f = await attachment.to_file()
                files.append(f)

            await original_message.reply(content=message, files=files)
            await interaction.response.send_message("✅ Replied to the message.", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"⚠️ Failed to reply: `{str(e)}`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BotSpeak(bot))
