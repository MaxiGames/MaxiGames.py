#shamelessly copied from kymchi

import discord
from discord.ext import commands
import datetime
import json
import config

class Client(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.help_command = None
        self.start_time = datetime.datetime.utcnow()
    
    @property
    def uptime(self):
        return datetime.datetime.utcnow() - self.start_time

    @property
    def config(self):
        return config
    
    @property
    def primary_colour(self):
        return self.config.primary_colour
    
    @property
    def error_colour(self):
        return self.config.error_colour
    
    @property
    def icon_url(self):
        return self.config.icon_url
    
    # async def start_bot(self):
    #     for extension in self.config.initial_extensions:
    #         try:
    #             self.load_extension(extension)
    #         except Exception:
    #             log.error(f"Failed to load extension {extension}.")
    #             log.error(traceback.print_exc())

        
    #     await self.start(self.config.token)
    
