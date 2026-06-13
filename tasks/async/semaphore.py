import asyncio
import aiohttp


semaphore = asyncio.Semaphore(10)


async def fetch_data(url, session):
    async with semaphore:
        async with session.get(url) as response:
            return await response.read()


async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://www.example.org/'] * 20
        tasks = [fetch_data(u, session) for u in urls]
        await asyncio.gather(*tasks)

asyncio.run(main())


### or


async def supervisor(tasks):
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
    for task in pending:
        task.cancel()

    for task in done:
        if task.exception():
            print("task failed", task.exception())
        else:
            print("task succeeded", task.result())
            

async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://www.example.org/'] * 20
        tasks = [fetch_data(u, session) for u in urls]
        await supervisor(tasks)