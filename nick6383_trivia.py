import discord
from discord import app_commands
from discord.ext import commands
import random

class Nick6383Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trivia_data = [
{
        "lyric": "I got it out the dirt like a zombie",
        "answer": "From The Dirt"
    },
{
        "lyric": "I throw my money up, I throw my money up",
        "answer": "I JUST BOUGHT A NEW NOSE!"
    },
{
        "lyric": "I'm in the club and all I see is paparazzi",
        "answer": "MAKE ME FAMOUS!"
    },
{
        "lyric": "Slit my wrists and now I'm laughing, Ten racks, got my jeans saggin'",
        "answer": "10k Freestyle"
    },
{
        "lyric": "I'ma slit my fuckin' neck, chop off my arms",
        "answer": "American Beauty"
    },
{
        "lyric": "Starve myself, I can weigh less",
        "answer": "American Psycho"
    },
{
        "lyric": "Hungry, hungry, I feel so ugly",
        "answer": "Anorexic Party"
    },
{
        "lyric": "Can you rip my heart out? Shoot me with the AK",
        "answer": "Backstage"
    },
{
        "lyric": "Welcome to my fuckin' show, I'm throwin' rocks through your window",
        "answer": "Beware of the Dog"
    },
{
        "lyric": "I got so rich so quick, your welfare check is coming in",
        "answer": "Bible School"
    },
{
    "lyric": "I'm posing for the cameras, why your girl a fan of us?",
    "answer": "Bloody Mary"
},
{
    "lyric": "Kill myself on my fuckin' birthday.",
    "answer": "Birthday Song"
},
{
    "lyric": "I'm at the pumpkin patch — where's Punkin at?",
    "answer": "Bloody Mary"
},
{
    "lyric": "I'ma slit your throat like Bianca.",
    "answer": "Bury Me Alive"
},
{
    "lyric": "Trick or treat, smell my feet, gimme all your candy.",
    "answer": "CAMERAS POINTED AT ME!"
},
{
    "lyric": "Shoot me in the heart, turn me to a star.",
    "answer": "Carrie White"
},
{
    "lyric": "I just wanna take a pic in front of the Christmas lights.",
    "answer": "Christmas Lights"
},
{
    "lyric": "Can we FaceTime?",
    "answer": "Christmas Time"
},
{
    "lyric": "I'm playing you like a game — yeah, it's obvious.",
    "answer": "Christmas Wishlist"
},
{
    "lyric": "I just sold my soul for this shit — I'm getting rich.",
    "answer": "Circus Freak"
},
{
    "lyric": "You're all I ever wanted, throw me in the garbage.",
    "answer": "Crying in the Club"
},
{
    "lyric": "Slit my neck, watch me bleed.",
    "answer": "Cut Me from the Frame"
},
{
    "lyric": "I scream, you scream, we all scream for ice cream.",
    "answer": "Dead Presidents"
},
{
    "lyric": "I bought a new nose — it's time for another line.",
    "answer": "Deer in the Headlights"
},
{
    "lyric": "Shoot me with a fuckin' Uzi, turn me to a smoothie.",
    "answer": "Demon with a Halo"
},
{
    "lyric": "I will be your Ken, you're my Barbie.",
    "answer": "Don't HMU #realonesknow"
},
{
    "lyric": "If I pull up to your door, you know I'm not finna knock.",
    "answer": "Elf on the Shelf"
},
{
    "lyric": "I was lying in the dirt with the rest of my zombies.",
    "answer": "Every Day Is Halloween"
},
{
    "lyric": "She sexed me up on Discord.",
    "answer": "Every Day Is Halloween 2"
},
{
    "lyric": "Do my dance and evil laugh.",
    "answer": "Everything Designer"
},
{
    "lyric": "Slit my wrists, suicide — married to my zombie wife.",
    "answer": "Welcome to My Show"
},
{
    "lyric": "Be my zombie princess, we can watch the sunset.",
    "answer": "Hollywood Dreams"
},
{
    "lyric": "I got cuts on my body, I'm a fuckin' zombie.",
    "answer": "IDGAF"
},
{
    "lyric": "She said she can feel my dick — it's just my blick.",
    "answer": "Kick the Cup"
},
{
    "lyric": "You're a thot and it shows, you are fat and you're old.",
    "answer": "Kms on Xmas"
},
{
    "lyric": "I love dirty Sprite and I love cough drops.",
    "answer": "lean"
},
{
    "lyric": "I'm sendin' texts, like, are you up tonight?",
    "answer": "Love Story"
},
{
    "lyric": "Did you know I liked that? 'Cause I really like that.",
    "answer": "Masquerade"
},
{
    "lyric": "Like a fuckin' dog? I'm a motherfuckin' hound.",
    "answer": "Merry Go Round"
},
{
    "lyric": "I just killed my ex today.",
    "answer": "Murder in Hollywood"
},
{
    "lyric": "Put me down like a dog — kiss me, princess, I'm a frog.",
    "answer": "Nervous Wreck"
},
{
    "lyric": "Shut the fuck up — suck my fuckin' nuts.",
    "answer": "No Russian"
},
{
    "lyric": "Hit you like Chris Brown.",
    "answer": "Ornaments"
},
{
    "lyric": "I'm at my funeral and I see confetti.",
    "answer": "Picture Perfect"
},
{
    "lyric": "Cookies on my plate, I'm in love with these candy canes.",
    "answer": "Prada"
},
{
    "lyric": "I don't love you, bitch — I love these fuckin' racks.",
    "answer": "Put You On"
},
{
    "lyric": "I'm posted at McDonald's lookin' for Grimace.",
    "answer": "Rare Xmas Freestyle"
},
{
    "lyric": "I'm an ugly vamp flexed up in the moonlight.",
    "answer": "SCARYY PARTYY"
},
{
    "lyric": "I'm shooting at the hearse — a hundred for a verse.",
    "answer": "Shooting Star"
},
{
    "lyric": "I just wanted to see the Christmas lights.",
    "answer": "Take a Picture, It'll Last Longer"
},
{
    "lyric": "Candy corn all on me, dirty-pop army.",
    "answer": "Talk to the Hand"
},
{
    "lyric": "Shit's about to get political — we are shooting at the liberals.",
    "answer": "True Love"
},
{
    "lyric": "Tattooed in the club — what is going on right now?",
    "answer": "Ugly & Glamorous"
},
{
    "lyric": "I'm all dolled up, I don't give a fuck.",
    "answer": "Undead Bride"
},
{
    "lyric": "I just slit my fuckin' neck, got blood all on my clothes.",
    "answer": "Welcome to My Show"
},
{
    "lyric": "I'm a sketchy guy, you might lose your fuckin' life.",
    "answer": "White Girl Wednesday"
},
{
    "lyric": "Stick to the script — before I end my life, I need to get rich.",
    "answer": "Wicked Witch"
},
{
    "lyric": "You could really die tonight, like King Von.",
    "answer": "Xanax Underneath the Christmas Tree"
},
{
    "lyric": "We're moving in slow-mo, like a movie.",
    "answer": "Wickerr Man"
},
{
    "lyric": "I'm flexing hard, I'll never stop.",
    "answer": "Black Amiri Uggs"
},
{
    "lyric": "Dead opps on the floor at the cemetery.",
    "answer": "Birthday Song"
},
{
    "lyric": "I got bloody racks on me, I'm off dirty drugs.",
    "answer": "Bloody Mary"
},
{
    "lyric": "She wanna fuck a thug — shout out my day ones.",
    "answer": "Christmas Wishlist"
},
{
    "lyric": "Put me in the dirt — I'm dancing with all of the worms.",
    "answer": "Bloody Mary"
},
{
    "lyric": "Drop racks on those titties, bitch — your shit look so mini, bitch.",
    "answer": "Backstage"
},
{
    "lyric": "You're acting like a bitch, just so you know.",
    "answer": "Rare Xmas Freestyle"
},
{
    "lyric": "Let's go shopping at the mall — buy everything.",
    "answer": "Crying in the Club"
},
{
    "lyric": "Yeah, I'm barking like a dog — yeah, beware.",
    "answer": "American Beauty"
},
{
    "lyric": "I don't need a bitch, I need my mommy.",
    "answer": "From The Dirt"
},
{
    "lyric": "Call me Cobain, bullets in my head.",
    "answer": "From The Dirt"
},
{
    "lyric": "Bae, I like your jeans but what's your size?",
    "answer": "From The Dirt"
},
{
    "lyric": "Bae, I need a hug right now, I'm crying in the fuckin' club.",
    "answer": "I Just Bought A New Nose!"
},
{
    "lyric": "I feel ugly, so I bought a new nose.",
    "answer": "I Just Bought A New Nose!"
},
{
    "lyric": "VIP, celebrity, kiss me in the limousine.",
    "answer": "I Just Bought A New Nose!"
},
{
    "lyric": "I'm so H-O-T on MTV.",
    "answer": "I Just Bought A New Nose!"
},
{
    "lyric": "She's in Abercrombie, be my paparazzi.",
    "answer": "I Just Bought A New Nose!"
},
{
    "lyric": "I unfollowed everyone because I don't give a fuck.",
    "answer": "I Just Bought A New Nose!"
},
{
    "lyric": "Party like it's 2012, I got Bacardi in my cup.",
    "answer": "I Just Bought A New Nose!"
},
{
    "lyric": "Let's go to the mall, spend it all, we'll buy it all.",
    "answer": "Make Me Famous!"
},
{
    "lyric": "I know you want me, just drop that fucking bra.",
    "answer": "Make Me Famous!"
},
{
    "lyric": "I have it made, I'll take you fucking backstage.",
    "answer": "Make Me Famous!"
},
{
    "lyric": "I feel like Punkinloveee but right now I'm the only one.",
    "answer": "Make Me Famous!"
},
{
    "lyric": "Just lose your pants, bitch, I wanna dance, bitch.",
    "answer": "Make Me Famous!"
},
{
    "lyric": "No regrets bitch, let's get drunk at the outlets.",
    "answer": "Make Me Famous!"
},
{
    "lyric": "Disney star, yeah, I just got signed, bruh.",
    "answer": "Make Me Famous!"
},
{
    "lyric": "O-M-G, O-M-G, I'm in love with that band tee.",
    "answer": "Make Me Famous!"
},
{
    "lyric": "Omg, Z.B.C. hate me.",
    "answer": "Make Me Famous!"
},
{
    "lyric": "H-O-fuckin'-T, I'm in the limousine.",
    "answer": "Make Me Famous!"
},
{
    "lyric": "Get away from me, get that opp away from me.",
    "answer": "Make Me Famous!"
},
{
    "lyric": "Die young, get cake, shoutout Lil Jeep.",
    "answer": "10K Freestyle"
},
{
    "lyric": "Picture perfect, I'm so worthless, I just wanna fucking cry.",
    "answer": "10K Freestyle"
},
{
    "lyric": "I don't have no fuckin' friends because I'm a scary guy.",
    "answer": "10K Freestyle"
},
{
    "lyric": "Piss on your tombstone, yeah, you can get buried alive.",
    "answer": "10K Freestyle"
},
{
    "lyric": "I'ma fuck your skeleton, you can be my zombie wife.",
    "answer": "10K Freestyle"
},
{
    "lyric": "Kiss me in the moonlight 'cause I'm motherfucking lit.",
    "answer": "10K Freestyle"
},
{
    "lyric": "Every day is Halloween, like a pumpkin, bitch, I'm lit.",
    "answer": "10K Freestyle"
},
{
    "lyric": "She got cuts all on her thighs, I got slits all on my wrists.",
    "answer": "10K Freestyle"
},
{
    "lyric": "I got diamonds on my face, she got lipstick on my dick.",
    "answer": "10K Freestyle"
},
{
    "lyric": "Pull up to the party, everybody getting shot.",
    "answer": "10K Freestyle"
},
{
    "lyric": "They tryna act like we're all in love, but you are not.",
    "answer": "10K Freestyle"
},
{
    "lyric": "Shoot me with a Uzi, I'm covered in Gucci.",
    "answer": "American Beauty"
},
{
    "lyric": "American beauty queen, I got blood all on my jeans.",
    "answer": "American Beauty"
},
{
    "lyric": "I got racks all on me, she's a broken Barbie.",
    "answer": "American Beauty"
},
{
    "lyric": "My bitch is a model, I feel fuckin' awful, sippin' out the bottle.",
    "answer": "American Beauty"
},
{
    "lyric": "Rapunzel, let down your long hair.",
    "answer": "American Beauty"
},
{
    "lyric": "I know that life is beautiful but it's not fair.",
    "answer": "American Beauty"
},
{
    "lyric": "Yeah, I'm a Jesus freak, so let's say a prayer.",
    "answer": "American Beauty"
},
{
    "lyric": "Take off that makeup, you're still fucking mid.",
    "answer": "American Psycho"
},
{
    "lyric": "I think she hate me but she still gon' let me hit.",
    "answer": "American Psycho"
},
{
    "lyric": "I'll be famous when they find out what I did.",
    "answer": "American Psycho"
},
{
    "lyric": "Yeah, bad bitch on my right, bad bitch on my left.",
    "answer": "Anorexic Party"
},
{
    "lyric": "I can't be with you, you're ugly and you get around.",
    "answer": "Anorexic Party"
},
{
    "lyric": "I like your tank top, when it's see-through.",
    "answer": "Anorexic Party"
},
{
    "lyric": "Slit my neck on Friday, I'm driving on the highway.",
    "answer": "Anorexic Party"
},
{
    "lyric": "Like Jesus, take the wheel, I take pics on BeReal.",
    "answer": "Anorexic Party"
},
{
    "lyric": "You're big like a seal, hang myself on IG reels.",
    "answer": "Anorexic Party"
},
{
    "lyric": "We should break up, I think that we should just be friends.",
    "answer": "Anorexic Party"
},
{
    "lyric": "She just tryna turn up, I'm just tryna get laid.",
    "answer": "Backstage"
},
{
    "lyric": "I'm only afraid of God, every day I fucking pray.",
    "answer": "Backstage"
},
{
    "lyric": "Can you close the curtains please? Come with me backstage.",
    "answer": "Backstage"
},
{
    "lyric": "We're all in love, we look so hot, hot, hot, hot.",
    "answer": "Backstage"
},
{
    "lyric": "Can you get off of my cock, cock, cock, cock?",
    "answer": "Backstage"
},
{
    "lyric": "Times Square, New York City, bitch, can you show me titties, bitch?",
    "answer": "Backstage"
},
{
    "lyric": "Dirty pop wedding ring, I can buy you anything.",
    "answer": "Backstage"
},
{
    "lyric": "Beware of dog, I'm in the pound.",
    "answer": "Beware Of The Dog"
},
{
    "lyric": "I'm that dog, please put me down.",
    "answer": "Beware Of The Dog"
},
{
    "lyric": "I got it out the fuckin' dirt, climbing out the fuckin' ground.",
    "answer": "Beware Of The Dog"
},
{
    "lyric": "We shot up the fuckin' hearse, then we breakin' in your house.",
    "answer": "Beware Of The Dog"
},
{
    "lyric": "We're all in love in the club, we got no love.",
    "answer": "Beware Of The Dog"
},
{
    "lyric": "They was laughin' at my homie, so we shot it up.",
    "answer": "Beware Of The Dog"
},
{
    "lyric": "@noosetied, @wereallinlove, you can follow us.",
    "answer": "Beware Of The Dog"
},
{
    "lyric": "Double D's in my face, fuck your A cups.",
    "answer": "Beware Of The Dog"
},
{
    "lyric": "Jesus freak, I rock my piece and I won't ever sin.",
    "answer": "Bible School"
},
{
    "lyric": "My mommy love me, bitches wanna hug me.",
    "answer": "Bible School"
},
{
    "lyric": "There's blow up in my nose, I'm sniffin' fuckin' snow globes.",
    "answer": "Bible School"
},
{
    "lyric": "I'm turnt up at church on a Sunday.",
    "answer": "Birthday Song"
},
{
    "lyric": "I'ma slit my neck on the runway.",
    "answer": "Birthday Song"
},
{
    "lyric": "All up in my pack, all up in my blunt.",
    "answer": "Birthday Song"
},
{
    "lyric": "Like, dap me up, cuh, what is up?",
    "answer": "Birthday Song"
},
{
    "lyric": "Strippers give me hugs, yeah, I'm throwing up my ones.",
    "answer": "Birthday Song"
},
{
    "lyric": "She's a slut, so I'm finna show her love.",
    "answer": "Birthday Song"
},
{
    "lyric": "If you got a problem, bitch, tell me where you at.",
    "answer": "Birthday Song"
},
{
    "lyric": "On a scary night, bring your nightlight.",
    "answer": "Birthday Song"
},
{
    "lyric": "Put me on the news, now the rumors are true.",
    "answer": "Birthday Song"
},
{
    "lyric": "808s, kicks, claps, snares.",
    "answer": "Black Amiri Uggs"
},
{
    "lyric": "Money, drugs, fame and notoriety.",
    "answer": "Black Amiri Uggs"
},
{
    "lyric": "Hug and kiss on me like I'm pretty.",
    "answer": "Black Amiri Uggs"
},
{
    "lyric": "I bought a nose, I need rhinoplasty.",
    "answer": "Black Amiri Uggs"
},
{
    "lyric": "Six ninety on my shoes, what do I have to lose?",
    "answer": "Black Amiri Uggs"
},
{
    "lyric": "I got no presents on Christmas.",
    "answer": "Black Amiri Uggs"
},
{
    "lyric": "Let's hit the bar, they don't card.",
    "answer": "Black Amiri Uggs"
},
{
    "lyric": "Hop outside the limousine in the backseat of the cab.",
    "answer": "Bloody Mary"
},
{
    "lyric": "I'm off lean and fuckin' weed, spend some racks and make it back.",
    "answer": "Bloody Mary"
},
{
    "lyric": "Pop a Xan and pop a tag, backstage pass, we in the back.",
    "answer": "Bloody Mary"
},
{
    "lyric": "They sleep on me, why they nap?",
    "answer": "Bloody Mary"
},
{
    "lyric": "I'm fucked up on lots of drugs, I'm fucked up inside the club.",
    "answer": "Bloody Mary"
},
{
    "lyric": "I'm swimmin' with the fishies, I got bitches fuckin' with me.",
    "answer": "Bloody Mary"
},
{
    "lyric": "Steal your chain and it's a wrap.",
    "answer": "Bloody Mary"
},
{
    "lyric": "I don't fuck with candy corn, put me in a fuckin' porn.",
    "answer": "Bloody Mary"
},
{
    "lyric": "Pop a Xan and fall asleep, honestly, we're meant to.",
    "answer": "Bloody Mary"
},
{
    "lyric": "Thirty racks all on my jeans, I'm off the lean inside the jeep.",
    "answer": "Bloody Racks"
},
{
    "lyric": "Hop out the limousine, free Britney, I'm off Xanax like it's 2017.",
    "answer": "Bloody Racks"
},
{
    "lyric": "Post about me on your story, bitch, I don't give a fuck.",
    "answer": "Bloody Racks"
},
{
    "lyric": "Stomped his ass out, I got blood on my Nikes.",
    "answer": "Bloody Racks"
},
{
    "lyric": "Why they gay? Why they on my dick?",
    "answer": "Bloody Racks"
},
{
    "lyric": "I'm saggin' my jeans like some ghetto white trash.",
    "answer": "Bloody Racks"
},
{
    "lyric": "New designer coat, I'm rockin' Prada.",
    "answer": "Bury Me Alive"
},
{
    "lyric": "And I don't want that ho, I want my momma.",
    "answer": "Bury Me Alive"
},
{
    "lyric": "I don't know who you are, or why you stalk me.",
    "answer": "Cameras Pointed At Me!"
},
{
    "lyric": "Let's have sex at the mall, yeah, you turn me on.",
    "answer": "Cameras Pointed At Me!"
},
{
    "lyric": "I'm in the club with Copi, they wanna see my neck bleed.",
    "answer": "Cameras Pointed At Me!"
},
{
    "lyric": "Every day is Halloween, Jack-o'-lanterns on me.",
    "answer": "Cameras Pointed At Me!"
},
{
    "lyric": "I just sold my soul for a fuckin' Diet Coke.",
    "answer": "Cameras Pointed At Me!"
},
{
    "lyric": "Let's go to Disneyland, let's go to the park.",
    "answer": "Carrie White"
},
{
    "lyric": "No security, I pull up with my gun.",
    "answer": "Carrie White"
},
{
    "lyric": "Why you tryna play me like a puppet?",
    "answer": "Carrie White"
},
{
    "lyric": "You really make me nervous — butterflies.",
    "answer": "Carrie White"
},
{
    "lyric": "I really wanna hold you 'til you die.",
    "answer": "Carrie White"
},
{
    "lyric": "New Chanel with the pink Burberry.",
    "answer": "Carrie White"
},
{
    "lyric": "Fuck me in your wedding dress, marry me.",
    "answer": "Carrie White"
},
{
    "lyric": "I'm really hangin' from the Christmas tree, put a star on me.",
    "answer": "Carrie White"
},
{
    "lyric": "And if you finna take pics of me, I'll kill you all tonight.",
    "answer": "Christmas Lights"
},
{
    "lyric": "You make me fucking sick, you make me wanna die.",
    "answer": "Christmas Lights"
},
{
    "lyric": "L7 on the beat, hear the bells chime.",
    "answer": "Christmas Time"
},
{
    "lyric": "They think they know me, I think that's federal.",
    "answer": "Christmas Time"
},
{
    "lyric": "I love America but I hate liberals.",
    "answer": "Christmas Time"
},
{
    "lyric": "I got hella hoes and they twerkin' on me.",
    "answer": "Christmas Time"
},
{
    "lyric": "Shoutout We're All In Love, 'cause that's my fuckin' team.",
    "answer": "Christmas Time"
},
{
    "lyric": "So grateful for my fans, 'cause they all love me.",
    "answer": "Christmas Time"
},
{
    "lyric": "I got a carrot on my nose like a snowman.",
    "answer": "Christmas Wishlist"
},
{
    "lyric": "That bitch a ten when she has on her makeup.",
    "answer": "Christmas Wishlist"
},
{
    "lyric": "Fifteen Xanax, I'm not coming back.",
    "answer": "Christmas Wishlist"
},
{
    "lyric": "Bitch, I got the strap in my mo'fuckin' backpack.",
    "answer": "Christmas Wishlist"
},
{
    "lyric": "You can hit my Cash App, you can't get a follow back.",
    "answer": "Christmas Wishlist"
},
{
    "lyric": "You're ugly and you're fucking fat.",
    "answer": "Christmas Wishlist"
},
{
    "lyric": "She fuck me in the club, she fuck me in my Jordan 1s.",
    "answer": "Christmas Wishlist"
},
{
    "lyric": "I can feel my heart beating out my chest.",
    "answer": "Circus Freak"
},
{
    "lyric": "You can strangle me, grab me by my neck.",
    "answer": "Circus Freak"
},
{
    "lyric": "I'm a Jesus freak, I'm stressed and I'm blessed.",
    "answer": "Circus Freak"
},
{
    "lyric": "I love checks, I love bread — you're an opp, you're a fed.",
    "answer": "Circus Freak"
},
{
    "lyric": "You're a bop, leave you on read.",
    "answer": "Circus Freak"
},
{
    "lyric": "I'm getting too old for this shit, let's make a wish.",
    "answer": "Circus Freak"
},
{
    "lyric": "I'm getting too bold in this bitch, let's take some flicks.",
    "answer": "Circus Freak"
},
{
    "lyric": "Cuddle me like a bunny.",
    "answer": "Circus Freak"
},
{
    "lyric": "I just popped a thousand Xanax, I feel ugly.",
    "answer": "Circus Freak"
},
{
    "lyric": "I'm in the hospital on life support — unplug me.",
    "answer": "Circus Freak"
},
{
    "lyric": "I'm in Hollywood for my show.",
    "answer": "City Lights"
},
{
    "lyric": "You look great when you put on that new Chanel.",
    "answer": "City Lights"
},
{
    "lyric": "You can't get close to me, we not personal.",
    "answer": "City Lights"
},
{
    "lyric": "You can't be with me — you're ugly and you're fucking fat.",
    "answer": "City Lights"
},
{
    "lyric": "Like, bitch, I'm Nick, it's nice to meet you.",
    "answer": "City Lights"
},
{
    "lyric": "They on my dick, like, what the fuck is new?",
    "answer": "City Lights"
},
{
    "lyric": "You're like a snack, I just wanna eat you.",
    "answer": "Cookies Are For Santa"
},
{
    "lyric": "I looked inside the mirror, I saw a monster.",
    "answer": "Cookies Are For Santa"
},
{
    "lyric": "It's all a lie just like April Fools.",
    "answer": "Cookies Are For Santa"
},
{
    "lyric": "It's all CGI like a movie.",
    "answer": "Cookies Are For Santa"
},
{
    "lyric": "I have a bag full of goodies.",
    "answer": "Cookies Are For Santa"
},
{
    "lyric": "Hit my Motorola phone.",
    "answer": "Crying In The Club"
},
{
    "lyric": "There's a dance tonight, baby, if you wanna go.",
    "answer": "Crying In The Club"
},
{
    "lyric": "I'm sorry that I care, I'm sorry that you never did.",
    "answer": "Crying In The Club"
},
{
    "lyric": "Let's go to shopping at the mall, buy everything.",
    "answer": "Crying In The Club"
},
{
    "lyric": "Don't hit my phone up — you are dead to me.",
    "answer": "Cut Me From The Frame"
},
{
    "lyric": "Let's go to Mickey D's, I really wanna treat you.",
    "answer": "Cut Me From The Frame"
},
{
    "lyric": "Diamonds on my belt — you can't get in Heaven, you can go to Hell.",
    "answer": "Dead Presidents"
},
{
    "lyric": "Chop my fuckin' head off like the Cartel.",
    "answer": "Dead Presidents"
},
{
    "lyric": "Walk around with a Glock in the hotel.",
    "answer": "Dead Presidents"
},
{
    "lyric": "Abercrombie fuckin' Fitch — your bitch is a fuckin' six.",
    "answer": "Dead Presidents"
},
{
    "lyric": "Red dot, green beams — be my scream queen.",
    "answer": "Dead Presidents"
},
{
    "lyric": "Dirty-pop army, I'm a fuckin' zombie.",
    "answer": "Dead Presidents"
},
{
    "lyric": "Death and glitter, I'm a sinner — @wereallinlove, bitch, on Twitter.",
    "answer": "Dead Presidents"
},
{
    "lyric": "Santa gave me fuckin' coal — that's not fuckin' cool.",
    "answer": "Dead Presidents"
},
{
    "lyric": "In the backseat of the cab, I jumped out the fuckin' cab.",
    "answer": "Dead Presidents"
},
{
    "lyric": "Scream 3, stab me — I'm so hungry.",
    "answer": "Dead Presidents"
},
{
    "lyric": "Purple jeans with the tag, put the money in the bag.",
    "answer": "Dead Presidents"
},
{
    "lyric": "Revenge X tee, I'm off Creatine.",
    "answer": "Dead Presidents"
},
{
    "lyric": "I swear I'm in a movie — American Beauty.",
    "answer": "Dead Presidents"
},
{
    "lyric": "Kill cheerleaders, fuck my teachers.",
    "answer": "Dead Presidents"
},
{
    "lyric": "Like a skeleton, I'm anorexic.",
    "answer": "Dead Presidents"
},
{
    "lyric": "I'm eatin' flesh, bitch, and I love it.",
    "answer": "Dead Presidents"
},
{
    "lyric": "George Washington, I'm a money fiend.",
    "answer": "Dead Presidents"
},
{
    "lyric": "And bitch, I'm not fuckin' gay — I don't swing that way.",
    "answer": "Deer In The Headlights"
},
{
    "lyric": "Cameras in my face, paparazzi know my name.",
    "answer": "Demon With A Halo"
},
{
    "lyric": "You gon' catch this fade, yuh, if you didn't know.",
    "answer": "Don't HMU #RealOnesKnow"
},
{
    "lyric": "I been on some new shit, you been on some old shit.",
    "answer": "Don't HMU #RealOnesKnow"
},
{
    "lyric": "Yeah, I'ma throw my life away like I'm Tom Brady.",
    "answer": "Don't HMU #RealOnesKnow"
},
{
    "lyric": "I fucked your mother — shout out young W6lker.",
    "answer": "Don't Touch Me, I'm Expensive"
},
{
    "lyric": "Be my beauty queen, I'll buy you anything.",
    "answer": "Elf On The Shelf"
},
{
    "lyric": "She wanna link but I don't know where she been.",
    "answer": "Elf On The Shelf"
},
{
    "lyric": "On Sunday, I'm not a sinner.",
    "answer": "Elf On The Shelf"
},
{
    "lyric": "I rap, I'm not a singer.",
    "answer": "Elf On The Shelf"
},
{
    "lyric": "I sold myself to the Devil — now labels wanna sign me.",
    "answer": "Every Day Is Halloween"
},
{
    "lyric": "Your boyfriend is so wack.",
    "answer": "Every Day Is Halloween 2"
},
{
    "lyric": "Bitch, I'll leave you fuckin' neckless if you talk reckless.",
    "answer": "Everything Designer"
},
{
    "lyric": "I can't fuck with you if you're fat — gummy bears and fruit snacks.",
    "answer": "Everything Designer"
},
{
    "lyric": "Greetings and salutations.",
    "answer": "Faceless"
},
{
    "lyric": "I'm dead on fuckin' pavement.",
    "answer": "Faceless"
},
{
    "lyric": "Kill you and make it look like suicide.",
    "answer": "Faceless"
},
{
    "lyric": "Know your place before you get erased.",
    "answer": "Faceless"
},
{
    "lyric": "You a goofy — you not bulletproof.",
    "answer": "Fuck The Fame"
},
{
    "lyric": "I'm starving, I don't fuck wit' food.",
    "answer": "Fuck The Fame"
},
{
    "lyric": "Yeah, we connect like we Bluetooth.",
    "answer": "Fuck The Fame"
},
{
    "lyric": "Tie me to the train tracks, yeah, I really love that.",
    "answer": "Fuck Ur Clique"
},
{
    "lyric": "I'm rappin' like I'm Lone or Diamondsonmydick.",
    "answer": "Fuck Ur Clique"
},
{
    "lyric": "We're All In Love for life, so it's fuck your clique.",
    "answer": "Fuck Ur Clique"
},
{
    "lyric": "Carve my name in your skin if you want me, bitch.",
    "answer": "Fuck Ur Clique"
},
{
    "lyric": "I'm off fuckin' lean, bitch, just like Lil Wayne.",
    "answer": "Giving Girls Cocaine"
},
{
    "lyric": "I love America, I'ma rip your face off.",
    "answer": "Giving Girls Cocaine"
},
{
    "lyric": "Dirty-pop princess, I'm not into incest.",
    "answer": "Giving Girls Cocaine"
},
{
    "lyric": "I'm not even into sex.",
    "answer": "Giving Girls Cocaine"
},
{
    "lyric": "What's your Snap? Like, can we keep a streak?",
    "answer": "Hang Me From The Christmas Tree"
},
{
    "lyric": "Damn bruh, I just got my fucking bands up — like, who are ya?",
    "answer": "Hang With Me"
},
{
    "lyric": "I think that she is just a fangirl, get off of me.",
    "answer": "Hang With Me"
},
{
    "lyric": "She listen like a bitch, all black on my fit.",
    "answer": "Hang With Me"
},
{
    "lyric": "Cash, racks — something you don't know.",
    "answer": "Hang With Me"
},
{
    "lyric": "Money, bands — go get some fuckin' hoes.",
    "answer": "Hang With Me"
},
{
    "lyric": "Don't talk to me, bitch — talk to the hand.",
    "answer": "Hang With Me"
},
{
    "lyric": "If it ain't 'bout money, I don't give a fuck.",
    "answer": "Hang With Me"
},
{
    "lyric": "I saw her backstage — she gave me a hug.",
    "answer": "Hang With Me"
},
{
    "lyric": "I wanna see you get undressed — get undressed for me, I'm starin' like paparazzi.",
    "answer": "Haunted House"
},
{
    "lyric": "You're not my friend, so don't act like it.",
    "answer": "Haunted House"
},
{
    "lyric": "New year, new me — got blood on my jeans, on TV screens.",
    "answer": "Hollywood Dreams"
},
{
    "lyric": "Bad bitch on me — she's from the scene.",
    "answer": "Hollywood Dreams"
},
{
    "lyric": "I got rackies all on me, that's why she fuckin' with me.",
    "answer": "Hollywood Dreams"
},
{
    "lyric": "Bloody jeans and scary dreams, put me in a movie scene.",
    "answer": "Hollywood Dreams"
},
{
    "lyric": "Cameras pointed right at me — I just wanna hear you scream.",
    "answer": "Hollywood Dreams"
},
{
    "lyric": "I'm chasin' bags — why you chasin' me?",
    "answer": "IDGAF"
},
{
    "lyric": "I don't fuck with skeletons, so Xexio — get off my D.",
    "answer": "IDGAF"
}
]

    @app_commands.command(name="nick6383trivia", description="Answer a trivia question with Nick6383 lyrics.")
    @app_commands.checks.has_role(1371885746415341648)
    async def nick6383trivia(self, interaction: discord.Interaction):
        
        if interaction.channel_id != 1373112868249145485:
            await interaction.response.send_message("This command can only be used in the #trivia channel.", ephemeral=True)
            return

        entry = random.choice(self.trivia_data)
        lyric = entry["lyric"]
        correct = entry["answer"]
        all_titles = list(set([d["answer"] for d in self.trivia_data]))
        choices = random.sample([t for t in all_titles if t != correct], 3) + [correct]
        random.shuffle(choices)

        def make_result_embed(chosen, correct):
            color = discord.Color.green() if chosen == correct else discord.Color.red()
            title = "✅ Correct!" if chosen == correct else "❌ Incorrect."
            description = f"You chose **{chosen}**.\n\n" + ("You got it right!" if chosen == correct else f"Incorrect. The correct answer was **{correct}**.")
            return discord.Embed(title=title, description=description, color=color)

        class TriviaView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.answered = False

            async def handle(self, interaction_button: discord.Interaction, chosen):
                if interaction_button.user.id != interaction.user.id:
                    await interaction_button.response.send_message("Only the original user can answer this trivia.", ephemeral=True)
                    return
                if self.answered:
                    await interaction_button.response.send_message("You already answered.", ephemeral=True)
                    return
                self.answered = True
                result_embed = make_result_embed(chosen, correct)
                await interaction_button.response.send_message(embed=result_embed)

            @discord.ui.button(label=choices[0], style=discord.ButtonStyle.secondary)
            async def option1(self, interaction_button: discord.Interaction, button: discord.ui.Button):
                await self.handle(interaction_button, button.label)

            @discord.ui.button(label=choices[1], style=discord.ButtonStyle.secondary)
            async def option2(self, interaction_button: discord.Interaction, button: discord.ui.Button):
                await self.handle(interaction_button, button.label)

            @discord.ui.button(label=choices[2], style=discord.ButtonStyle.secondary)
            async def option3(self, interaction_button: discord.Interaction, button: discord.ui.Button):
                await self.handle(interaction_button, button.label)

            @discord.ui.button(label=choices[3], style=discord.ButtonStyle.secondary)
            async def option4(self, interaction_button: discord.Interaction, button: discord.ui.Button):
                await self.handle(interaction_button, button.label)

        embed = discord.Embed(
            title="Trivia",
            description=f"*{lyric}*",
            color=discord.Color.magenta()
        )
        embed.set_image(url="https://raw.githubusercontent.com/wereallinlove/WE-RE-ALL-IN-LOVE-BOT/main/nick6383.jpg")
        await interaction.response.send_message(embed=embed, view=TriviaView())

async def setup(bot):
    await bot.add_cog(Nick6383Trivia(bot))
