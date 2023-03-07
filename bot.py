import asyncio, pickle, discord,spider
with open('config.pkl',mode='rb') as file: config=pickle.load(file)

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    async def backgrount_task(self):
        await self.wait_until_ready()
        channel=self.get_channel(config['channel_id'])
        sleep_time=60*60
        fail_count=0
        while not self.is_closed():
            try: news_list=await spider.get_tnfsh_news()
            except Exception:
                print('cannot connect to source')
                if fail_count >= 5:
                    print('retry in 3600s')
                    sleep_time=60*60
                else:
                    print('retry in 5s')
                    fail_count+=1
                    sleep_time=5
            else:
                fail_count=0
                if len(news_list)==0: print('no news detected')
                for item in news_list:
                    message=spider.news_to_str(item)
                    print(message)
                    self.loop.create_task(channel.send(message))
                    await asyncio.sleep(.5)
                sleep_time=60*60
            
            print('sleep')
            await asyncio.sleep(sleep_time)

    async def setup_hook(self) -> None:
        self.loop.create_task(self.backgrount_task())

client=MyClient(intents=discord.Intents.default())
client.run(config['token'])
