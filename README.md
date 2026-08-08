# Connect4
Learning Websockets via Connect4

Added a venv

Added a .gitignore file

Adding requirements.txt for all the required packages/libraries

Observations:

Whenever we interrupt the client using Ctrl + C or Ctrl + D, the server also breaks apart. And you see a websockets.exceptions.ConnectionClosedOK exception from the server side.

Any code change in the server (app.py) requires a restart of the server.

The WebSocket server loads the Python code in app.py then serves every WebSocket request with this version of the code. As a consequence, changes to app.py aren’t visible until you restart the server.

Note: It is possible to restart the WebSocket server automatically.

The ConnectionClosedOK exception doesn’t appear anymore after properly handled in the server.

Websockets provides a shortcut for iterating over messages received on the connection until the client disconnects instead of manually handling the ConnectionClosedOK exception.

Until now we connected from websocket client to server, we now connect from browser to the server.

Before you exchange messages with the server, you need to decide their format. Let's use JSON.

sendMoves() registers a listener for click events on the board. The listener figures out which column was clicked, builds a event of type "play", serializes it, and sends it to the server.

Thus we successfully transmitted from browser to server

Now let's transmit from server to browser back.

In JavaScript, you receive WebSocket messages by listening to message events.

You’re going to need three types of messages from the server to the browser:

{type: "play", player: "red", column: 3, row: 0}

{type: "win", player: "red"}

{type: "error", message: "This slot is full."}

## Summary

In this first part of the tutorial, you learned how to:

build and run a WebSocket server in Python with serve();

receive a message in a connection handler with recv();

send a message in a connection handler with send();

iterate over incoming messages with async for message in websocket: ...;

open a WebSocket connection in JavaScript with the WebSocket API;

send messages in a browser with WebSocket.send();

receive messages in a browser by listening to message events;

design a set of events to be exchanged between the browser and the server.

You can now play a Connect Four game in a browser, communicating over a WebSocket connection with a server where the game logic resides!

However, the two players share a browser, so the constraint of being in the same room still applies.

Move on to the second part of the tutorial to break this constraint and play from separate browsers.

### Route & Broadcast

Open two WebSocket connections from two separate browsers, one for each player, to the same server in order to play the same game

This requires moving the state of the game to a place where both connections can access it.

As long as you’re running a single server process, you can share state by storing it in a global variable.

For multi server process => Pub / Sub mechanism

How can you make two connection handlers agree on which game they’re playing?

When the first player starts a game, you give it an identifier.

Then, you communicate the identifier to the second player.

When the second player joins the game, you look it up with the identifier.

Note: Keep track of the WebSocket connections of the two players.

A module-level dict enables lookups by identifier: JOIN = {}

When the first player starts the game, initialize and store it. When the second player joins the game, look it up and register to receive moves from the same game.

In both connection handlers, you have a game pointing to the same Connect4 instance, so you can interact with the game, and a connected set of connections, so you can send game events to both players as follows:

for connection in connected:

        await connection.send(json.dumps(event))


Perhaps you spotted a major piece missing from the puzzle. How does the second player obtain join_key? Let’s design new events to carry this information.

To start a game, the first player sends an "init" event

{type: "init"}

The connection handler for the first player creates a game and responds with join key

With this information, the user interface of the first player can create a link to http://localhost:8000/?join=<join_key>. 

To join the game, the second player sends a different "init" event

{type: "init", join: "<join_key>"}

The connection handler for the second player can look up the game with the join key as shown above.

Define a function to send an initialization event when the WebSocket connection is established, which triggers an open event

Update the initialization sequence to account for the second player.

Update the handler coroutine to look for the join key in the "init" message, then load that game

The server logs say first player started game ... and second player joined game .... The numbers match, proving that the game local variable in both connection handlers points to same object in the memory of the Python process.

In the initialization sequence, you’re routing connections to start() or join() depending on the first message received by the server.