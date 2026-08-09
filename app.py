#!/usr/bin/env python

import secrets
import asyncio

from websockets.asyncio.server import serve
from websockets.asyncio.connection import broadcast

import json

from connect4 import PLAYER1, PLAYER2, Connect4

import secrets

JOIN = {}

async def start(websocket):
    game = Connect4()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    try:
        event = {"type": "init", "join": join_key}
        await websocket.send(json.dumps(event))
        print("First player started game", id(game))
        await play(websocket, game, PLAYER1, connected)
    finally:
        del JOIN[join_key]

async def error(websocket, message):
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))

async def join(websocket, join_key):
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return
    connected.add(websocket)
    try:
        print("Second player joined game", id(game))
        await play(websocket, game, PLAYER2, connected)
    finally:
        connected.remove(websocket)

async def play(websocket, game, player, connected):
    async for message in websocket:
        event = json.loads(message)
        print(event)
        assert event["type"] == "play"
        column = event["column"]
        try:
            row = game.play(player, column)
            event = {
                "type": "play",
                "player": player,
                "column": column,
                "row": row,
            }
            
            # for connection in connected:
            #     await connection.send(json.dumps(event))

            broadcast(connected, json.dumps(event))
            
            if (game.winner is not None):
                event = {
                    "type": "win",
                    "player": game.winner
                }
                
                # for connection in connected:
                #     await connection.send(json.dumps(event))

                broadcast(connected, json.dumps(event))

        except Exception as ex:
            await error(websocket, str(ex))
            continue
        

async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"
    if ("join" in event):
        await join(websocket, event["join"])
    else:
        await start(websocket)

async def main():
    server = await serve(handler, "", 8001) # Starts a websocket server
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())