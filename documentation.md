
# pymp - Multiplayer Engine Documentation

This document provides a detailed guide to using the **pymp** multiplayer engine. This lightweight framework facilitates multiplayer applications using a client-server architecture built with Python sockets. Below you will find separate sections for both the Server and Client components, outlining their initialization and primary functionalities.

---
<div align='center'>
<h1>Server</h1>
</div>

The **Server** class is responsible for accepting client connections, handling client-specific data, and broadcasting updates. It uses multithreading to manage simultaneous connections.

### Initialization

To create and start the server, initialize the `Server` class with the desired host, port, and maximum number of clients. For example:

```python
server = Server("0.0.0.0", 5555, 2)
```

- **Host:** IP address or hostname where the server will listen.
- **Port:** Port number for client connections.
- **max_clients:** Maximum number of simultaneous client connections.

This constructor sets up the socket, binds it, and starts a daemon thread to accept incoming client connections.

### Methods

#### .wait(n)

The `wait` method pauses the server's execution for a specified number of seconds. Internally, it calls Python’s `time.sleep(n)`. This is useful for introducing delays when necessary.

```python
server.wait(0.1)
```

#### .send_to_clients(message)

The `send_to_clients` function is used to update the server's shared data. You pass in the data (or list of variables) that you want to broadcast to all connected clients:

```python
server.send_to_clients([x, y, ...])
```

- The method updates the internal `serverData` attribute.
- This data is then merged with client-specific variables during the broadcast update process.

#### .data

The `data` attribute holds the aggregated data that has been shared among all clients. It reflects the current state of client variables as updated during each broadcast. You can access this attribute to review the complete state of shared data:

```python
print(server.data)
```

#### .shutdown

The `shutdown` method stops the server and disconnects all clients.

```python
server.shutdown()
```

- Closes the server socket to stop listening for new connections.
- Iterates through all connected clients and disconnects them.
- Stops the internal `accept_clients` thread.
- Prints a shutdown confirmation message.

---

<div align='center'>
<h1>Client</h1>
</div>

The **Client** class manages the connection to the server and handles real-time data updates sent by the server.

### Initialization

To create a new client instance, simply initialize the `Client` class:

```python
client = Client()
```

This creates a client object that is ready to connect to a server.

### Methods

#### .connect(host, port)

The `connect` method establishes a connection with the server using the specified host and port. It also starts a daemon listener thread to receive updates from the server:

```python
client.connect("localhost", 5555)
```

- Once connected, the server sends an initialization message assigning a unique `client_id`.

#### .client_id

After the connection is established, the server sends an "init" message to the client, which sets the `client_id` attribute. This unique identifier distinguishes the client from others:

```python
print(client.client_id)
```

#### .send_variables(variables)

The `send_variables` method allows the client to send a dictionary of variables (such as game state data) to the server. For example:

```python
client.send_variables({
    "player_y": player.body.y,
    "player_x": player.body.x,
    # ... additional variables
})
```

- These variables represent the client’s state and are broadcast by the server to other connected clients.

#### .data

The `data` attribute on the client stores the aggregated data received from the server. This includes the variables from all other connected clients (excluding the current client's own data):

```python
print(client.data)
```

- This makes it easy to keep track of the state of other players or objects in the multiplayer environment.



#### .disconnect

The `disconnect` method safely disconnects the client from the server:

```python
client.disconnect()
```

- Closes the client socket to stop communication with the server.
- Ends the listener thread that receives updates from the server.
- Prints a confirmation message upon disconnection.

---

## Summary

- **Server:**  
  - **Initialization:** `Server("0.0.0.0", 5555, 2)` starts the server.
  - **wait(n):** Introduces a delay of `n` seconds.
  - **send_to_clients(message):** Updates the shared server data.
  - **data:** Holds the current shared state from all clients.
  - **shutdown():** Stops the server and disconnects all clients.

- **Client:**  
  - **Initialization:** `Client()` creates a new client instance.
  - **connect(host, port):** Connects to the server.
  - **client_id:** Returns the unique client identifier.
  - **send_variables(variables):** Sends state data (e.g., position coordinates) to the server.
  - **data:** Contains data from other clients, excluding the current client.
  - **disconnect()**: Safely disconnects the client from the server.

This structure makes it simple to manage and synchronize game state across multiple devices, forming the backbone of the multiplayer experience provided by **pymp**.
