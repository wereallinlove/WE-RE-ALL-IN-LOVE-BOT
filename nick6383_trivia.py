import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import random

class TriviaView(discord.ui.View):
    def __init__(self, interaction, correct_title, options):
        super().__init__(timeout=60)
        self.correct_title = correct_title
        self.interaction = interaction
        for option in options:
            self.add_item(TriviaButton(option, correct_title, interaction.user))

class TriviaButton(discord.ui.Button):
    def __init__(self, label, correct_title, requester):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.correct_title = correct_title
        self.requester = requester

    async def callback(self, interaction):
        if interaction.user.id != self.requester.id:
            await interaction.response.send_message("This isn't your trivia question.", ephemeral=True)
            return
        for child in self.view.children:
            child.disabled = True
        await interaction.response.edit_message(view=self.view)
        if self.label == self.correct_title:
            result = discord.Embed(title="Correct!", description=f"**{self.correct_title}** was the right answer.", color=discord.Color.green())
        else:
            result = discord.Embed(title="Incorrect!", description=f"The correct answer was **{self.correct_title}**.", color=discord.Color.red())
        await interaction.followup.send(embed=result, ephemeral=True)

trivia_data = [
    {"lyric": "I got it out the dirt like a zombie", "song": "From the dirt"},
    {"lyric": "I throw my money up, I throw my money up", "song": "I JUST BOUGHT A NEW NOSE!"},
    {"lyric": "I'm in the club and all I see is paparazzi", "song": "MAKE ME FAMOUS!"},
    {"lyric": "Slit my wrists and now I'm laughing, Ten racks, got my jeans saggin'", "song": "10k freestyle"},
    {"lyric": "American beauty queen, I got blood all on my jeans", "song": "American beauty"},
    {"lyric": "Take off that makeup, you're still fucking mid", "song": "American psycho"},
    {"lyric": "Slit my neck on Friday, I'm driving on the highway", "song": "Anorexic party"},
    {"lyric": "Can you close the curtains please? Come with me backstage", "song": "backstage"},
    {"lyric": "Beware of dog, I'm in the pound", "song": "beware of the dog"},
    {"lyric": "Shoot me in the heart, turn me to a star", "song": "Carrie white"},
    {"lyric": "Kill myself on my fuckin' birthday", "song": "Birthday song"},
    {"lyric": "Pop a Xan and pop a tag, backstage pass, we in the back", "song": "Bloodt Mary"},
    {"lyric": "You're like a snack, I just wanna eat you", "song": "Cookies are for Santa"},
    {"lyric": "Slit my neck, watch me bleed", "song": "Cut me from the frame"},
    {"lyric": "Pourin' blood up in the blunt, I told Kaleb spark me", "song": "Talk to the hand"},
    {"lyric": "You a goofy, you not bulletproof", "song": "Fuck the fame"},
    {"lyric": "Tie me to the train tracks, yeah, I really love that", "song": "Fuck ur clique"},
    {"lyric": "Be my beauty queen, I'll buy you anything", "song": "Elf on the shelf"},
    {"lyric": "Let's go shopping at the mall, buy everything", "song": "Crying in the club"},
    {"lyric": "Hop outside the limousine in the backseat of the cab", "song": "Bloodt Mary"},
    {"lyric": "I'm sendin' texts, like, are you up tonight?", "song": "love story"},
    {"lyric": "You're not my friend so don't act like it", "song": "haunted house"},
    {"lyric": "I just killed my ex today", "song": "Murder in Hollywood"},
    {"lyric": "I'm lost in the sauce", "song": "true love"},
    {"lyric": "We're moving in slow-mo, like a movie", "song": "Wickerr man"},
]

song_titles = list(set([entry['song'] for entry in trivia_data]))

def setup(bot):
    @bot.tree.command(name="nick6383trivia", description="Guess which song a Nick6383 lyric comes from.")
    async def nick6383trivia(interaction):
        question = random.choice(trivia_data)
        lyric = question['lyric']
        correct = question['song']
        choices = [correct] + random.sample([s for s in song_titles if s != correct], 3)
        random.shuffle(choices)
        embed = discord.Embed(title="Trivia", description=f"*{lyric}*", color=discord.Color.from_rgb(255, 105, 180))
        year = datetime.now().year
        embed.set_footer(text=f"WE'RE ALL IN LOVE {year}")
        view = TriviaView(interaction, correct, choices)
        await interaction.response.send_message(embed=embed, view=view)
