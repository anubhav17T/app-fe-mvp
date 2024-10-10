import runpod

runpod.api_key = "6MRIL8BDMAUTBIMX6JGVOGJCMGR32PYXI7MHR229"

# Get all pods
pods = runpod.get_pods()
print(pods)


def machine_learning_pod():
    """This function fetch runpod ip address """
    add = ""
    for pod in pods:
        for port in pod['runtime']['ports']:
            if port['privatePort'] == 8002:
                add = f"{port['ip']}:{port['publicPort']}"
    if add != "":
        return add
    else:
        return ""
print(machine_learning_pod())