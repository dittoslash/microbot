import discord #yep
from discord.ext import commands
import toml #.INIs on steroids
import os #file shit
import logging as log #print() on steroids
import util
import asyncio

cfg = {}

def loadCFG():
	global cfg
	log.debug("loading config...")
	if os.path.isfile("config.toml"): #check file exists
		cfg = toml.load("config.toml") #parse toml
		log.debug("config loaded successfully")
	else:
		log.critical("config file not found, copy config.default.toml to config.toml and configure properly")
		exit()

	if cfg["roles"]["enable_categories"]:
		for cat, vals in cfg["roles"]["categories"].items():
			cfg["roles"]["roles"] += vals

	print(cfg)



log.basicConfig(level=log.INFO, format='[%(levelname)s] %(message)s')

log.info("==µBot==")
loadCFG()
bot = commands.Bot(command_prefix='u')

@bot.event
async def on_ready():
	log.info("Ready!")

@bot.command()
async def reloadcfg(ctx):
	loadCFG()
	await ctx.send("done")

@bot.command()
async def roles(ctx):
	if cfg["roles"]["enable_categories"]:
		out = ""
		for cat, vals in cfg["roles"]["categories"].items():
			out += "{}: `{}`\n".format(cat, ", ".join(vals))
		await ctx.send(out)
	else:
		await ctx.send("`{}`".format(", ".join(cfg["roles"]["roles"])))

@bot.command()
async def role(ctx, role):
	r = discord.utils.get(ctx.guild.roles, name=role)
	if r and role in cfg["roles"]["roles"]:
		if r in ctx.author.roles:
			await ctx.author.remove_roles(r)
			await ctx.send("removed role {}, you had it already".format(role))
		else:
			await ctx.author.add_roles(r)
			await ctx.send("ok, granted role {}".format(role))
	else: await ctx.send("role unknown or ungrantable")

bot.run(cfg["connection"]["token"])