from discord.ext import commands

from almond.logger import log


class EventsCog(commands.Cog):
    """This is a cog for event listeners.

    Event listeners are executed automatically on a specific event.
    They can be used to handle errors, guild changes and more.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log("Bot is ready.")
