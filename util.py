def check_can_message_channel(ctx, cfg):
	channel = ctx.channel

	if cfg["server"]["server_id"] != ctx.guild.id and cfg["server"]["force_server"]:
		return False
	if not channel in cfg["server"]["channels"] and cfg["server"]["force_channels"]:
		return False
	if channel in cfg["server"]["ignore_channels"]:
		return False
	if cfg["server"]["ignore_others"] and not channel in cfg["server"]["channels"]:
		return False
	return True
def check_can_interact_channel(ctx, cfg):
	return not (cfg["server"]["ignore_others"] and channel in cfg["server"]["channels"])