#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve

async def handler(websocket):
    async for message in websocket:
        print(message)


async def main():
    server = await serve(handler, "", 8001) # Starts a websocket server
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())