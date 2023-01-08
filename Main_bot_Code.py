import discord
from discord.ext import commands, tasks
import random
import os 
from itertools import cycle


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents=intents)
Status = cycle(['Welcome to the The Blue Bird','Share our server link with your friends','HAve a great time here'])

token = "Your Bot token"

@bot.event
async def on_ready():
    change_status.start()
    print("BOT IS ONLINE!!")

@tasks.loop(seconds = 5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(Status)))

@bot.event 
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.send("Invalid command used")

@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server')

@bot.event
async def  on_member_remove(member):
    print(f'{member} has been removed form server')


#Greeting to bot
@bot.command(aliases=['hi','hello','Yo','Aye'])
async def greet(ctx):
    responses = ["Long time no see",
                "hello mate!!!",
                "welcome",
                "Its good to see you again!!"]
    
#clear messages
@bot.command()
async def clr(ctx,amount : int):
    await ctx.channel.purge(limit=amount)

@clr.error
async def clr_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
       await ctx.send("Please specify an amount of messages to delete")




#kicking/banning members
@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)    
    await ctx.send(f'Banned {member.mention}')

#unbanning member
@bot.command()
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_tag = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.tag) == (member_name,member_tag):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return




      

bot.run(token)