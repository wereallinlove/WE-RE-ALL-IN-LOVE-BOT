import discord
from discord.ext import commands
from discord import app_commands
import random

VERIFIED_ROLE_ID = 1371885746415341648
ALLOWED_CHANNEL_ID = 1373112868249145485

duels = {}

class MinesDuelGame:
    def __init__(self, user1: discord.User, user2: discord.User, bombs: int):
        self.user1 = user1
        self.user2 = user2
        self.bombs = bombs
        self.grid_size = 20
        self.bombs_user1 = set(random.sample(range(self.grid_size), bombs))
        self.bombs_user2 = set(random.sample(range(self.grid_size), bombs))
        self.revealed_user1 = set()
        self.revealed_user2 = set()
        self.done_user1 = False
        self.done_user2 = False
        self.loser = None

    def reveal(self, user: discord.User, tile: int):
        if user == self.user1:
            if self.done_user1 or tile in self.revealed_user1:
                return None
            self.revealed_user1.add(tile)
            if tile in self.bombs_user1:
                self.done_user1 = True
                self.loser = self.user1
                return "bomb"
            return "safe"

        elif user == self.user2:
            if self.done_user2 or tile in self.revealed_user2:
                return None
            self.revealed_user2.add(tile)
            if tile in self.bombs_user2:
                self.done_user2 = True
                self.loser = self.user2
                return "bomb"
            return "safe"

    def cash_out(self, user: discord.User):
        if user == self.user1:
            self.done_user1 = True
        elif user == self.user2:
            self.done_user2 = True

    def check_winner(self):
        if self.loser:
            return self.user2 if self.loser == self.user1 else self.user1
        if self.done_user1 and self.done_user2:
            if len(self.revealed_user1) > len(self.revealed_user2):
                return self.user1
            elif len(self.revealed_user2) > len(self.revealed_user1):
                return self.user2
            else:
                return "tie"
        return None

    def is_complete(self):
        return self.loser or (self.done_user1 and self.done_user2)

    def display_board(self, user: discord.User, final=False):
        grid = []
        revealed = self.revealed_user1 if user == self.user1 else self.revealed_user2
        bombs = self.bombs_user1 if user == self.user1 else self.bombs_user2
        for i in range(self.grid_size):
            if i in revealed:
                if i in bombs:
                    grid.append("💥")
                else:
                    grid.append("✅" if final else "🟩")
            else:
                grid.append("⬜")
        rows = [" ".join(grid[i:i+5]) for i in range(0, self.grid_size, 5)]
        return "\n".join(rows)

    def player_status(self, user: discord.User):
        if user == self.user1:
            done = self.done_user1
            revealed = len(self.revealed_user1)
            lost = self.loser == self.user1
        else:
            done = self.done_user2
            revealed = len(self.revealed_user2)
            lost = self.loser == self.user2

        emoji = "💥" if lost else "✅" if done else "🔳"
        return f"{emoji} {user.mention} - {revealed} safe tiles"

class CashOutButton(discord.ui.Button):
    def __init__(self, game: MinesDuelGame, user: discord.User):
        super().__init__(style=discord.ButtonStyle.success, label="Cash Out 💸")
        self.game = game
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        self.game.cash_out(self.user)
        if self.game.is_complete():
            await send_final_embed(interaction, self.game)
        else:
            await interaction.response.send_message("You cashed out! Waiting on your opponent.", ephemeral=True)

class MinesDuelView(discord.ui.View):
    def __init__(self, game: MinesDuelGame, user: discord.User):
        super().__init__(timeout=None)
        self.game = game
        self.user = user
        for i in range(20):
            self.add_item(MinesDuelButton(i, game, user, self))
        self.add_item(CashOutButton(game, user))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.user

class MinesDuelButton(discord.ui.Button):
    def __init__(self, index: int, game: MinesDuelGame, user: discord.User, view: discord.ui.View):
        super().__init__(style=discord.ButtonStyle.secondary, label=str(index + 1), row=index // 5)
        self.index = index
        self.game = game
        self.user = user
        self.view_ref = view

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            return await interaction.response.send_message("This is not your board.", ephemeral=True)

        result = self.game.reveal(self.user, self.index)
        if result is None:
            return await interaction.response.send_message("Already clicked or finished.", ephemeral=True)

        if result == "bomb" or self.game.is_complete():
            await send_final_embed(interaction, self.game)
            return

        embed = discord.Embed(
            title=f"{self.user.display_name}'s Board",
            description=self.game.display_board(self.user),
            color=0xFF69B4
        )
        await interaction.response.edit_message(embed=embed, view=self.view_ref)

async def send_final_embed(interaction, game: MinesDuelGame):
    winner = game.check_winner()
    embed = discord.Embed(title="👑 Duel Over!", color=0xFF0000)
    if winner == "tie":
        embed.description = "🤝 It's a tie! Both players revealed the same number of tiles."
    elif isinstance(winner, discord.User):
        loser = game.user2 if winner == game.user1 else game.user1
        embed.description = f"👑 {winner.mention} **has won the duel!**\n💀 {loser.mention} **has lost.**"
    else:
        embed.description = f"👑 {game.check_winner().mention} has won the duel."

    embed.add_field(name="Players", value=f"{game.player_status(game.user1)}\n{game.player_status(game.user2)}", inline=False)
    embed.add_field(name=f"{game.user1.display_name}'s Board", value=game.display_board(game.user1, final=True), inline=False)
    embed.add_field(name=f"{game.user2.display_name}'s Board", value=game.display_board(game.user2, final=True), inline=False)
    embed.set_footer(text=f"This duel used {game.bombs} bombs per player.")
    await interaction.channel.send(embed=embed)
    duels.pop(game.user1.id, None)
    duels.pop(game.user2.id, None)

class MinesDuel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="minesduel", description="Duel someone in a game of mines. Highest number of safe tiles wins!")
    @app_commands.describe(opponent="The user you want to duel", bombs="Number of bombs (1-19)")
    async def minesduel(self, interaction: discord.Interaction, opponent: discord.Member, bombs: int):
        if interaction.channel.id != ALLOWED_CHANNEL_ID:
            return await interaction.response.send_message("You can only use this command in the game channel.", ephemeral=True)

        if not any(role.id == VERIFIED_ROLE_ID for role in interaction.user.roles):
            return await interaction.response.send_message("You don’t have permission to use this command.", ephemeral=True)

        if not any(role.id == VERIFIED_ROLE_ID for role in opponent.roles):
            return await interaction.response.send_message("The user you're challenging is not verified.", ephemeral=True)

        if bombs < 1 or bombs >= 20:
            return await interaction.response.send_message("Choose between 1 and 19 bombs.", ephemeral=True)

        if opponent.bot:
            return await interaction.response.send_message("You can't duel a bot.", ephemeral=True)

        if interaction.user.id in duels or opponent.id in duels:
            return await interaction.response.send_message("One of you is already in a duel.", ephemeral=True)

        duel = MinesDuelGame(interaction.user, opponent, bombs)
        duels[interaction.user.id] = duel
        duels[opponent.id] = duel

        announce = discord.Embed(
            title="💣 Duel Started!",
            description=f"{interaction.user.mention} vs {opponent.mention}\nEach player has **{bombs} bombs** hidden. Safely uncover tiles or cash out!",
            color=0xFF69B4
        )
        await interaction.response.send_message(embed=announce)

        embed1 = discord.Embed(title=f"{interaction.user.display_name}'s Board", description=duel.display_board(interaction.user), color=0xFF69B4)
        embed2 = discord.Embed(title=f"{opponent.display_name}'s Board", description=duel.display_board(opponent), color=0xFF69B4)

        await interaction.channel.send(embed=embed1, view=MinesDuelView(duel, interaction.user))
        await interaction.channel.send(embed=embed2, view=MinesDuelView(duel, opponent))

async def setup(bot):
    await bot.add_cog(MinesDuel(bot))
