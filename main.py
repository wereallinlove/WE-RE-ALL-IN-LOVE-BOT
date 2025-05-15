import discord
from discord.ext import commands
from discord.ui import Button, View
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

ADMIN_CHANNEL_ID = 1318298515948048549
APPROVED_ROLE_NAME = "WE'RE ALL IN LOVE"
APPROVER_ROLE_NAME = ".approve"

recent_joins = set()

class ApproveButton(Button):
    def __init__(self, member_id):
        super().__init__(label="Approve", style=discord.ButtonStyle.success, custom_id=f"approve:{member_id}")

    async def callback(self, interaction: discord.Interaction):
        approver_role = discord.utils.get(interaction.user.roles, name=APPROVER_ROLE_NAME)
        if not approver_role:
            await interaction.response.send_message("You must have the `.approve` role to approve members.", ephemeral=True)
            return

        member_id = int(self.custom_id.split(":")[1])
        guild = interaction.guild
        member = guild.get_member(member_id)

        if not member:
            await interaction.response.send_message("Could not find the member to approve.", ephemeral=True)
            return

        role = discord.utils.get(guild.roles, name=APPROVED_ROLE_NAME)
        if not role:
            await interaction.response.send_message("Approved role not found.", ephemeral=True)
            return

        await member.add_roles(role)
        await interaction.response.edit_message(
            content=f"{member.mention} has been approved and given the role '{role.name}'.",
            embed=None,
            view=None
        )

class ApprovalView(View):
    def __init__(self, member_id):
        super().__init__(timeout=None)
        self.add_item(ApproveButton(member_id))

@bot.event
async def on_ready():
    bot.add_view(ApprovalView(0))
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    if member.id in recent_joins:
        return

    recent_joins.add(member.id)
    await asyncio.sleep(5)
    recent_joins.remove(member.id)

    channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if not channel:
        print("Admin channel not found.")
        return

    embed = discord.Embed(
        title="WE'RE ALL IN LOVE",
        description=f"{member.mention} joined the server.\n\nGrant them access to **WE'RE ALL IN LOVE**?",
        color=discord.Color.purple()
    )

    await channel.send(embed=embed, view=ApprovalView(member.id))

# Keep-alive for Render
from keep_alive import keep_alive
keep_alive()

bot.run(os.getenv("TOKEN"))
