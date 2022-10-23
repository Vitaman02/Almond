import aiohttp
import discord
from discord import app_commands as slash_commands
from discord.ext import commands, tasks

from almond import constants as const
from almond.logger import log
from almond.helpers import get_host_usage


class MonitoringCog(commands.Cog):
    """This is a cog used for monitoring.

    It's used for monitoring and alerting
    when high cpu or memory usage is detected
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.alert_message = "VPS: {}\nCPU: {}%\nMEM: {}%\nDisk: {}%"
        self.current_cpu_usage = 0
        self.current_mem_usage = 0
        self.resolved = True
        self.monitoring.start()

    @tasks.loop(seconds=30)
    async def monitoring(self) -> None:
        """Monitor cpu and memory usage"""

        # Don't send any more alerts if the
        # previous one has not been resolved
        if not self.resolved:
            return

        settings = self.bot.settings

        # Get cpu and memory usage percentage
        data = await get_host_usage(f"{settings.host_url}/usage")
        
        # Unload data
        cpu = data["cpu"]
        mem = data["memory"]
        disk = data["disk"]
        
        # Check if cpu or memory usage is above threshold
        if cpu >= settings.cpu_threshold or mem >= settings.mem_threshold:
            log(f"Sent alert for: CPU: {cpu}% | MEM: {mem}% | Disk: {disk}%")

            # Create alert message
            alert_message = "⚠⚠⚠ HIGH USAGE ALERT ⚠⚠⚠\n```"
            alert_message += self.alert_message.format(settings.vps_name, cpu, mem, disk)
            alert_message += "```"

            # Send alert
            alerting_channel = self.bot.get_channel(const.ALERTING_CHANNEL_ID)
            self.resolved = False
            await alerting_channel.send(alert_message)

    @monitoring.before_loop
    async def before_monitoring(self) -> None:
        """Wait for the bot to be ready"""

        await self.bot.wait_until_ready()

    @slash_commands.command(
        name="status",
        description="Get the current CPU, MEM and disk usage",
    )
    async def status(self, interaction: discord.Interaction) -> None:
        """Get the current CPU and MEM usage"""

        settings = self.bot.settings

        # Get cpu, memory and disk usage percentage
        data = await get_host_usage(f"{settings.host_url}/usage")
        cpu = data["cpu"]
        mem = data["memory"]
        disk = data["disk"]

        # Send status message
        alert_message = self.alert_message.format(settings.vps_name, cpu, mem, disk)
        await interaction.response.send_message(alert_message)

    @slash_commands.command(name="resolved", description="Set alert status as resolved")
    async def resolved(self, interaction: discord.Interaction) -> None:
        """Set alert status as resolved"""

        self.resolved = True
        await interaction.response.send_message(
            "Alert status set as resolved", ephemeral=True
        )
