import discord
from discord import app_commands
from discord.ext import commands

class Clips(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clips_channel_id = 1373753580938330175
        self.clips_role_id = 1373753906974429254

    @app_commands.command(name="clip", description="Upload or repost a video clip with a caption and optional featuring.")
    @app_commands.describe(message_link="Link to an existing Discord message with a video",
                           caption="Caption for the clip",
                           featuring="Tag someone featured in the clip (optional)")
    async def clip(self, interaction: discord.Interaction, message_link: str = None, caption: str = "", featuring: discord.User = None):
        # Check if user has the proper role
        if not any(role.id == self.clips_role_id for role in interaction.user.roles):
            await interaction.response.send_message("❌ You don’t have permission to post clips.", ephemeral=True)
            return

        channel = self.bot.get_channel(self.clips_channel_id)
        if not channel:
            await interaction.response.send_message("❌ Clips channel not found.", ephemeral=True)
            return

        # Check for file or link
        has_video = False
        files = []
        if interaction.attachments:
            for attachment in interaction.attachments:
                if attachment.content_type and attachment.content_type.startswith("video/"):
                    files.append(await attachment.to_file())
                    has_video = True

        if not has_video and not message_link:
            await interaction.response.send_message("❌ Please upload a video or provide a message link containing a video.", ephemeral=True)
            return

        # Handle repost from message link
        if message_link and not has_video:
            try:
                parts = message_link.strip().split("/")
                message_channel_id = int(parts[-2])
                message_id = int(parts[-1])
                message_channel = self.bot.get_channel(message_channel_id)
                message = await message_channel.fetch_message(message_id)
                for attachment in message.attachments:
                    if attachment.content_type and attachment.content_type.startswith("video/"):
                        files.append(await attachment.to_file())
                        has_video = True
                        break
            except Exception:
                await interaction.response.send_message("❌ Could not retrieve video from the message link.", ephemeral=True)
                return

        if not has_video:
            await interaction.response.send_message("❌ No valid video found in the message link or attachment.", ephemeral=True)
            return

        # Build post content
        content = f"🎬 **New Clip Uploaded**
📤 Submitted by: {interaction.user.mention}"
        if featuring:
            content += f"
🎭 Featuring: {featuring.mention}"
        if caption:
            content += f"
📝 {caption}"

        await channel.send(content, files=files)
        await interaction.response.send_message("✅ Your clip has been posted!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Clips(bot))