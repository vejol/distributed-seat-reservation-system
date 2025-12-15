# Distributed Seat Reservation System

## Table of Contents

- [How to Run the Raft Nodes Locally](#how-to-run-the-raft-nodes-locally)
  - [1. Install Python](#1-install-python)
  - [2. Clone the Repository](#2-clone-the-repository)
  - [3. Set Up a Python Virtual Environment](#3-set-up-a-python-virtual-environment)
  - [4. Running the Nodes](#4-running-the-nodes)
    - [Required flag: --id](#required-flag-id)
    - [Optional flag: --config](#optional-flag-config)
- [Dynamically Changing the Raft Configuration](#dynamically-changing-the-raft-configuration)
  - [Adding a Node](#adding-a-node)
  - [Removing a Node](#removing-a-node)

## How to Run the Raft Nodes Locally

This project includes a simple distributed seat reservation system implemented with the
[PySyncObj](https://github.com/bakwc/PySyncObj) library.  
Each instance acts as a Raft node that participates in leader election and state replication.

Below are the steps for running three Raft nodes locally on your machine.

---

## 1. Install Python

1. Make sure you have **Python 3.10.12** installed.
   - Other Python 3.x versions may also work, but the application has been tested specifically with 3.10.12.
   - Check your Python version using:  
     `python --version` or `python3 --version`

---

## 2. Clone the Repository

1. Clone this repository to your local machine.
   - If you are a collaborator, you can use SSH:  
     `git clone git@github.com:vejol/distributed-seat-reservation-system.git`
2. Move into the project directory:  
   `cd distributed-seat-reservation-system`

---

## 3. Set Up a Python Virtual Environment

1. Create a virtual environment:  
   `python3 -m venv raft-node/venv`
   - A virtual environment keeps the project's dependencies isolated from global packages.
2. Activate the environment:  
   `source raft-node/venv/bin/activate`
3. Install the dependencies:
   `pip install -r raft-node/requirements.txt`

---

## 4. Running the Nodes

To run three nodes with a shared replicated state:

1. Open **three separate terminal windows**.
2. In each terminal, navigate to the cloned repository and activate the virtual environment with `source raft-node/venv/bin/activate`
3. Start `main.py` in each terminal with a different node ID:

   - Terminal 1:  
     `python3 raft-node/main.py --id 0`
   - Terminal 2:  
     `python3 raft-node/main.py --id 1`
   - Terminal 3:  
     `python3 raft-node/main.py --id 2`

### Required flag: `--id`

The `--id` flag is **mandatory**. It tells the program which node this process represents.  
The value corresponds to the index of the node in the `config.json` file.

### Optional flag: `--config`

The `--config` flag is **optional**.  
If omitted, the program uses the configuration profile under the `"default"` key in `config.json`.

The `config.json` file may contain multiple profiles (e.g. `"default"`, `"localhost"`, `"docker"`, `"production"`).  
You can choose a profile by passing its name via `--config`:

Example:

- Terminal 1:
  `python3 raft-node/main.py --id 0 --config staging`
- etc.

## Dynamically Changing the Raft Configuration

The application supports dynamic Raft configuration changes, meaning nodes can be added or removed at runtime. Our implementation leverages the existing PySyncObj methods `addNodeToCluster` and `removeNodeFromCluster`.

### Adding a Node

Adding a new node is done via the `add-node` command in `console.py`. The command prompts for the new node’s address (host:port). The console then attempts to add the node to the configuration and waits for the operation to complete. The result is printed once available, and the operation has a 60-second timeout.

For example, to add a fourth node to the default three-node configuration running on localhost:

1. Start the nodes normally:

   - python3 ./raft-node/main.py --id 0
   - python3 ./raft-node/main.py --id 1
   - python3 ./raft-node/main.py --id 2

2. Modify `config.json` to reflect the new configuration by adding the new node’s address. The updated `config.json` might look like:

   ```json
   {
     "default": [
       "localhost:6000",
       "localhost:6001",
       "localhost:6002",
       "localhost:6003"
     ]
   }
   ```

3. Run the `add-node` command in any console.

4. When prompted, enter the new node’s address in the form `localhost:6003`.

5. Start the new node in a separate console:

   - python3 ./raft-node/main.py --id 3

### Removing a Node

To remove an existing node, use the `remove-node` command in `console.py`. The console prompts for the node’s address (host:port), submits the configuration change, and waits for the result (15-second timeout).

Example: removing `localhost:6003` from a four-node cluster:

1. Run the `remove-node` command in any console.
2. When prompted, enter `localhost:6003`.
3. Wait for the success message or an error/timeout.
4. Stop the removed node’s process (e.g., press Ctrl+C in its terminal).
5. Update `config.json` to reflect the new configuration by removing the node’s address. For example:

   ```json
   {
     "default": ["localhost:6000", "localhost:6001", "localhost:6002"]
   }
   ```
