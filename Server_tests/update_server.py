import paramiko

server = "js3.es.aau.dk"
user = "breise18"
password = ""

source = "/Users/reiserbalazs/Documents/GitHub/tpod_CA_18Gr731/server/feature_computation.py"
destination = "/dev/shm/breise18/feature_computation.py"
source2 = "/Users/reiserbalazs/Documents/GitHub/tpod_CA_18Gr731/server/haralicklib.py"
destination2 = "/dev/shm/breise18/haralicklib.py"


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


def copy_file(hostname, port, username, password, src, dst):
    ssh = createSSHClient(hostname, port, username, password)
    sftp = ssh.open_sftp()
    sftp.put(src, dst)
    print(src + ' >>> ' + dst)
    print
    sftp.close()
    ssh.close()


copy_file(server, 22, user, password, source, destination)
copy_file(server, 22, user, password, source2, destination2)

