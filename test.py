import asyncio
from pathlib import Path
import aiohttp


async def upload_photo(path, name):
    async with aiohttp.ClientSession() as session:
        with open(path, 'rb') as file:
            res = await session.post('http://localhost:5000/photos', data={str(name): file})
            print('done')

async def delete_photo(name):
    async with aiohttp.ClientSession() as session:
        res = await session.delete('http://localhost:5000/photos', json={'name': name})
        print('done')

async def main(num):
    path = Path(__file__).parent / 'image2.jpg'
    await delete_photo('f5bf01c8-7728-4f09-8c8a-d91231d27bb5.jpg')
    # await asyncio.gather(*[upload_photo(path, i) for i in range(num)])

loop = asyncio.get_event_loop()
loop.run_until_complete(main(20))
