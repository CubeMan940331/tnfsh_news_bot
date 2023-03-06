import pickle
with open('config.pkl',mode='rb') as file: config=pickle.load(file)
import spider
import discord
import asyncio

client=discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    while True:
        news_list=spider.get_tnfsh_new()
        for item in news_list:
            message=spider.news_to_str(item)
            print(message)
            await client.get_channel(config['channel_id']).send(message)
        await asyncio.sleep(60*60)

client.run(config['token'])
