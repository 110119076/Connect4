#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve

import json

from connect4 import PLAYER1, PLAYER2, Connect4

async def handler(websocket):
    game = Connect4()
    curr_player = PLAYER1
    async for message in websocket:
        event = json.loads(message)
        game.play(curr_player, event["column"])
        last_player = game.last_player
        curr_player = PLAYER2 if last_player==PLAYER1 else PLAYER1
        for player, column, row in game.moves:
            if (not game.winner):
                event = {
                    "type": "play",
                    "player": player,
                    "column": column,
                    "row": row,
                }
                await websocket.send(json.dumps(event))
                await asyncio.sleep(0.1)
            else:
                event = {
                    "type": "win",
                    "player": game.winner,
                }
                await websocket.send(json.dumps(event))

async def main():
    server = await serve(handler, "", 8001) # Starts a websocket server
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())