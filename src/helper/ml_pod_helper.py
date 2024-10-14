import runpod
import os

# Set your API key
runpod.api_key = "6MRIL8BDMAUTBIMX6JGVOGJCMGR32PYXI7MHR229"

# Get all pods
pods = runpod.get_pods()


# Print the ID of each pod

def get_address():
    """This function fetch runpod ip address """
    add = ""
    for pod in pods:
        if 'runtime' in pod and pod['runtime']:
            for port in pod['runtime']['ports']:
                if port['privatePort'] == 8002:
                    add = f"{port['ip']}:{port['publicPort']}"
    if add != "":
        return add
    else:
        return False


