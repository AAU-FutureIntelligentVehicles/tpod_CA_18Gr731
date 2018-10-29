import paramiko
import time


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def process_frame(client, test_nbr):
    sftp = client.open_sftp()
    # print("Computing Haralick Features... ")
    i = 0
    while i < test_nbr:
        stdin, stdout, stderr = client.exec_command('bash')
        t1 = time.time()
        sftp.put("/Users/reiserbalazs/Desktop/Project/pictures/picture{0}.png".format(i), "/dev/shm/breise18/testy.png")
        #sftp.put("/Users/reiserbalazs/Desktop/Project/1.txt", "/dev/shm/breise18/1.txt")
        t2 = time.time()
        print('Transfer time {0}: '.format(i), t2 - t1)
        t2 = time.time()
        stdin.write("touch /dev/shm/breise18/1.txt \n")
        stdin.flush()
        t22 = time.time()
        print('Create 1.txt {0}: '.format(i), t22 - t2)
        t2 = time.time()
        while True:
            stdin.write("ls /dev/shm/breise18/ \n")
            stdin.flush()
            # print('Im in while loop')
            recieved = stdout.channel.recv(2048).split()
            # print(recieved)

            if not (b'1.txt' in recieved):
                break
        stdin.write("exit\n")
        stdin.flush()
        t3 = time.time()
        print('Processing time {0}: '.format(i), t3 - t2)
        t3 = time.time()
        sftp.get("/dev/shm/breise18/features.npy".format(i), "/Users/reiserbalazs/Desktop/Project/calculated_features/features{0}.npy".format(i))
        t4 = time.time()
        print('Download time {0}: '.format(i), t4 - t3)
        t5 = time.time()
        print("TOTAL Transfering and Computing Time {0}: ".format(i), t5 - t1)
        i = i+1
    stdin, stdout, stderr = client.exec_command('bash')
    stdin.write("touch /dev/shm/breise18/end.txt \n")
    stdin.flush()
    stdin.write("touch /dev/shm/breise18/1.txt \n")
    stdin.flush()
    sftp.close()


ssh = createSSHClient("js4.es.aau.dk", 22, "breise18", "")
process_frame(ssh, 2)
