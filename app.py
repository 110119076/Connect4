#!/usr/bin/env python

import secrets
import asyncio

from websockets.asyncio.server import serve

import json

from connect4 import PLAYER1, PLAYER2, Connect4

import secrets

JOIN = {}

# async def handler(websocket):
#     game = Connect4()
#     curr_player = PLAYER1
#     async for message in websocket:
#         event = json.loads(message)
#         is_play = event["type"] == "play"
#         if is_play:
#             column = event["column"]
#         try:
#             row = game.play(curr_player, column)
#         except Exception as ex:
#             event = {
#                 "type": "error",
#                 "message": str(ex),
#             }
#             await websocket.send(json.dumps(event))
#             continue
#         if (not game.winner):
#             event = {
#                 "type": "play",
#                 "player": curr_player,
#                 "column": column,
#                 "row": row,
#             }
#             await websocket.send(json.dumps(event))
#             await asyncio.sleep(0.3)
#             last_player = game.last_player
#             curr_player = PLAYER2 if last_player==PLAYER1 else PLAYER1
#         else:
#             event = {
#                 "type": "play",
#                 "player": curr_player,
#                 "column": column,
#                 "row": row,
#             }
#             await websocket.send(json.dumps(event))
#             await asyncio.sleep(0.3)
#             event = {
#                 "type": "win",
#                 "player": game.winner,
#             }
#             await websocket.send(json.dumps(event))

async def start(websocket):
    game = Connect4()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    try:
        event = {"type": "init", "join": join_key}
        await websocket.send(json.dumps(event))
        print("First player started game", id(game))
        async for message in websocket:
            print("First player sent", message)
    finally:
        del JOIN[join_key]

async def handler(websocket):
    async for message in websocket:
        event = json.loads(message)
        assert event["type"] == "init"
        await start(websocket)

async def main():
    server = await serve(handler, "", 8001) # Starts a websocket server
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())