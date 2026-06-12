import asyncio


async def fanc(n):
    await asyncio.sleep(1)
    return n

# послідовне виконання
async def main():
    r1 = await fanc(1)
    r2 = await fanc(2)
    print('result', r1, r2)

asyncio.run(main())

# конкурентно
async def func(n):
    await asyncio.sleep(1)
    return n

async def main2():
    r1, r2 = await asyncio.gather(func(1), func(2))
    print('result', r1, r2)

asyncio.run(main2())


async def func(n):
    await asyncio.sleep(1)
    return n

async def main3():
    tasks = [asyncio.create_task(func(c)) for c in range(3)] # ту уже запуст тасок у фоні
    await asyncio.sleep(9999)


asyncio.run(main3())