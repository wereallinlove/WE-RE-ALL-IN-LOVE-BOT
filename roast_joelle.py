import random
import discord
from discord import app_commands
from discord.ext import commands

class RoastJoelle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roastjoelle", description="Roast Joelle Joshua Saint Surin mercilessly.")
    @app_commands.checks.has_role(1371885746415341648)
    async def roastjoelle(self, interaction: discord.Interaction):
        if interaction.channel.id != 1318298515948048549:
            await interaction.response.send_message("❌ This command can only be used in the designated roast channel.", ephemeral=True)
            return

        roasts = [
            "You're so bad at Valorant, your aim needs a seeing eye dog.",
            "You play DBD like you’re trying to get tunneled IRL.",
            "Minecraft kicked you out for building crimes.",
            "You love chicken and watermelon like it’s a loadout.",
            "Joelle, you’re so bitchmade you came with a receipt.",
            "August > Joelle in every dimension of existence.",
            "Fuck you Joelle.",
            "You're the reason tutorials exist.",
            "You're built like a loading screen.",
            "Even the bots report you.",
            "No bitches want you, Joelle.",
            "You're a walking L highlight reel.",
            "Joelle, you solo queue like a hazard warning.",
            "You play like your monitor is turned off.",
            "You aim like you're playing on a trampoline.",
            "Your KD ratio is a hate crime.",
            "Joelle, you're the opposite of clutch.",
            "Your builds in Minecraft look like cry-for-help notes.",
            "If you were a killer in DBD, I’d DC out of pity.",
            "Joelle, you're such a liability, people fake AFK to avoid you.",
            "You’re like a tutorial boss that never levels up.",
            "Joelle, your crosshair is just decorative at this point.",
            "You peak like you want to die.",
            "Even the Entity said 'nah' and disconnected.",
            "You fall for the same trap five times in one game.",
            "Joelle, if L's were a stat, you'd be prestige 99.",
            "You're the reason people alt-F4.",
            "Nobody mains failure like you do.",
            "You’re worse than lag.",
            "The only thing you clutch is defeat.",
            "Joelle, your Valorant skills are a public safety hazard.",
            "You aim like your mouse is upside down.",
            "Your in-game awareness is legally blind.",
            "You die more than plot devices in horror movies.",
            "You got kicked from a casual game for being too casual.",
            "Even Spectator mode gets bored watching you.",
            "Joelle, you’re the tutorial level boss… but weaker.",
            "The Entity is filing a restraining order against you.",
            "Joelle, your rank is a myth.",
            "Your Minecraft redstone contraptions are just TNT traps for yourself.",
            "You're a jump-scare in team voice chat.",
            "Joelle, you're proof that matchmaking is broken.",
            "You couldn’t win a 1v1 if it was rigged for you.",
            "You lose aim duels to AFK players.",
            "You play horror games like a romcom.",
            "Even NPCs talk shit about your gameplay.",
            "You're the last person someone wants to revive.",
            "Your builds look like you gave up halfway—and then again.",
            "Joelle, you could camp in DBD and still get 0 kills.",
            "You bring emotional damage to your team.",
            "Joelle, your loadouts look like randomized presets.",
            "You're a ping spike in human form.",
            "Your 'highlights' are just you dying creatively.",
            "You use flashbangs to blind your own team.",
            "Joelle, you’re the reason friendly fire was removed.",
            "You play like you’re lagging… in real life.",
            "Joelle, you get outplayed by tutorials.",
            "You thought crouching in Valorant made you invisible.",
            "Joelle, your skill tree has no branches.",
            "You play like the controls are in hieroglyphics.",
            "Even your Minecraft pets try to escape you.",
            "Joelle, you're the DLC no one asked for.",
            "You play like the game is trying to uninstall itself.",
            "You're the boss fight that players skip.",
            "Your Valorant aim is so off, it needs a GPS.",
            "Joelle Joshua Saint Surin is a walking uninstall button.",
            "Even the killer in DBD runs away from you.",
            "You die so fast it counts as teleportation.",
            "Your crosshair is allergic to heads.",
            "Joelle, even shadows outmaneuver you.",
            "Your builds have no symmetry, just sadness.",
            "Joelle, if I gave you a free win, you'd still lose it.",
            "Your flashlight saves in DBD are just you clicking into darkness.",
            "Joelle, every time you log on, the MMR drops in protest.",
            "You use aim assist and still miss everything.",
            "Joelle, your teammates prefer the killer.",
            "You're so bad, your team queues without you.",
            "You bring a knife to a gunfight and then drop it.",
            "You're the first one dead and the last one blamed.",
            "Even mobile players feel superior to you.",
            "Joelle, you couldn’t clutch a door handle.",
            "Your only W is your WiFi password.",
            "Joelle, you're a stat booster for the enemy team.",
            "You die so much the game sends flowers.",
            "Joelle, the best thing about your gameplay is the silence.",
            "You build walls and then walk into them.",
            "Joelle, your best plays are accidents.",
            "You peak like you’re practicing suicide.",
            "You bring bad luck to digital life.",
            "Joelle, the controller disconnects in fear when you touch it.",
            "You're proof that matchmaking is punishment-based.",
            "Even the bots dodge your lobbies.",
            "Your DBD perks are just coping mechanisms.",
            "Your strategies are just loud panic.",
            "Joelle, you play every game like it’s your first.",
            "Joelle Joshua Saint Surin—name longer than your kill count.",
            "August is better than you at life and death.",
            "You get caught lacking before the round starts.",
            "Joelle, you're a lag spike disguised as a teammate.",
            "You play like every match is a social experiment.",
            "Joelle, I’d rather 1v4 than queue with you.",
            "You're the reason teammates fake DC.",
            "Joelle, you need a training arc... and a new identity."
        ]

        roast = random.choice(roasts)
        await interaction.response.send_message(f"<@781019397820645386> {roast}")

async def setup(bot):
    await bot.add_cog(RoastJoelle(bot))
