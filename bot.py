import os

import discord
from discord import app_commands
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
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


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
        color=discord.Color.blue(),
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text="Embed sent by Discord Bot")
    await ctx.send(embed=embed)


@bot.tree.command(name="embed", description="Send a formatted embed message")
@app_commands.describe(title="Title of the embed", description="Description text for the embed")
async def embed_slash(interaction: discord.Interaction, title: str = "Embed Title", description: str = "Embed Description"):
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue(),
    )
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    embed.set_footer(text="Embed sent by Discord Bot")
    await interaction.response.send_message(embed=embed)


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
