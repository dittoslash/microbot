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
	return ctx.guild.get_role(cfg["server"]["admin_role"]) in ctx.author.roles

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

@bot.command()
@commands.check(adminPerms)
async def sas(ctx, role, category=""):
	r = discord.utils.get(ctx.guild.roles, name=role)
	if not r and role in cfg["roles"]["roles"]: #role exists in config, not in server
		await ctx.send("you've fucked something up. the role exists in config, but not on the server. fix ur shit b")
	elif role in cfg["roles"]["roles"]: #role exists in config
		await ctx.send("role exists")
	else:
		if cfg["roles"]["enable_categories"]:
			if not cfg["roles"]["categories"][category]: cfg["roles"]["categories"][category] = [] #create category if it doesn't exist
			cfg["roles"]["categories"][category].append(role) #add the shit to the category
		else: cfg["roles"]["roles"].append(role) #add the shit to the not category
		if not r: ctx.guild.create_role(name=role) #create role if it doesn't exist
		toml.dump(cfg, open("config.toml", 'w')) #write shit to config
		loadCFG() #reload config, which'll repopulate the cfg.roles.roles if we're using categories
		await ctx.send("role created")

bot.run(cfg["connection"]["token"])