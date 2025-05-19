import discord
from discord.ext import commands
from discord import app_commands
import random
import datetime

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
            "You will die doing something dumb — but hot.",
            "You give off ‘I text back if they’re hot enough’ energy.",
            "You miss someone who doesn’t even remember your birthday.",
            "The vibes will shift. And you will be unprepared.",
            "You give off ‘I text back if they’re hot enough’ energy.",
            "You will get back with your ex. Sexually. Not emotionally.",
            "You will win an argument, but lose your charger.",
            "You peaked… but in a nostalgic, romantic way.",
            "Someone’s thinking about you. In the shower.",
            "You peaked… but in a nostalgic, romantic way.",
            "You miss someone who doesn’t even remember your birthday.",
            "The group chat is talking about you. It’s not that bad.",
            "You are the main character, but like a tragic one.",
            "You will win an argument, but lose your charger.",
            "You won’t die alone, but you’ll wish you had.",
            "Your playlist is a cry for help — and fashion.",
            "You were right… but they’ll never admit it.",
            "You miss someone who doesn’t even remember your birthday.",
            "You will get back with your ex. Sexually. Not emotionally.",
            "You are the main character, but like a tragic one.",
            "You were right… but they’ll never admit it.",
            "Your funeral will be catered. Hope you like shrimp.",
            "You will die doing something dumb — but hot.",
            "You will make money… but it won’t feel legal.",
            "Someone is stalking your old Instagram. Pray it’s not your mom.",
            "You are the main character, but like a tragic one.",
            "Someone’s thinking about you. In the shower.",
            "Someone you ghosted is going to hex you this week.",
            "You give off ‘I text back if they’re hot enough’ energy.",
            "The vibes will shift. And you will be unprepared.",
            "They didn’t love you. They just liked the attention.",
            "Someone’s thinking about you. In the shower.",
            "You were right… but they’ll never admit it.",
            "Your playlist is a cry for help — and fashion.",
            "The vibes will shift. And you will be unprepared.",
            "Love is coming. But it’s going to ruin everything first.",
            "The vibes will shift. And you will be unprepared.",
            "Someone is stalking your old Instagram. Pray it’s not your mom.",
            "They didn’t love you. They just liked the attention.",
            "You won’t die alone, but you’ll wish you had.",
            "You will cry. But in a pretty, dramatic, cinematic way.",
            "Your funeral will be catered. Hope you like shrimp.",
            "You were right… but they’ll never admit it.",
            "Someone you ghosted is going to hex you this week.",
            "You will make money… but it won’t feel legal.",
            "You're about to ruin your own life… deliciously.",
            "You peaked… but in a nostalgic, romantic way.",
            "You are the main character, but like a tragic one.",
            "You will make money… but it won’t feel legal.",
            "Delete that post. Or don’t. It’s already screenshotted.",
            "You give off ‘I text back if they’re hot enough’ energy.",
            "You will win an argument, but lose your charger.",
            "Your funeral will be catered. Hope you like shrimp.",
            "You peaked… but in a nostalgic, romantic way.",
            "Love is coming. But it’s going to ruin everything first.",
            "They didn’t love you. They just liked the attention.",
            "The group chat is talking about you. It’s not that bad.",
            "Death is stalking you. But like… in a flirty way.",
            "Death is stalking you. But like… in a flirty way.",
            "Delete that post. Or don’t. It’s already screenshotted.",
            "The group chat is talking about you. It’s not that bad.",
            "The next message you receive will change your mood forever.",
            "Death is stalking you. But like… in a flirty way.",
            "You will cry. But in a pretty, dramatic, cinematic way.",
            "You will die doing something dumb — but hot.",
            "You will cry. But in a pretty, dramatic, cinematic way.",
            "Someone’s thinking about you. In the shower.",
            "You miss someone who doesn’t even remember your birthday.",
            "You won’t die alone, but you’ll wish you had.",
            "Your funeral will be catered. Hope you like shrimp.",
            "The next message you receive will change your mood forever.",
            "Someone is stalking your old Instagram. Pray it’s not your mom.",
            "You won’t die alone, but you’ll wish you had.",
            "You will win an argument, but lose your charger.",
            "You will get back with your ex. Sexually. Not emotionally.",
            "You're about to ruin your own life… deliciously.",
            "They didn’t love you. They just liked the attention.",
            "The next message you receive will change your mood forever.",
            "Someone you ghosted is going to hex you this week.",
            "Someone you ghosted is going to hex you this week.",
            "The group chat is talking about you. It’s not that bad.",
            "The next message you receive will change your mood forever.",
            "You will die doing something dumb — but hot.",
            "You will get back with your ex. Sexually. Not emotionally.",
            "You're about to ruin your own life… deliciously.",
            "You will cry. But in a pretty, dramatic, cinematic way.",
            "Death is stalking you. But like… in a flirty way.",
            "Delete that post. Or don’t. It’s already screenshotted.",
            "Your next situationship will last 6 business days.",
            "Your playlist is a cry for help — and fashion.",
            "Your playlist is a cry for help — and fashion.",
            "Your next situationship will last 6 business days.",
            "Someone is stalking your old Instagram. Pray it’s not your mom.",
            "Delete that post. Or don’t. It’s already screenshotted.",
            "Love is coming. But it’s going to ruin everything first.",
            "Love is coming. But it’s going to ruin everything first.",
            "Your next situationship will last 6 business days.",
            "You will make money… but it won’t feel legal.",
            "Your next situationship will last 6 business days.",
            "You're about to ruin your own life… deliciously.",
        ]

        selected = random.choice(fortunes)
        embed = discord.Embed(
            title="**Your Fortune**",
            description=f"*{selected}*",
            color=discord.Color.magenta()
        )
        embed.set_footer(text=f"WE'RE ALL IN LOVE {datetime.datetime.now().year}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fortune(bot))
