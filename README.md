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
