import discord
import asyncio
import time
import json
import os

intents = discord.Intents.none()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

token = "<token>"
if os.path.exists("notify_disabled.json"):
    with open("notify_disabled.json", mode="r") as f:
        notify_disabled = json.load(f)
else:
    notify_disabled = []

sabach_id = 1233072112139501608

@client.event
async def on_message(message):
    if message.author.id == sabach_id and len(message.embeds) > 0 and message.embeds[0].footer != None and message.embeds[0].footer.text == "voted":
        if str(message.interaction_metadata.user.id) in notify_disabled:return
        next = message.embeds[0].fields[0].value.replace("<t:","").replace(":R>","")
        await message.channel.send(message.interaction_metadata.user.mention, embed=discord.Embed(title="投票通知", description="<t:"+next+":R> に投票通知を行います。", color=0x00ccff))
        await asyncio.sleep(int(next) - time.time())
        await message.channel.send(message.interaction_metadata.user.mention, embed=discord.Embed(title="投票通知", description="投票が出来るようになりました。\n</vote:1233256792507682860> で投票できます。", color=0x33aa55))

@client.event
async def on_ready():
    print("Bot is ready.")
    await tree.sync()

@tree.command(name="setnotify",description="投票通知を設定します。")
@discord.app_commands.describe(enable="投票通知")
async def setnotify(interaction: discord.Interaction, enable: bool):
    global notify_disabled
    filename = "notify_disabled.json"
    async with asyncio.Lock():
        if str(interaction.user.id) in notify_disabled:
            notify_disabled.remove(str(interaction.user.id))
        if not enable:
            notify_disabled.append(str(interaction.user.id))
        with open(filename, mode="w") as f:
            json.dump(notify_disabled, f)
    if enable:
        await interaction.response.send_message("投票通知を有効にしました。", ephemeral=True)
    else:
        await interaction.response.send_message("投票通知を無効にしました。", ephemeral=True)

client.run(token)
