import asyncio

async def fetch_data(n):
    print(f'start task {n}')
    await asyncio.sleep(1) # imitation oi,, this not block thread
    print(f'end task {n}')

async def main():
    await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3),
        fetch_data(4),
    )


asyncio.run(main())

