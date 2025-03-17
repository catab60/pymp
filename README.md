# pymp - Multiplayer Engine

![multiplayer](https://raw.githubusercontent.com/catab60/pymp/refs/heads/main/logopymp.png)

An awesome project developed in **3 days** to help me learn about **sockets** and how computers talk to each other. This universal multiplayer engine supports gameplay across multiple devices using pure Python.



## About the Project

This engine is a lightweight framework for building multiplayer applications. It uses a simple client-server setup where you can run a dedicated server, but port forwarding is required for external connections. The project also includes a multiplayer Pong demo built with the `pymp.py` library.

## Installation Guide


1. **Download `pymp.py`:**  
   Add the `pymp.py` file to your project directory.

2. **Import the Library in Your Code:**

   ```python
   # For the client side:
   from pymp import Client
   
   # For the dedicated server:
   from pymp import Server
   ```


## Documentation

For detailed documentation, please refer to [documentation.md](documentation.md).

## Demo Play Guide

The repository includes a demo for a multiplayer Pong game. To play the demo:

1. **Run the Dedicated Server:**

   Open a command prompt and type:

   ```bash
   python pong_server.py
   ```

2. **Start the Clients:**

   In two separate command prompt windows, run:

   ```bash
   python pong.py
   ```

   - **Local Testing:** Run both clients on the same computer to see how it works.
   - **Online Multiplayer:** For playing with a friend over the internet, ensure you set up port forwarding and adjust the IP and port in `pong.py`.
