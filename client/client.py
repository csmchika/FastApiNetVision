import random
import string

import aiohttp
import asyncio


class Client:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.numDelete = 0
        self.numDeleteAll = 0

    @staticmethod
    def generate_string():
        return "".join(random.choice(string.digits+string.ascii_letters) for i in range(16))

    @staticmethod
    async def iterator(count):
        for i in range(count):
            yield i
            await asyncio.sleep(0.0)

    async def create_post(self):
        async with self.session.post(url="http://127.0.0.1:8000/items/new",
                                     json={"text": self.generate_string()}) as response:
            assert response.status == 200

    async def delete_posts(self):
        async with self.session.get("http://127.0.0.1:8000/items/10") as response:
            items = await response.json()
            async for i in self.iterator(len(items)):
                async with self.session.delete(f'http://127.0.0.1:8000/items/{items[i]["uuid"]}') as response_:
                    assert response_.status == 200
                    self.numDelete += 1
                    self.numDeleteAll += 1

    async def count_delete(self):
        while True:
            await asyncio.sleep(10)
            print(f"Удалено за последние 10 секунд: {self.numDelete}")
            print(f"Удалено всего: {self.numDeleteAll}")
            self.numDelete = 0

    async def start(self):
        asyncio.create_task(self.count_delete())
        while True:
            try:
                create_list = [self.create_post() for i in range(random.randint(10, 101))]
                await asyncio.gather(*create_list, self.delete_posts())
            except aiohttp.ClientConnectorError:
                print("Ошибка подключения, пробую переподключиться")
                await asyncio.sleep(5)


async def main():
    async with aiohttp.ClientSession() as session:
        await Client(session).start()

if __name__ == '__main__':
    asyncio.run(main())
