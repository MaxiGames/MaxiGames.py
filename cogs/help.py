import discord
from discord.ext.commands import Bot, Cog, Command, Context, Group, HelpCommand

class CustomHelpCommand(HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'description': 'Shows this help message.',
            'hidden': True
        })



class Help (Cog):
    def __init__(self, client):
        self.client = client
        self.old_help_command = client.help_command
        client.help_command = CustomHelpCommand()
        client.help_command.cog = self

def setup(client):
    client.add_cog(Help(client))