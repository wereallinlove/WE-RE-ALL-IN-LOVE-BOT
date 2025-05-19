
import discord
from discord.ext import commands
from discord import app_commands
import random

class Fortune(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="fortune")
    async def fortune(self, interaction: discord.Interaction):
        allowed_channel = 1373112868249145485
        allowed_role_id = 1371885746415341648

        if interaction.channel.id != allowed_channel:
            return await interaction.response.send_message("You can only use this command in the right channel.", ephemeral=True)

        if not any(role.id == allowed_role_id for role in interaction.user.roles):
            return await interaction.response.send_message("You don’t have permission to use this command.", ephemeral=True)

        verified_role = discord.utils.get(interaction.guild.roles, id=allowed_role_id)
        verified_members = [member.mention for member in interaction.guild.members if verified_role in member.roles and member != interaction.user]
        mention = random.choice(verified_members) if verified_members else "someone"

        fortunes = [
            "You will sext {{user}} and immediately regret it.",
            "Your next situationship will last 2 orgasms.",
            "Someone in this server thinks you're a little bitch. They're right.",
            "You will say 'I'm done' and then go back for more.",
            "You will post something thirsty and {{user}} will see it first.",
            "You will fall in love with someone who calls you 'bro'.",
            "{{user}} is secretly in love with you. Unfortunately.",
            "You will get blocked by someone you weren't even flirting with.",
            "Your FBI agent is disgusted. But entertained.",
            "You will receive an unsolicited confession. Ignore it.",
            "Your vibe: looks mean, cries during aftercare.",
            "You will make eye contact with a demon. They’ll like you.",
            "Your search history will be leaked. On your birthday.",
            "Someone will kiss you and then ghost you for 4 days.",
            "You give off 'I heal by making it worse' energy.",
            "You're about to develop a crush on someone who listens to Nightcore.",
            "Your next sneaky link will be emotionally unavailable *and* have an Android.",
            "You will send a risky DM and get left on read by {{user}}.",
            "You will wake up next to your mistake. Again.",
            "You will get exposed in the groupchat. With screenshots.",
            "The next person you flirt with will have a foot fetish.",
            "Your ex is about to post something thirst-trappy and you will LIKE it.",
            "You’re the villain in someone’s trauma story. Oops.",
            "Someone is manifesting you… with evil intent.",
            "You’ll look hot but be miserable. Standard.",
            "You will cry in the shower. But like… sexy.",
            "Someone you forgot about is about to pop up horny AND chaotic.",
            "Your nudes are safe. But your reputation isn’t.",
            "{{user}} is watching your stories and judging silently.",
            "You’re the main character. But of a dark comedy.",
            "You give off 'would ghost God if He texted first' energy.",
        ]

        selected = random.choice(fortunes)
        selected = selected.replace("{user}", mention)

        embed = discord.Embed(
            title=f"{interaction.user.display_name}'s Fortune",
            description=f"*{selected}*",
            color=discord.Color.magenta()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fortune(bot))
