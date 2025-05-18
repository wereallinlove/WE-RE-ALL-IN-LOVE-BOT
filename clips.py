import discord
from discord import app_commands
from discord.ext import commands

class Clips(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clips_channel_id = 1373753580938330175
        self.clips_role_id = 1373753906974429254

    @app_commands.command(name="clip", description="Post a video clip with caption and optional featuring.")
    @app_commands.describe(
        message_link="Discord message link containing a video",
        caption="Caption for the clip (optional)",
        featuring="User featured in the clip (optional)"
    )
    async def clip(
        self,
        interaction: discord.Interaction,
        message_link: str,
        caption: str = "",
        featuring: discord.User = None
    ):
        if not any(role.id == self.clips_role_id for role in interaction.user.roles):
            await interaction.response.send_message("❌ You don’t have permission to post clips.", ephemeral=True)
            return

        channel = self.bot.get_channel(self.clips_channel_id)
        if not channel:
            await interaction.response.send_message("❌ Clips channel not found.", ephemeral=True)
            return

        files = []
        has_video = False

        try:
            parts = message_link.strip().split("/")
            msg_channel_id = int(parts[-2])
            msg_id = int(parts[-1])
            msg_channel = self.bot.get_channel(msg_channel_id)
            msg = await msg_channel.fetch_message(msg_id)

            for attachment in msg.attachments:
                if attachment.content_type and attachment.content_type.startswith("video/"):
                    files.append(await attachment.to_file())
                    has_video = True
                    break
        except Exception:
            await interaction.response.send_message("❌ Could not retrieve video from the message link.", ephemeral=True)
            return

        if not has_video:
            await interaction.response.send_message("❌ No video found in the provided message.", ephemeral=True)
            return

        content = f"🎬 Submitted by: {interaction.user.mention}"
        if featuring:
            content += f"\n🎭 Featuring: {featuring.mention}"
        if caption:
            content += f"\n📝 {caption}"

        await channel.send(content, files=files)
        await interaction.response.send_message("✅ Your clip has been posted!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Clips(bot))
