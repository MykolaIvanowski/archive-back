import logging

import aiohttp
import asyncio


session = None

async def get_session():
    global session
    if session is None:
        session = aiohttp.ClientSession()

    return session


async def fetch_data(url):
    try:
        session = await get_session()
        async with session.get(url) as response:
            return await response.text()
    except aiohttp.ClientError as e:
        logging.error(e)
    except asyncio.TimeoutError as e:
        logging.error(e)


async def main():
    print(await fetch_data('http://example/getdata'), "to do")

asyncio.run(main())


async def post_data(url, data):
    try:
        session = await get_session()
        async with session.post(url, data=data) as response:
            response = await response.json()
    except aiohttp.ClientError as e:
        logging.error(e)
    except asyncio.TimeoutError as e:
        logging.error(e)



from fastapi import FastAPI
import aiohttp


### Fast api version

app = FastAPI()
session: aiohttp.ClientSession | None = None


@app.on_event('startup')
async def startup():
    global session
    session = aiohttp.ClientSession()

@app.on_event('shutdown')
async def shutdown():
    await session.close()


# using in endpoints
@app.get('/getdata')
async def get_data():
    try:
        async with session.get('http://example/getdata') as response:
            return await response.json()
    except aiohttp.ClientError as e:
        logging.error(e)
    except asyncio.TimeoutError as e:
        logging.error(e)