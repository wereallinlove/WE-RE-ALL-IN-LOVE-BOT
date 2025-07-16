import discord
from discord.ext import commands
from discord import app_commands

ALLOWED_ROLE_ID = 1395157495873540278
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
        try:
            target_user = await self.bot.fetch_user(int(user))
        except:
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
            files = [await attachment.to_file()] if attachment else None
            await target_user.send(message, file=files[0] if files else None)

            embed = discord.Embed(
                title="✅ Message Sent",
                description=f"Message successfully sent to <@{target_user.id}>.\n\n**Message:**\n{message}",
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
            return

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

        view = ReplyButton(message.author.id)
        await relay_channel.send(embed=embed, view=view)

        for attachment in message.attachments:
            await relay_channel.send(
                content=f"📎 Attachment from {message.author}:", 
                file=await attachment.to_file()
            )

class ReplyButton(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="Reply", style=discord.ButtonStyle.primary)
    async def reply(self, interaction: discord.Interaction, button: discord.ui.Button):
        if ALLOWED_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("❌ You don't have permission to use this.", ephemeral=True)
            return

        await interaction.response.send_modal(ReplyModal(user_id=self.user_id, responder=interaction.user))

class ReplyModal(discord.ui.Modal, title="Reply to DM"):
    response = discord.ui.TextInput(label="Your message", style=discord.TextStyle.paragraph, required=True)

    def __init__(self, user_id: int, responder: discord.Member):
        super().__init__()
        self.user_id = user_id
        self.responder = responder

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user = await interaction.client.fetch_user(self.user_id)
            await user.send(self.response.value)

            channel = interaction.client.get_channel(RELAY_CHANNEL_ID)
            if channel:
                embed = discord.Embed(
                    title="✅ Reply Sent",
                    description=f"**To:** <@{user.id}>\n**Message:** {self.response.value}",
                    color=discord.Color.green()
                )
                embed.set_footer(text=f"Sent by {self.responder}")
                await channel.send(embed=embed)

            await interaction.response.send_message("Reply sent.", ephemeral=True)

        except:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Failed to Send",
                    description="Could not DM this user.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Messenger(bot))
