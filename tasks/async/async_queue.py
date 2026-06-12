import asyncio
import logging

from pygments.lexers import q


async def main():
    q = asyncio.Queue()
    await q.put(1)
    await q.put(2)
    await q.put(3)

asyncio.run(main())


import asyncio

async def worker(q):
    while True:
        item = await q.get()
        logging.info('processiong')
        await asyncio.sleep(1)
        q.task_done()


async def main():
    q = asyncio.Queue()

    for _ in range(5):
        asyncio.create_task(worker(q))

    for i in range(4):
        await q.put(i)

    q.join() # чекаєм на завершення всіх задач

asyncio.run(main())