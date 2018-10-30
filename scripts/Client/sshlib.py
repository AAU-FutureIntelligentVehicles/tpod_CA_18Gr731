import paramiko
import time


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


def put2server(client, src, dst):
    sftp = client.open_sftp()
    sftp.put(src, dst)


def get_from_server(client, src, dst):
    sftp = client.open_sftp()
    sftp.get(src, dst)


def img2features(client):
    sftp = client.open_sftp()
    stdin, stdout, stderr = client.exec_command('bash')

    t1 = time.time()
    sftp.put("/Users/reiserbalazs/Desktop/Project/pictures/picture0.png", "/dev/shm/breise18/testy.png")
    t2 = time.time()
    print "Image transferring time:                ", t2 - t1

    stdin.write("touch /dev/shm/breise18/flag.txt \n")
    stdin.flush()

    t3 = time.time()
    while True:
        stdin.write("ls /dev/shm/breise18/ \n")
        stdin.flush()
        recieved = stdout.channel.recv(2048).split()
        if not (b'flag.txt' in recieved):
            break
    stdin.write("exit\n")
    stdin.flush()
    t4 = time.time()
    print "Processing time of feature computation: ", t4 - t3

    t5 = time.time()
    sftp.get("/dev/shm/breise18/features.npy", "/Users/reiserbalazs/Desktop/Project/calculated_features/features.npy")
    t6 = time.time()
    print "Feature downloading time :              ", t6 - t5

    print "TOTAL Transfering and Computing Time:   ", t6 - t1

    stdin, stdout, stderr = client.exec_command('bash')
    stdin.write("touch /dev/shm/breise18/end.txt \n")
    stdin.flush()
    stdin.write("touch /dev/shm/breise18/flag.txt \n")
    stdin.flush()
    sftp.close()
