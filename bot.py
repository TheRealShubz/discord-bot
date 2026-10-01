import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("Bot is ready!")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")


@bot.command()
async def embed(ctx, title="Embed Title", description="Embed Description"):
    """Send a formatted embed message"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text="Embed sent by Discord Bot")
    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower() == "hello":
        await message.channel.send(f"Hi {message.author.mention}!")

    await bot.process_commands(message)


if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("DISCORD_TOKEN is missing. Add it to your .env file.")
    bot.run(TOKEN)
