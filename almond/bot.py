import asyncio

import discord
from typing import Literal
from discord import Activity, ActivityType
from discord.ext import commands

from almond.cogs import MonitoringCog, EventsCog
from almond.settings import get_settings
from almond.logger import setup_logger


settings = get_settings()
intents = discord.Intents.all()
activity = Activity(type=ActivityType.watching, name="over your VPS")
bot = commands.Bot(command_prefix="!", activity=activity, intents=intents)

bot.settings = settings


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
    ctx: commands.Context,
    guilds: commands.Greedy[discord.Object],
    spec: Literal["~", "*", "^"] | None = None,
) -> None:
    """Sync all the slash commands of the bot.
    Syncs all slash commands for the bot,
    in the guild or globally.
    """

    # If no guilds are specified,
    # sync all the slash commands.
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        # Deide the scope of the sync
        scope = "to the current guild."
        if spec is None:
            scope = "globally."

        await ctx.send(f"Synced {len(synced)} commands {scope}")
        return

    # Sync all commands for each guild, if guilds are specified
    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def main(bot: commands.Bot) -> None:
    """Run the bot"""

    # Setup logging
    setup_logger()

    # Load cogs
    await bot.add_cog(EventsCog(bot))
    await bot.add_cog(MonitoringCog(bot))

    # Start bot
    await bot.start(settings.almond_token)


if __name__ == "__main__":
    asyncio.run(main(bot))
