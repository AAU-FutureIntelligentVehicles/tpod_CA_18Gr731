import paramiko
import time
import numpy as np

server = "js1"


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


def process_frame(client, test_nbr):

    put_times = np.array([])
    # txt_times = np.array([])
    haralick_times = np.array([])
    get_times = np.array([])
    total_times = np.array([])

    sftp = client.open_sftp()
    print "ssh running...\n\n"

    i = 0
    while i < test_nbr:
        stdin, stdout, stderr = client.exec_command('bash')
        t1 = time.time()
        sftp.put("/Users/reiserbalazs/Desktop/Project/pictures/picture0.png", "/dev/shm/breise18/testy.png")
        t2 = time.time()
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
        sftp.get("/dev/shm/breise18/features.npy", "/Users/reiserbalazs/Desktop/Project/calculated_features/features.npy")
        t5 = time.time()

        put_times = np.append(put_times, t2 - t1)
        # txt_times = np.append(txt_times, t3 - t2)
        haralick_times = np.append(haralick_times, t4 - t3)
        get_times = np.append(get_times, t5 - t4)
        total_times = np.append(total_times, t5 - t1)
        i = i + 1
        print "Number of recieved features: ", i

    stdin, stdout, stderr = client.exec_command('bash')
    stdin.write("touch /dev/shm/breise18/end.txt \n")
    stdin.flush()
    stdin.write("touch /dev/shm/breise18/flag.txt \n")
    stdin.flush()
    sftp.close()

    np.save(server + "p.npy", put_times)
    # np.save("js4t.npy", txt_times)
    np.save(server + "h.npy", haralick_times)
    np.save(server + "g.npy", get_times)
    np.save(server + "total.npy", total_times)

    print "PUT\n", put_times, "\n\n"
    # print "TXT\n", txt_times, "\n\n"
    print "HARALICK\n", haralick_times, "\n\n"
    print "GET\n", get_times, "\n\n"
    print "TOTAL\n", total_times, "\n\n"


ssh = createSSHClient(server + ".es.aau.dk", 22, "breise18", "")
process_frame(ssh, 100)
