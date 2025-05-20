import random
import discord
from discord import app_commands
from discord.ext import commands

ROAST_CHANNEL_ID = 1318298515948048549
VERIFIED_ROLE_ID = 1371885746415341648
ADMIN_ROLE_ID = 1371681883796017222

class RoastValentine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}

    @app_commands.command(name="roastvalentine", description="Roast Valentine brutally and without mercy.")
    @app_commands.checks.has_role(VERIFIED_ROLE_ID)
    async def roastvalentine(self, interaction: discord.Interaction):
        if interaction.channel.id != ROAST_CHANNEL_ID:
            await interaction.response.send_message("❌ This command can only be used in the roast channel.", ephemeral=True)
            return

        is_admin = any(role.id == ADMIN_ROLE_ID for role in interaction.user.roles)
        now = discord.utils.utcnow().timestamp()
        last_used = self.cooldowns.get(interaction.user.id, 0)

        if not is_admin and now - last_used < 3600:
            remaining = int(3600 - (now - last_used))
            await interaction.response.send_message(f"⏳ You can use this again in {remaining // 60}m {remaining % 60}s.", ephemeral=True)
            return

        self.cooldowns[interaction.user.id] = now

        roasts = [
            "Valentine's so useless in the kitchen, even her abuela’s ghost avoids haunting her.",
            "She says she’s a proud Latina, but can’t roll an R to save her sad little life.",
            "If you gave Valentine a molcajete, she’d try to charge it with a USB-C cable.",
            "Valentine swears she’s Mexican, but eats tacos with a fork and knife like it’s a damn salad.",
            "She brings nothing to the carne asada but excuses and recycled Riz.",
            "If laziness were a sport, Valentine would still show up late — in socks and slides.",
            "Valentine calls herself spicy but cries over Valentina Mild.",
            "She’s the only Mexican afraid of the chancla — and still manages to deserve it daily.",
            "Her ancestors didn’t survive La Conquista for her to be this mid.",
            "She says '¡Viva México!' but spells tamarindo with an E.",
            "Even a piñata has more personality than Valentine — and it gets hit on more too.",
            "The only thing she’s committed to is never learning how to make arroz right.",
            "She shows up to Día de los Muertos and still manages to kill the vibe.",
            "She got kicked out of a quinceañera for bringing Sprite… and no manners.",
            "Her fade disappears faster than her motivation.",
            "Valentine talks about cultura but can’t even name 3 states in Mexico.",
            "She thought lotería was just ‘Mexican bingo’ — and still lost.",
            "Even elote vendors cross the street when they see her.",
            "Her singing is so bad, La Virgen turns off the radio herself.",
            "If disrespect was a dish, Valentine would show up and still under-season it.",
            "She’s not ‘La Más Chingona’ — she’s ‘La Más Chafa.’",
            "Her family tree is full of warriors and she’s out here losing fights with tortilla chips.",
            "She says she’s bilingual, but gets nervous ordering at Taco Bell.",
            "Valentine’s so fake, even telenovela villains think she’s doing too much.",
            "If she tried to make tamales, they’d sue.",
            "She looks like she sells candy at school — and still gets caught.",
            "Valentine acts hard but still asks her mom to cut her tortillas.",
            "She flirts like it’s a dare — and still gets curved.",
            "Her drip is from the clearance bin at Ross.",
            "She talks about ‘the culture’ but thinks pozole is a Pokémon.",
            "Valentine’s DMs are emptier than her spice rack.",
            "She thought horchata was an STD.",
            "Even her Snapchat streaks ghosted her.",
            "She’s the type to wear socks at the beach and call it tradition.",
            "Valentine gets roasted more than her mom's chile rellenos.",
            "She shows up late and still asks for leftovers.",
            "Her game is so dry, the desert files copyright claims.",
            "She’s so slow, she gets lapped in Mario Party.",
            "If failure were a telenovela, she’d be the main character.",
            "Valentine got caught simping on BeReal.",
            "She thinks salsa dancing involves chips.",
            "She’s allergic to effort and commitment.",
            "Even Google Maps can’t help her find relevance.",
            "She says she’s humble, but wears chains like a party favor.",
            "Valentine can’t even roast marshmallows without burning the vibe.",
            "She gets tired climbing a flight of DMs.",
            "She fumbled a talking stage with an NPC.",
            "She can’t handle spicy food or spicy women.",
            "She’s been benched more than a soccer ball.",
            "She’s the reason group projects fail.",
            "She thinks reggaeton is a seasoning.",
            "Her voice cracks more than a piñata.",
            "Even WhatsApp blocked her.",
            "Her playlist is just her apologizing.",
            "She still says 'rawr' unironically in 2025.",
            "She uses ‘sent from my iPhone’ to look smart.",
            "She thinks self-love means liking her own Instagram posts.",
            "Valentine got rejected by a Magic 8 Ball.",
            "Her main skill is disappearing when it matters.",
            "She talks about loyalty but can’t commit to a pair of shoes.",
            "She’s so extra, even La Rosa de Guadalupe had to tone it down.",
            "Her riz expired last decade.",
            "Her mom puts 'L' on her lunchbox.",
            "Even bad bitches pray they don’t match with her.",
            "She thinks ‘standing on business’ means doing taxes.",
            "She wears cologne like it’s a personality.",
            "She got ghosted before the convo started.",
            "Valentine is the human version of weak Wi-Fi.",
            "Her haircut is shaped like her career: unfinished.",
            "She watches anime and still gets no character development.",
            "Even her shadow walks ahead of her in shame.",
            "She tries to act mysterious but just comes off unemployed.",
            "If she were a drink, she’d be flat Jarritos.",
            "Valentine’s love language is ‘leaving you on read.’",
            "She thinks an aesthetic is a type of dog.",
            "She blames Mercury retrograde for being irrelevant.",
            "Her version of “healing” is buying new shoes.",
            "Even her NPCs lag out of her games.",
            "She’s built like a failed group chat.",
            "She uses Spanish only when she wants to flirt.",
            "She fakes being deep but can’t swim.",
            "Valentine’s resolution was to get attention — and still failed.",
            "She’s the final boss of disappointment.",
            "She thought 'La Llorona' was a beauty tutorial.",
            "She flexes her GPA like it stands for ‘Guys Passed me Again.’",
            "She uses filters that make her look like another person — then still gets left on delivered.",
            "Even the tortilla press can’t handle her flakiness.",
            "Her vibe is so off, even sage won’t fix it.",
            "She talks about vibes but has the energy of a DMV line.",
            "Valentine thinks she’s mysterious, but she’s just inconsistent.",
            "Her playlists are better than her personality.",
            "She rants about 'fake friends' like they aren’t dodging *her*.",
            "She thinks 'mañana' means 'never.'",
            "She’s the type to take mirror selfies and still crop out the confidence.",
            "If ‘try again later’ were a person, it’d be her."
        ]

        roast = random.choice(roasts)
        await interaction.response.send_message(f"<@496186403638607873> {roast}")

async def setup(bot):
    await bot.add_cog(RoastValentine(bot))
