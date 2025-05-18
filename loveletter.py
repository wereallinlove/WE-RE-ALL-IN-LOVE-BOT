import discord
from discord import app_commands
from discord.ext import commands

class LoveLetterView(discord.ui.View):
    def __init__(self, bot, message_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.message_id = message_id

    @discord.ui.button(label="🎀 Reveal Early", style=discord.ButtonStyle.danger, custom_id="reveal_early")
    async def reveal(self, interaction: discord.Interaction, button: discord.ui.Button):
        admin_role_id = 1371681883796017222

        if not any(role.id == admin_role_id for role in interaction.user.roles):
            await interaction.response.send_message("❌ Only admins can reveal the sender.", ephemeral=True)
            return

        cog = self.bot.get_cog("LoveLetter")
        if self.message_id not in cog.sent_messages:
            await interaction.response.send_message("❌ This letter was already revealed or not found.", ephemeral=True)
            return

        sender_id, recipient_id = cog.sent_messages.pop(self.message_id)
        sender = self.bot.get_user(sender_id)
        recipient = self.bot.get_user(recipient_id)

        embed = discord.Embed(
            title="💚 Love Letter Revealed!",
            description=f"{recipient.mention}, this love letter was sent by {sender.mention}",
            color=discord.Color.green()
        )

        channel = interaction.channel or self.bot.get_channel(interaction.channel_id)
        await channel.send(embed=embed)
        await interaction.response.send_message("✅ Letter has been revealed.", ephemeral=True)
        self.stop()

class LoveLetter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.love_channel_id = 1373733852534804540
        self.verified_role_id = 1371885746415341648
        self.reveal_emoji = "🎀"
        self.reaction_threshold = 5
        self.sent_messages = {}

    @app_commands.command(name="loveletter", description="Send a secret love letter anonymously.")
    @app_commands.checks.has_role(1371885746415341648)
    async def loveletter(self, interaction: discord.Interaction, user: discord.User, message: str):
        channel = self.bot.get_channel(self.love_channel_id)
        if not channel:
            await interaction.response.send_message("Love letter channel not found.", ephemeral=True)
            return

        embed = discord.Embed(
            title="💌 Love Letter",
            description=f"*{message}*\n\nTo: {user.mention}",
            color=discord.Color.from_str("#ff5ba2")
        )
        embed.set_image(url="https://media.tenor.com/v4xmu4vSzQ4AAAAM/love-letter-love-letters.gif")
        embed.set_footer(text="Get 5 🎀 reactions to reveal who anonymously sent this letter")

        view = LoveLetterView(self.bot, message_id=None)
        sent = await channel.send(embed=embed, view=view)
        await sent.add_reaction(self.reveal_emoji)

        self.sent_messages[sent.id] = (interaction.user.id, user.id)
        view.message_id = sent.id  # update view's reference
        await interaction.response.send_message("💌 Your anonymous love letter has been sent!", ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id not in self.sent_messages:
            return
        if str(payload.emoji) != self.reveal_emoji:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=self.reveal_emoji)

        if reaction and reaction.count >= self.reaction_threshold:
            sender_id, recipient_id = self.sent_messages.pop(payload.message_id)
            sender = self.bot.get_user(sender_id)
            recipient = self.bot.get_user(recipient_id)

            embed = discord.Embed(
                title="💚 Love Letter Revealed!",
                description=f"{recipient.mention}, this love letter was sent by {sender.mention}",
                color=discord.Color.green()
            )
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LoveLetter(bot))
