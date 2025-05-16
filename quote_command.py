import discord
from discord import app_commands
from datetime import datetime

QUOTE_CHANNEL_ID = 1372918174877614100

def setup(bot):
    @bot.tree.command(name="quote", description="Quote a message and send it to the pins channel.")
    @app_commands.describe(message_link="Right-click a message > Copy Message Link, then paste it here")
    async def quote(interaction: discord.Interaction, message_link: str):
        await interaction.response.defer(ephemeral=True)

        try:
            parts = message_link.strip("/").split("/")
            if "discord.com" in message_link:
                message_id = int(parts[-1])
                channel_id = int(parts[-2])
            else:
                await interaction.followup.send("Invalid link format.", ephemeral=True)
                return

            channel = interaction.guild.get_channel(channel_id)
            if not channel:
                await interaction.followup.send("Could not find the message channel.", ephemeral=True)
                return

            message = await channel.fetch_message(message_id)

            current_year = datetime.now().year
            timestamp = message.created_at.strftime("%B %d, %Y at %I:%M %p")

            embed = discord.Embed(
                title=f"Quote from {message.author.display_name}",
                description=f"*{message.content}*\n\n— ({message.author.mention}, {timestamp})",
                color=discord.Color.blue()
            )

            # Add profile picture as thumbnail
            embed.set_thumbnail(url=message.author.display_avatar.url)
            embed.set_footer(text=f"WE'RE ALL IN LOVE {current_year}")

            quote_channel = interaction.guild.get_channel(QUOTE_CHANNEL_ID)
            if quote_channel:
                await quote_channel.send(embed=embed)
                await interaction.followup.send("Quote posted!", ephemeral=True)
            else:
                await interaction.followup.send("Could not find the quote channel.", ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"Error quoting message: {str(e)}", ephemeral=True)