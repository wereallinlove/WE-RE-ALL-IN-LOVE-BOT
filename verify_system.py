import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands

import datetime

GUILD_ID = 1371732235963269130
VERIFY_CHANNEL_ID = 1371884372131319818
WAITING_ROOM_ID = 1381763578977194035
APPROVE_ROLE_ID = 1372695389555130420
VERIFIED_ROLE_ID = 1371885746415341648

class VerifySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(GUILD_ID)
        channel = guild.get_channel(VERIFY_CHANNEL_ID)
        role = guild.get_role(APPROVE_ROLE_ID)

        embed = discord.Embed(
            title="New Member Joined",
            description=f"{member.mention} has joined the server.\n\n{role.mention} Please approve or deny access.",
            color=discord.Color.dark_magenta()
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1318298515948048549/1372714113559824464/image.png")
        embed.set_footer(text=f"WE'RE ALL IN LOVE {datetime.datetime.now().year}")

        approve_button = discord.ui.Button(label="Approve", style=discord.ButtonStyle.success)
        deny_button = discord.ui.Button(label="Deny", style=discord.ButtonStyle.danger)

        view = discord.ui.View()
        view.add_item(approve_button)
        view.add_item(deny_button)

        async def approve_callback(interaction: discord.Interaction):
            if get(interaction.user.roles, id=APPROVE_ROLE_ID):
                await member.add_roles(guild.get_role(VERIFIED_ROLE_ID))
                approved_embed = discord.Embed(
                    title="✅ Member Approved",
                    description=f"{member.mention} has been approved by {interaction.user.mention}.",
                    color=discord.Color.green()
                )
                await channel.send(embed=approved_embed)

                try:
                    dm_embed = discord.Embed(
                        title="Welcome!",
                        description=f"You've been approved and are now a member of **{guild.name}**!",
                        color=discord.Color.green()
                    )
                    await member.send(embed=dm_embed)
                except:
                    pass

                await interaction.response.defer()
            else:
                await interaction.response.send_message("You are not authorized to approve members.", ephemeral=True)

        async def deny_callback(interaction: discord.Interaction):
            if get(interaction.user.roles, id=APPROVE_ROLE_ID):
                denied_embed = discord.Embed(
                    title="❌ Member Denied",
                    description=f"{member.mention} was denied access by {interaction.user.mention}.",
                    color=discord.Color.red()
                )
                await channel.send(embed=denied_embed)

                try:
                    dm_embed = discord.Embed(
                        title="Application Denied",
                        description=f"Unfortunately, you were denied access to **{guild.name}**.",
                        color=discord.Color.red()
                    )
                    await member.send(embed=dm_embed)
                except:
                    pass

                await member.kick(reason="Verification Denied")
                await interaction.response.defer()
            else:
                await interaction.response.send_message("You are not authorized to deny members.", ephemeral=True)

        approve_button.callback = approve_callback
        deny_button.callback = deny_callback

        await channel.send(embed=embed, view=view)

        # Send DM welcome embed
        try:
            dm_embed = discord.Embed(
                title="Welcome to the Server",
                description=f"Hey {member.mention}, you're in limbo right now while we review your application. You can wait in <#{WAITING_ROOM_ID}> until someone approves or denies you.",
                color=discord.Color.dark_magenta()
            )
            dm_embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
            dm_embed.set_footer(text=f"WE'RE ALL IN LOVE {datetime.datetime.now().year}")
            await member.send(embed=dm_embed)
        except:
            pass


async def setup(bot):
    await bot.add_cog(VerifySystem(bot))
