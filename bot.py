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

async def adminPerms(ctx):
	return ctx.guild.get_role(cfg["server"]["admin_role"]) in ctx.member.roles

log.basicConfig(level=log.INFO, format='[%(levelname)s] %(message)s')

log.info("==µBot==")
loadCFG()
bot = commands.Bot(command_prefix='u!')

@bot.event
async def on_ready():
	log.info("Ready!")

@bot.command()
async def reloadcfg(ctx):
	if not util.check_can_message_channel(ctx, cfg): return
	loadCFG()
	await ctx.send("done")

@bot.command()
async def roles(ctx):
	if not util.check_can_message_channel(ctx, cfg): return
	if cfg["roles"]["enable_categories"]:
		out = ""
		for cat, vals in cfg["roles"]["categories"].items():
			out += "{}: `{}`\n".format(cat, ", ".join(vals))
		await ctx.send(out)
	else:
		await ctx.send("`{}`".format(", ".join(cfg["roles"]["roles"])))

@bot.command()
async def iam(ctx, role):
	if not util.check_can_message_channel(ctx, cfg): return
	r = discord.utils.get(ctx.guild.roles, name=role)
	if r and role in cfg["roles"]["roles"] and not r in ctx.author.roles:
			await ctx.author.add_roles(r)
			await ctx.send("ok, granted role {}".format(role))
	else: await ctx.send("role unknown, ungrantable, or you already have it")

@bot.command()
async def iamnot(ctx, role):
	if not util.check_can_message_channel(ctx, cfg): return
	r = discord.utils.get(ctx.guild.roles, name=role)
	if r and role in cfg["roles"]["roles"] and r in ctx.author.roles:
			await ctx.author.remove_roles(r)
			await ctx.send("removed role {}".format(role))
	else: await ctx.send("role unknown, ungrantable, or you don't have it")

bot.run(cfg["connection"]["token"])