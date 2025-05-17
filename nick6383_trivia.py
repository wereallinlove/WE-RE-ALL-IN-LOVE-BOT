import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import random
import asyncio
import datetime

TRIVIA_CHANNEL_ID = 1373112868249145485
VERIFIED_ROLE_ID = 1371885746415341648
TRIVIA_COOLDOWN = 10
TRIVIA_TIMEOUT = 900  # 15 minutes

SONG_DATA = {
"From the Dirt": [
        "I got it out the dirt like a zombie",
        "I don't need a bitch, I need my mommy",
        "Call me Cobain, bullets in my head",
        "Bae, I like your jeans but what's your size?"
    ],
    "I JUST BOUGHT A NEW NOSE!": [
        "I throw my money up, I throw my money up",
        "Bae, I need a hug right now, I'm crying in the fuckin' club",
        "I feel ugly, so I bought a new nose",
        "VIP, celebrity, kiss me in the limousine"
    ],
    "MAKE ME FAMOUS!": [
        "I'm in the club and all I see is paparazzi",
        "Let's go to the mall, spend it all, we'll buy it all",
        "I know you want me, just drop that fucking bra",
        "I have it made, I'll take you fucking backstage"
    ],
    "10k Freestyle": [
        "Slit my wrists and now I'm laughing, Ten racks, got my jeans saggin'",
        "Die young, get cake, shoutout Lil Jeep",
        "Picture perfect, I'm so worthless, I just wanna fucking cry",
        "I don't have no fuckin' friends because I'm a scary guy"
    ],
    "American Beauty": [
    "I'ma slit my fuckin' neck, chop off my arms",
    "Shoot me with a uzi, I'm covered in Gucci",
    "American beauty queen, I got blood all on my jeans",
    "Rapunzel, let down your long hair"
],
"American Psycho": [
    "Starve myself, I can weigh less",
    "Take off that makeup, you're still fucking mid",
    "I'll be famous when they find out what I did"
],
"Anorexic Party": [
    "Hungry, hungry, I feel so ugly",
    "I like your tank top, when it's see-through",
    "You're big like a seal, hang myself on IG reels"
],
"Backstage": [
    "Can you rip my heart out? Shoot me with the AK",
    "Can you close the curtains please? Come with me backstage",
    "Times Square, New York City, bitch, Can you show me titties, bitch?"
],
"Beware Of The Dog": [
    "Welcome to my fuckin' show, I'm throwin' rocks through your window",
    "I'm that dog, please put me down",
    "We shot up the fuckin' hearse, Then we breakin' in your house"
],
"Bible School": [
    "I got so rich so quick, your welfare check is coming in",
    "My mommy love me, bitches wanna hug me"
],
"Birthday Song": [
    "Kill myself on my fuckin' birthday",
    "On a scary night, bring your nightlight",
    "Put me on the news, now the rumors are true"
],
"Black Amiri Uggs": [
    "808s, Kicks, Claps, Snares",
    "Money, drugs, fame and notoriety",
    "I got no presents on Christmas"
],
"Bloody Mary": [
    "Hop outside the limousine in the backseat of the cab",
    "Pop a Xan and pop a tag, backstage pass, we in the back",
    "I'm posin' for the cameras, why yo' girl a fan of us?",
    "Stomped his ass out, I got blood on my Nikes"
],
"Bury Me Alive": [
    "I'ma slit your throat like Bianca",
    "New designer coat, I'm rockin' Prada",
    "And I don't want that ho, I want my momma"
],
"CAMERAS POINTED AT ME!": [
    "I don't know who you are, or why you stalk me",
    "Let's have sex at the mall, yeah, you turn me on",
    "I just sold my soul for a fuckin' Diet Coke"
],
"Carrie White": [
    "Shoot me in the heart, turn me to a star",
    "You really make me nervous, butterflies",
    "I'm really hangin' from the Christmas tree, put a star on me"
],
"Christmas Lights": [
    "I just wanna take a pic in front of the Christmas lights",
    "And if you finna take pics of me, I'll kill you all tonight"
],
"Christmas Time": [
    "Can we FaceTime?",
    "I love America but I hate liberals",
    "Shoutout WE'RE ALL IN LOVE 'cause that's my fuckin' team"
],
"Christmas Wishlist": [
    "I'm playing you like a game, yeah, it's obvious",
    "Fifteen Xanax, I'm not coming back",
    "She fuck me in the club, She fuck me in my Jordan 1s"
],
"Circus Freak": [
    "You can strangle me, grab me by my neck",
    "I just sold my soul for this shit, I'm getting rich",
    "I'm in the hospital on life support, unplug me"
],
"City Lights": [
    "I'm in Hollywood for my show",
    "You look great when you put on that new Chanel",
    "Like bitch, I'm Nick, it's nice to meet you"
],
"Cookies Are For Santa": [
    "You're like a snack, I just wanna eat you",
    "It's all CGI like a movie",
    "I have a bag full of goodies"
],
"Crying In The Club": [
    "Hit my Motorola phone",
    "You're all I ever wanted, throw me in the garbage",
    "Let's go shopping at the mall, buy everything"
],
"Cut Me From The Frame": [
    "Slit my neck, watch me bleed",
    "Don't hit my phone up, you are dead to me",
    "Let's go to Mickey D's, I really wanna treat you"
],
"Dead Presidents": [
    "Diamonds on my belt, You can't get in Heaven, you can go to Hell",
    "I scream, you scream, we all scream for ice cream",
    "Purple jeans with the tag, put the money in the bag"
],
"Deer In The Headlights": [
    "And bitch, I'm not fucking gay, I don't swing that way",
    "I bought a new nose, it's time for another line"
],
"Demon With A Halo": [
    "Cameras in my face, paparazzi know my name",
    "Shoot me with a fuckin' Uzi, turn me to a smoothie"
],
"Don't HMU #realonesknow": [
    "You gon' catch this fade, yuh, if you didn't know",
    "Yeah, I'ma throw my life away, like I'm Tom Brady"
],
"Don't Touch Me, I'm Expensive": [
    "I fucked your mother, shout out young w6lker"
],
"Elf On The Shelf": [
    "Be my beauty queen, I'll buy you anything",
    "If I pull up to your door, you know I'm not finna knock"
],
"Every Day Is Halloween": [
    "I sold myself to the Devil, Now labels wanna sign me",
    "I was lying in the dirt with the rest of my zombies"
],
"Every Day Is Halloween 2": [
    "She sex me up on Discord",
    "I unfollowed everyone, So everyone get off my dick"
],
"Everything Designer": [
    "Bitch, I'll leave you fuckin' neckless if you talk reckless",
    "Do my dance and evil laugh",
    "I can't fuck with you if you're fat, Gummy bears and fruit snacks"
],
"Faceless": [
    "Greetings and salutations",
    "I'm dead on fuckin' pavement",
    "Kill you and make it look like suicide",
    "Know your place before you get erased"
],
"Fuck The Fame": [
    "You a goofy, you not bulletproof",
    "I'm starving, I don't fuck wit' food",
    "Yeah, we connect like we Bluetooth"
],
"Fuck Ur Clique": [
    "Tie me to the train tracks, yeah, I really love that",
    "WE'RE ALL IN LOVE for life, so it's fuck your clique",
    "Carve my name in your skin if you want me, bitch"
],
"Giving Girls Cocaine": [
    "I'm off fuckin' lean, bitch, just like Lil Wayne",
    "Dirty-pop princess, I'm not into incest",
    "I'm not even into sex"
],
"Hang Me From The Christmas Tree": [
    "What's your Snap? Like, can we keep a streak?"
],
"Hang With Me": [
    "Damn bruh, I just got my fucking bands up, like, who are ya?",
    "Don't talk to me, bitch, talk to the hand",
    "I saw her backstage, she gave me a hug"
],
"Haunted House": [
    "I wanna see you get undressed, get undressed for me, I'm starin' like Paparazzi",
    "You're not my friend so don't act like it"
],
"Hollywood Dreams": [
    "New year, new me, got blood on my jeans, on TV screens",
    "Cameras pointed right at me, I just wanna hear you scream",
    "Be my zombie princess, we can watch the sunset"
],
"IDGAF": [
    "I'm chasin' bags, why you chasin' me?",
    "I cannot eat meat because that's too many calories"
],
"Kick The Cup": [
    "She's a lightskin, you know I like that mix",
    "She said she can feel my dick, it's just my blick",
    "If we're not friends, you can't use my name"
],
"Kms On Xmas": [
    "Xanax for Christmas, Every day I'm flexing",
    "I'm going back to my ex bitch",
    "You're a thot and it shows, You are fat and you're old, I don't fight, I just fold"
],
"Lean": [
    "Catch you like a Pokémon",
    "I love dirty Sprite and I love cough drops",
    "I need my mom"
],
"Love Story": [
    "I'm sendin' texts, like, are you up tonight?"
],
"Masquerade": [
    "Trick or Treat, smell my feet, Give me something good to eat",
    "Who put drugs beneath the Christmas tree? Now I'm crying",
    "Did you know I liked that? 'Cause I really like that"
],
"Merry-Go-Round": [
    "Bury me alive, I just wanna cry",
    "I'm dancin' in puddles, I'm dancing in the fuckin' rain",
    "Cardi B, Ice Spice, will you be my zombie wife?"
],
"Murder In Hollywood": [
    "I just killed my ex today"
],
"Nervous Wreck": [
    "Sick and twisted, my addiction",
    "Put me down like a dog, Kiss me, princess, I'm a frog",
    "I just stole all your shit like I am The Grinch"
],
"No Russian": [
    "I just hit the bank in my Air Force 1's",
    "My cup full of dirt, the mud is what I love",
    "You want dick? Come suck me up"
],
"Ornaments": [
    "New bitch, she brand new, my old bitch, she ran through",
    "Hit you like Chris Brown"
],
"Picture Perfect": [
    "I wanna see you in all black for our wedding",
    "I'm at the slumber party, meeting all her besties",
    "I'm at my funeral and I see confetti",
    "I'm drivin' fast, screaming \"Jesus, take the wheel\""
],
"Prada": [
    "Cookies on my plate, I'm in love with these candy canes",
    "The South Pole is my favorite place",
    "I take shots, I don't fuck with beer"
],
"Put You On": [
    "I don't love you, bitch, I love these fuckin' racks"
],
"Rare Xmas Freestyle": [
    "I'm shooting at the hearse, fuck a funeral",
    "You're acting like a bitch just so you know",
    "I'm like an ornament, I'm even hanging from the tree"
],
"SCARYY PARTYY": [
    "Take you to the moon, yeah, I'll take you to the stars",
    "I'm an ugly vamp flexed up in the moonlight"
],
"Shooting Star": [
    "You can hit my juul like we are in school",
    "I'm feeling up her skirt, it's like a tsunami"
],
"Take A Picture, It'll Last Longer": [
    "Ugly zombie, I'm just chasing cash",
    "I just wanted to see the Christmas lights"
],
"Talk To The Hand": [
    "Pourin' blood up in the blunt, I told Kaleb spark me",
    "Candy corn all on me, dirty-pop army"
],
"True Love": [
    "I'm lost in the sauce",
    "Shit's about to get political, We are shooting at the liberals"
],
"Ugly & Glamorous": [
    "Tattooed in the club, what is going on right now?",
    "Drop that bra and show some tits",
    "You can't get a feat. because you're trash"
],
"Undead Bride": [
    "I'm dancing like a ballerina",
    "I got two sticks and it's like I'm playing hockey",
    "It's an act, I don't know how to feel"
],
"Welcome To My Show": [
    "I Just slit my fuckin' neck, got blood all on my clothes",
    "Dancin' with a kitchen knife, kiss me under Christmas lights",
    "I'm real Prada gothic, if you're on it then I'm on it, bitch",
    "I'ma piss on your tombstone, WE'RE ALL IN LOVE, we do the most"
],
"White Girl Wednesday": [
    "Woah, this is how the beat goes",
    "I'm a sketchy guy, you might lose your fuckin' life"
],
"Wicked Witch": [
    "Stick to the script, Before I end my life, I need to get rich",
    "I'm acting like a hooligan, I'm off the rails again",
    "You can eat my heart, eat it with a fork",
    "Is that my ex? If she call, I press ignore"
],
"Xanax Underneath The Christmas Tree": [
    "I really woke up, pissed off, You could really die tonight, like King Von",
    "You could really pull up, I got that shit on me"
],
"Wickerr Man": [
    "We're moving in slow-mo, like a movie",
    "Please don't try to make me mad, I just made my old bitch sad"
],
}

used_recently = set()
active_trivia = {}

class TriviaView(View):
    def __init__(self, correct_title, user_id):
        super().__init__(timeout=TRIVIA_TIMEOUT)
        self.correct = correct_title
        self.user_id = user_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id

    async def on_timeout(self):
        if self.message:
            await self.message.reply(f"<@{self.user_id}> your trivia request expired. Please start a new one.")
            active_trivia.pop(self.user_id, None)

    @discord.ui.button(label="Option A", style=discord.ButtonStyle.gray)
    async def a(self, interaction, button): await self.check_answer(interaction, button.label)

    @discord.ui.button(label="Option B", style=discord.ButtonStyle.gray)
    async def b(self, interaction, button): await self.check_answer(interaction, button.label)

    @discord.ui.button(label="Option C", style=discord.ButtonStyle.gray)
    async def c(self, interaction, button): await self.check_answer(interaction, button.label)

    @discord.ui.button(label="Option D", style=discord.ButtonStyle.gray)
    async def d(self, interaction, button): await self.check_answer(interaction, button.label)

    async def check_answer(self, interaction, choice):
        active_trivia.pop(self.user_id, None)
        used_recently.add(self.user_id)
        await asyncio.sleep(TRIVIA_COOLDOWN)
        used_recently.discard(self.user_id)

        if choice == self.correct:
            embed = discord.Embed(title="✅ Correct!", description=f"You chose **{choice}**.\n\nYou got it right!", color=0x2ecc71)
        else:
            embed = discord.Embed(title="❌ Incorrect.", description=f"You chose **{choice}**.\n\nIncorrect. The correct answer was **{self.correct}**.", color=0xe74c3c)
        await interaction.response.send_message(embed=embed)
        self.stop()

class NickTrivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="nick6383trivia", description="Guess which Nick6383 song the lyric is from")
    async def nick6383trivia(self, interaction: discord.Interaction):
        if interaction.channel.id != TRIVIA_CHANNEL_ID:
            return
        if VERIFIED_ROLE_ID not in [role.id for role in interaction.user.roles]:
            return
        if interaction.user.id in used_recently:
            await interaction.response.send_message("Please wait before using this command again.")
            return
        if interaction.user.id in active_trivia:
            await interaction.response.send_message("You already have a trivia question active!")
            return

        song_title = random.choice(list(SONG_DATA.keys()))
        lyric = random.choice(SONG_DATA[song_title])

        other_titles = list(SONG_DATA.keys())
        other_titles.remove(song_title)
        options = random.sample(other_titles, 3) + [song_title]
        random.shuffle(options)

        embed = discord.Embed(title=f"Trivia for {interaction.user.display_name}", description=f"*{lyric}*", color=0xff69b4)
        file = discord.File("nick6383.jpg", filename="nick6383.jpg")
        embed.set_image(url="attachment://nick6383.jpg")

        view = TriviaView(song_title, interaction.user.id)
        view.children[0].label = options[0]
        view.children[1].label = options[1]
        view.children[2].label = options[2]
        view.children[3].label = options[3]

        msg = await interaction.channel.send(embed=embed, file=file, view=view)
        view.message = msg
        active_trivia[interaction.user.id] = msg

async def setup(bot):
    await bot.add_cog(NickTrivia(bot))
