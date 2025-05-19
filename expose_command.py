import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone, timedelta
import random  # ✅ THIS FIXES YOUR ERROR

EXPOSE_ROLE_ID = 1371885746415341648
EXPOSE_CHANNEL_ID = 1318298515948048549
EMBED_COLOR = discord.Color.from_rgb(231, 84, 128)  # bright pink

class Expose(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="expose", description="Expose someone with one of their own messages.")
    @app_commands.checks.has_role(EXPOSE_ROLE_ID)
    async def expose(self, interaction: discord.Interaction, user: discord.Member):
        if interaction.channel.id != EXPOSE_CHANNEL_ID:
            await interaction.response.send_message("You can only use this command in the designated channel.", ephemeral=True)
            return

        messages = []
        async for message in interaction.channel.history(limit=1000):
            if message.author.id != user.id:
                continue
            if message.content.startswith("/") or message.content.startswith("!") or message.author.bot:
                continue
            if len(message.content) < 8:
                continue
            if any(x in message.content.lower() for x in [
                "i want", "daddy", "ride", "moan", "feet", "bark", "lick", "piss", "shit", "fuck", "sex", "onlyfans",
                "ex", "bitch", "kill", "dead", "hate", "nsfw", "horny", "dream", "obsessed", "kneel", "bite", "choke",
                "step on", "ruin", "slave", "leash", "panties", "wet", "thirst", "please", "unholy", "sin", "impale",
                "slut", "raw", "breed", "hole", "scream", "pray", "desperate", "boyfriend", "girlfriend", "date",
                "nudes", "simp", "dilf", "mommy", "daddy issues"
            ]):
                messages.append(message)
            elif len(message.content.split()) >= 6:
                messages.append(message)

        if not messages:
            await interaction.response.send_message("No juicy messages found to expose them with 😔", ephemeral=True)
            return

        selected = random.choice(messages)
        timestamp = selected.created_at.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-4)))
        formatted_time = timestamp.strftime("%B %d, %Y at %I:%M %p")
        channel_name = f"#{selected.channel.name}"

        embed = discord.Embed(
            title=f"{user.display_name} exposed:",
            description=f"\"{selected.content}\"",
            color=EMBED_COLOR
        )
        embed.set_footer(text=f"— Message from {channel_name}, {formatted_time}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Expose(bot))
