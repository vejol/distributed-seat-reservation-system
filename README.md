# Distributed Seat Reservation System

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
