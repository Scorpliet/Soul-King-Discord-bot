  
import discord
from discord.ext import commands
import traceback
import difflib
import re
import sys
class ErrorHandling(commands.Cog):
    """
    Cog with global error handler.
    """
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error, *, from_local=False):
        """
        Global error handler.
        ---------------------
        If an error is raised in a command, it goes to the local error handler.
        If the local error handler handles the error correctly, the global error handler does nothing.
        If the local error handler does not handle the error correctly, then it goes to the global error handler.
        """
        if hasattr(ctx.command, "on_error") and not from_local:
            return
        error = getattr(error, "original", error)

        if isinstance(error, commands.CommandNotFound):
            pass
            #failed_command = re.match(f"^({ctx.prefix})\s*(.*)", ctx.message.content, flags=re.IGNORECASE).group(2)
            #matches = difflib.get_close_matches(failed_command, ctx.bot.command_list)
            #if not matches:
                #return
            #await ctx.send(f"Command '{failed_command}' is not found. Did you mean `{matches[0]}`?")

        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown, try again in `{error.retry_after:.2f}` seconds.")

        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"No you cannot run the `{ctx.command}` command lmao.")

        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command can only be used in a server.")

        elif isinstance(error, commands.MissingPermissions):
            perms = ctx.bot.utils.humanize_list(error.missing_perms).replace("_", " ").replace("guild", "server")
            await ctx.send(f"You are missing the `{perms}` permission(s) to use this command.")

        elif isinstance(error, commands.BotMissingPermissions):
            perms = ctx.bot.utils.humanize_list(error.missing_perms).replace("_", " ").replace("guild", "server")
            await ctx.send(f"I am missing the `{perms}` permission(s) to use this command.")


        elif isinstance(error, discord.HTTPException):
            embed = discord.Embed(
                title=f"An HTTP Exception Occurred",
                description=
                f"HTTP error code `{error.status}`\n"
                f"Discord error code `{error.code}` ([understanding what the error codes mean](https://discord.com/developers/docs/topics/opcodes-and-status-codes#http-http-response-codes))",
                colour=discord.Color.gold())
            embed.add_field(name="Error Message", value=error.text or "No error message.")
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException:  # missing send messages permission or discord is having issues
                try:
                    await ctx.author.send(embed=embed)
                except discord.HTTPException:  # can't send to dms either
                    pass

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title=f"`{str(error.param).split(':')[0]}` is a required argument that is missing.",
                description=f"For more information on what arguments this command requires, do `brook help {ctx.command}`.",
                colour=discord.Color.gold())
            await ctx.send(embed=embed)

        elif isinstance(error, (commands.MessageNotFound, commands.ChannelNotFound, commands.MemberNotFound, commands.EmojiNotFound, commands.RoleNotFound, commands.UserNotFound)):
            await ctx.send(error)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title=str(error),
                description=f"For more information on what arguments this command requires, do `brook help {ctx.command}`.",
                colour=discord.Color.gold())
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadUnionArgument):
            embed = discord.Embed(
                title=str(error),
                description=f"For more information on what arguments this command requires, do `brook help {ctx.command}`.",
                colour=discord.Color.gold())
            await ctx.send(embed=embed)

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send(error)

        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send(f"The `{ctx.command}` command is limited to `{error.number}` {'use' if error.number == 1 else 'uses'} per `{error.per.name}` at a time.")

        elif isinstance(error, commands.CheckFailure):
            pass

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandling())