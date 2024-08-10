import discord
import asyncio
import time

intents = discord.Intents.none()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

token = "<token>"

sabach_id = 1233072112139501608

@client.event
async def on_message(message):
    if message.author.id == sabach_id and len(message.embeds) > 0 and message.embeds[0].footer != None and message.embeds[0].footer.text == "voted":
        next = message.embeds[0].fields[0].value.replace("<t:","").replace(":R>","")
        await message.channel.send(message.interaction_metadata.user.mention+" さんが投票しました。\n<t:"+next+":R> に通知します。")
        await asyncio.sleep(int(next) - time.time())
        await message.channel.send(message.interaction_metadata.user.mention+" 投票が再度出来るようになりました。")

client.run(token)
