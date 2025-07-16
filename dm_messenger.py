import discord
from discord.ext import commands
from discord import app_commands

ALLOWED_ROLE_ID = 1371681883796017222
ALLOWED_CHANNEL_ID = 1395149106388795577
RELAY_CHANNEL_ID = 1395149106388795577
EMBED_COLOR = discord.Color.pink()

class Messenger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="message", description="Send a private DM to a user by ID or username")
    @app_commands.describe(user="User ID or tag (e.g., 1234567890 or name#0001)", message="The message to send", attachment="Optional file to attach")
    @app_commands.checks.has_role(ALLOWED_ROLE_ID)
    async def message(self, interaction: discord.Interaction, user: str, message: str, attachment: discord.Attachment = None):
        if interaction.channel_id != ALLOWED_CHANNEL_ID:
            await interaction.response.send_message("❌ This command can only be used in the private messaging channel.", ephemeral=True)
            return

        target_user = None

        # Try fetching by ID
        try:
            target_user = await self.bot.fetch_user(int(user))
        except:
            # Try by username#discriminator
            for u in self.bot.users:
                if str(u) == user:
                    target_user = u
                    break

        if not target_user:
            await interaction.response.send_message(embed=discord.Embed(
                title="❌ User Not Found",
                description="Make sure the user ID or username#tag is correct.",
                color=discord.Color.red()
            ))
            return

        try:
            content = message
            files = [await attachment.to_file()] if attachment else None
            await target_user.send(content, file=files[0] if files else None)

            embed = discord.Embed(
                title="✅ Message Sent",
                description=f"Successfully messaged <@{target_user.id}>.\n\n**Message:**\n{message}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)

        except Exception:
            await interaction.response.send_message(embed=discord.Embed(
                title="❌ Failed to Send",
                description="Could not DM this user. They may have DMs disabled.",
                color=discord.Color.red()
            ))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild or message.author.bot:
            return  # Only listen to DMs from real users

        relay_channel = self.bot.get_channel(RELAY_CHANNEL_ID)
        if not relay_channel:
            return

        embed = discord.Embed(
            title="📨 DM Reply Received",
            description=message.content if message.content else "*[No text]*",
            color=EMBED_COLOR
        )
        embed.set_author(
            name=f"{message.author} ({message.author.id})",
            icon_url=message.author.display_avatar.url
        )

        # Send embed first
        await relay_channel.send(embed=embed)

        # Send attachments, if any
        for attachment in message.attachments:
            await relay_channel.send(
                content=f"📎 Attachment from {message.author}:", 
                file=await attachment.to_file()
            )

async def setup(bot):
    await bot.add_cog(Messenger(bot))
