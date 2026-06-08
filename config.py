import os
os.environ["NO_PROXY"] = "*"
import json
def load_servers():
    servers_env = os.getenv("SERVERS")
    if servers_env:
        servers = servers_env.split(",")
        print(f"{len(servers)} servers from ENV")
        return servers

    try:
        with open("config.json", "r") as file:
            data = json.load(file)
            servers = data.get("servers", [])
            print(f"Loaded {len(servers)} servers from file")
            return servers
    except FileNotFoundError:
        raise Exception("No SERVERS env or config.json found")