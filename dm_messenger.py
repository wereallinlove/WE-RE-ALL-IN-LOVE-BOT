import discord
from discord.ext import commands
from discord import app_commands

ALLOWED_ROLE_ID = 1371681883796017222
ALLOWED_CHANNEL_ID = 1395149106388795577
RELAY_CHANNEL_ID = 1395149106388795577  # where replies from users are shown
EMBED_COLOR = discord.Color.pink()

class Messenger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="message", description="DM a user anonymously")
    @app_commands.describe(user_id="The Discord user ID", message="The message to send")
    @app_commands.checks.has_role(ALLOWED_ROLE_ID)
    async def message(self, interaction: discord.Interaction, user_id: str, message: str):
        if interaction.channel_id != ALLOWED_CHANNEL_ID:
            await interaction.response.send_message(
                "❌ This command can only be used in the private messaging channel.", ephemeral=True
            )
            return

        try:
            user = await self.bot.fetch_user(int(user_id))
            await user.send(embed=discord.Embed(
                title="📩 You received a message",
                description=message,
                color=EMBED_COLOR
            ))
            await interaction.response.send_message(embed=discord.Embed(
                title="✅ Message Sent",
                description=f"Successfully messaged <@{user.id}>.",
                color=discord.Color.green()
            ))
        except Exception:
            await interaction.response.send_message(embed=discord.Embed(
                title="❌ Failed to Send",
                description="Could not DM this user. They may have DMs disabled.",
                color=discord.Color.red()
            ))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is not None or message.author.bot:
            return  # only process DMs from real users

        relay_channel = self.bot.get_channel(RELAY_CHANNEL_ID)
        if relay_channel:
            embed = discord.Embed(
                title="📨 DM Reply Received",
                description=message.content,
                color=EMBED_COLOR
            )
            embed.set_author(name=f"{message.author} ({message.author.id})", icon_url=message.author.display_avatar.url)
            await relay_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Messenger(bot))
