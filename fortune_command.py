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
        allowed_role = 1371885746415341648

        if interaction.channel.id != allowed_channel:
            return await interaction.response.send_message("You can only use this command in the right channel.", ephemeral=True)

        if not any(role.id == allowed_role for role in interaction.user.roles):
            return await interaction.response.send_message("You don’t have permission to use this command.", ephemeral=True)

        fortunes = [
            "You will receive an unsolicited confession. Ignore it.",
            "Someone you forgot about is about to pop up horny AND chaotic.",
            "Your vibe: looks mean, cries during aftercare.",
            "Someone you forgot about is about to pop up horny AND chaotic.",
            "You give off 'I heal by making it worse' energy.",
            "You will post something thirsty and @Joelle will see it first.",
            "You give off 'I heal by making it worse' energy.",
            "Your vibe: looks mean, cries during aftercare.",
            "You will post something thirsty and @Joelle will see it first.",
            "@Witchy is secretly in love with you. Unfortunately.",
            "Your next sneaky link will be emotionally unavailable *and* have an Android.",
            "You’re the main character. But of a dark comedy.",
            "Your ex is about to post something thirst-trappy and you will LIKE it.",
            "Your next sneaky link will be emotionally unavailable *and* have an Android.",
            "You give off 'would ghost God if He texted first' energy.",
            "You will fall in love with someone who calls you 'bro'.",
            "You’ll look hot but be miserable. Standard.",
            "You give off 'would ghost God if He texted first' energy.",
            "You will get blocked by someone you weren't even flirting with.",
            "Your FBI agent is disgusted. But entertained.",
            "You will say 'I'm done' and then go back for more.",
            "Your FBI agent is disgusted. But entertained.",
            "You give off 'I heal by making it worse' energy.",
            "You will fall in love with someone who calls you 'bro'.",
            "Your ex is about to post something thirst-trappy and you will LIKE it.",
            "You give off 'would ghost God if He texted first' energy.",
            "@Daddy is secretly in love with you. Unfortunately.",
            "You’re the villain in someone’s trauma story. Oops.",
            "Someone in this server thinks you're a little bitch. They're right.",
            "The next person you flirt with will have a foot fetish.",
            "You give off 'I heal by making it worse' energy.",
            "You're about to develop a crush on someone who listens to Nightcore.",
            "You will send a risky DM and get left on read by @Softie.",
            "Your search history will be leaked. On your birthday.",
            "You will cry in the shower. But like… sexy.",
            "You will fall in love with someone who calls you 'bro'.",
            "You will sext @Ghost and immediately regret it.",
            "You will sext @Witchy and immediately regret it.",
            "Someone in this server thinks you're a little bitch. They're right.",
            "You will get exposed in the groupchat. With screenshots.",
            "You will cry in the shower. But like… sexy.",
            "Your next sneaky link will be emotionally unavailable *and* have an Android.",
            "Someone is manifesting you… with evil intent.",
            "You will cry in the shower. But like… sexy.",
            "You will get blocked by someone you weren't even flirting with.",
            "You will sext @Baby and immediately regret it.",
            "You will fall in love with someone who calls you 'bro'.",
            "Your FBI agent is disgusted. But entertained.",
            "Your next sneaky link will be emotionally unavailable *and* have an Android.",
            "You’re the villain in someone’s trauma story. Oops.",
            "Your vibe: looks mean, cries during aftercare.",
            "You will get blocked by someone you weren't even flirting with.",
            "Your FBI agent is disgusted. But entertained.",
            "You will send a risky DM and get left on read by @Lurker.",
            "Your next situationship will last 2 orgasms.",
            "Your search history will be leaked. On your birthday.",
            "Someone you forgot about is about to pop up horny AND chaotic.",
            "Someone in this server thinks you're a little bitch. They're right.",
            "You will make eye contact with a demon. They’ll like you.",
            "You will get blocked by someone you weren't even flirting with.",
            "@Softie is watching your stories and judging silently.",
            "Someone in this server thinks you're a little bitch. They're right.",
            "You will get blocked by someone you weren't even flirting with.",
            "You will post something thirsty and @Joelle will see it first.",
            "You’ll look hot but be miserable. Standard.",
            "Your next situationship will last 2 orgasms.",
            "You give off 'I heal by making it worse' energy.",
            "You will make eye contact with a demon. They’ll like you.",
            "@Ghost is secretly in love with you. Unfortunately.",
            "@Witchy is watching your stories and judging silently.",
            "You will say 'I'm done' and then go back for more.",
            "Someone will kiss you and then ghost you for 4 days.",
            "You will wake up next to your mistake. Again.",
            "Someone you forgot about is about to pop up horny AND chaotic.",
            "You’re the main character. But of a dark comedy.",
            "You’ll look hot but be miserable. Standard.",
            "You will get exposed in the groupchat. With screenshots.",
            "You will post something thirsty and @Joelle will see it first.",
            "You will send a risky DM and get left on read by @Baby.",
            "You will cry in the shower. But like… sexy.",
            "You will cry in the shower. But like… sexy.",
            "You will get blocked by someone you weren't even flirting with.",
            "Someone will kiss you and then ghost you for 4 days.",
            "@Ghost is secretly in love with you. Unfortunately.",
            "You will sext @Daddy and immediately regret it.",
            "Your FBI agent is disgusted. But entertained.",
            "@Joelle is secretly in love with you. Unfortunately.",
            "You will send a risky DM and get left on read by @Softie.",
            "Someone you forgot about is about to pop up horny AND chaotic.",
            "@Baby is watching your stories and judging silently.",
            "You’ll look hot but be miserable. Standard.",
            "Someone is manifesting you… with evil intent.",
            "You will get exposed in the groupchat. With screenshots.",
            "You will sext @Lurker and immediately regret it.",
            "Your vibe: looks mean, cries during aftercare.",
            "You will post something thirsty and @Joelle will see it first.",
            "You will say 'I'm done' and then go back for more.",
            "You give off 'I heal by making it worse' energy.",
            "Someone in this server thinks you're a little bitch. They're right.",
            "You will cry in the shower. But like… sexy.",
            "Your vibe: looks mean, cries during aftercare.",
            "Someone in this server thinks you're a little bitch. They're right.",
            "Your next situationship will last 2 orgasms.",
            "You’re the villain in someone’s trauma story. Oops.",
            "You will get exposed in the groupchat. With screenshots.",
            "You give off 'would ghost God if He texted first' energy.",
            "You will post something thirsty and @Joelle will see it first.",
            "You give off 'I heal by making it worse' energy.",
            "You’re the villain in someone’s trauma story. Oops.",
            "Your next situationship will last 2 orgasms.",
            "You will sext @Daddy and immediately regret it.",
            "Your vibe: looks mean, cries during aftercare.",
            "You will post something thirsty and @Joelle will see it first.",
            "Someone will kiss you and then ghost you for 4 days.",
            "Your FBI agent is disgusted. But entertained.",
            "You will fall in love with someone who calls you 'bro'.",
            "You will sext @Baby and immediately regret it.",
            "@DemonBaby is secretly in love with you. Unfortunately.",
            "You will receive an unsolicited confession. Ignore it.",
            "Your vibe: looks mean, cries during aftercare.",
        ]

        selected = random.choice(fortunes)
        embed = discord.Embed(
            title=f"**{{interaction.user.display_name}}'s Fortune**",
            description=f"*{{selected}}*",
            color=discord.Color.magenta()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fortune(bot))
