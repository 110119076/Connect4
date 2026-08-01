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