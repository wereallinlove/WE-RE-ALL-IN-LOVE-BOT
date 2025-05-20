import discord
from discord.ext import commands
from discord import app_commands
import random

VERIFIED_ROLE_ID = 1371885746415341648
ALLOWED_CHANNEL_ID = 1373112868249145485

class MinesGame:
    def __init__(self, user_id: int, bomb_count: int):
        self.user_id = user_id
        self.bomb_count = bomb_count
        self.rows = 4
        self.cols = 5
        self.max_tiles = self.rows * self.cols
        self.bombs = set(random.sample(range(self.max_tiles), bomb_count))
        self.revealed = set()
        self.active = True

    def reveal(self, tile: int):
        if not self.active or tile in self.revealed:
            return None
        self.revealed.add(tile)
        if tile in self.bombs:
            self.active = False
            return "bomb"
        return "safe"

    def cash_out(self):
        self.active = False
        return len(self.revealed), False

    def lose(self):
        self.active = False
        return len(self.revealed), True

    def is_active(self):
        return self.active

    def display_board(self):
        grid = []
        for i in range(self.max_tiles):
            if i in self.revealed:
                if i in self.bombs:
                    grid.append("💥")
                else:
                    grid.append("✅")
            else:
                grid.append("🔳")
        rows = [" ".join(grid[i:i+self.cols]) for i in range(0, self.max_tiles, self.cols)]
        return "\n".join(rows)

active_games = {}

class MinesCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mines", description="Play a mines game with a 4x5 grid.")
    @app_commands.describe(bombs="How many bombs to place (1-19)")
    async def mines(self, interaction: discord.Interaction, bombs: int):
        if interaction.channel.id != ALLOWED_CHANNEL_ID:
            return await interaction.response.send_message("You can only use this command in the game channel.", ephemeral=True)

        if not any(role.id == VERIFIED_ROLE_ID for role in interaction.user.roles):
            return await interaction.response.send_message("You don’t have permission to use this command.", ephemeral=True)

        if bombs < 1 or bombs >= 20:
            return await interaction.response.send_message("Choose between 1 and 19 bombs.", ephemeral=True)

        if interaction.user.id in active_games:
            return await interaction.response.send_message("You already have a game in progress.", ephemeral=True)

        game = MinesGame(interaction.user.id, bombs)
        active_games[interaction.user.id] = game

        view = MinesView(game, interaction.user.id)

        embed = discord.Embed(
            title="💣 Mines Game Started",
            description=game.display_board(),
            color=0xFF69B4
        )
        await interaction.response.send_message(embed=embed, view=view)

class MinesView(discord.ui.View):
    def __init__(self, game: MinesGame, user_id: int):
        super().__init__(timeout=None)
        self.game = game
        self.user_id = user_id
        for i in range(game.max_tiles):  # 20 buttons
            self.add_item(MinesButton(i, game, user_id, self))
        self.add_item(CashOutButton(game, user_id))  # total = 21 = safe ✅

class MinesButton(discord.ui.Button):
    def __init__(self, index: int, game: MinesGame, user_id: int, view: discord.ui.View):
        super().__init__(style=discord.ButtonStyle.secondary, label=str(index+1), row=index // 5)
        self.index = index
        self.game = game
        self.user_id = user_id
        self.view_ref = view

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("You're not playing this game.", ephemeral=True)

        result = self.game.reveal(self.index)
        if result == "bomb":
            revealed, _ = self.game.lose()
            embed = discord.Embed(
                title="💥 You Lose!",
                description=f"You revealed {revealed} safe tile(s) before hitting a bomb.",
                color=0xFF0000
            )
            await interaction.response.edit_message(embed=embed, view=None)
            active_games.pop(self.user_id, None)
            return

        if result == "safe":
            embed = discord.Embed(
                title="💣 Mines Game",
                description=self.game.display_board(),
                color=0xFF69B4
            )
            await interaction.response.edit_message(embed=embed, view=self.view_ref)

class CashOutButton(discord.ui.Button):
    def __init__(self, game: MinesGame, user_id: int):
        super().__init__(style=discord.ButtonStyle.success, label="Cash Out 💸")
        self.game = game
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("You're not playing this game.", ephemeral=True)

        revealed, _ = self.game.cash_out()
        embed = discord.Embed(
            title="✅ You Cashed Out!",
            description=f"You safely revealed {revealed} tile(s).",
            color=0x00FF00
        )
        await interaction.response.edit_message(embed=embed, view=None)
        active_games.pop(self.user_id, None)

async def setup(bot):
    await bot.add_cog(MinesCommand(bot))
