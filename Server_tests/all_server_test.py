import paramiko
import time
import numpy as np
from matplotlib import pyplot as plt

server1 = "js1"
server3 = "js3"
server4 = "js4"
user = ""
password = ""

number_of_test = 100


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


def process_frame(client, server, test_nbr):

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


ssh1 = createSSHClient(server1 + ".es.aau.dk", 22, user, password)
ssh3 = createSSHClient(server3 + ".es.aau.dk", 22, user, password)
ssh4 = createSSHClient(server4 + ".es.aau.dk", 22, user, password)

process_frame(ssh1, server1, number_of_test)
process_frame(ssh3, server3, number_of_test)
process_frame(ssh4, server4, number_of_test)

x = np.arange(100)

js1_put = np.load("js1p.npy")
# js1_txt = np.load("js1t.npy")
js1_haralick = np.load("js1h.npy")
js1_get = np.load("js1g.npy")
js1_total = np.load("js1total.npy")

js3_put = np.load("js3p.npy")
# js3_txt = np.load("js3t.npy")
js3_haralick = np.load("js3h.npy")
js3_get = np.load("js3g.npy")
js3_total = np.load("js3total.npy")

js4_put = np.load("js4p.npy")
# js4_txt = np.load("js4t.npy")
js4_haralick = np.load("js4h.npy")
js4_get = np.load("js4g.npy")
js4_total = np.load("js4total.npy")


plt.plot(x, js1_put, 'r', label="JS1")
plt.plot(x, js3_put, 'g', label="JS3")
plt.plot(x, js4_put, 'b', label="JS4")
plt.ylabel('sec')
plt.legend(loc='upper left')
plt.title("Image transfer time to server")
plt.show()

plt.plot(x, js1_get, 'r', label="JS1")
plt.plot(x, js3_get, 'g', label="JS3")
plt.plot(x, js4_get, 'b', label="JS4")
plt.ylabel('sec')
plt.legend(loc='upper left')
plt.title("Get features from server")
plt.show()

plt.plot(x, js1_haralick, 'r', label="JS1")
plt.plot(x, js3_haralick, 'g', label="JS3")
plt.plot(x, js4_haralick, 'b', label="JS4")
plt.ylabel('sec')
plt.legend(loc='upper left')
plt.title("Haralick feature processing time in server")
plt.show()

plt.plot(x, js1_total, 'r', label="JS1")
plt.plot(x, js3_total, 'g', label="JS3")
plt.plot(x, js4_total, 'b', label="JS4")
plt.ylabel('sec')
plt.legend(loc='upper left')
plt.title("Total feature calculation time with file transfers")
plt.show()


plt.plot(x, js1_put, 'r', label="JS1 put image")
plt.plot(x, js1_haralick, 'r', label="JS1 compute haralick")
plt.plot(x, js1_get, 'y', label="JS1 get features")
plt.plot(x, js1_total, 'k', label="JS1 total")
plt.ylabel('sec')
plt.legend(loc='upper right')
plt.title("JS1 calculation times")
plt.show()

plt.plot(x, js3_put, 'r', label="JS3 put image")
plt.plot(x, js3_haralick, 'r', label="JS3 compute haralick")
plt.plot(x, js3_get, 'y', label="JS3 get features")
plt.plot(x, js3_total, 'k', label="JS3 total")
plt.ylabel('sec')
plt.legend(loc='upper right')
plt.title("JS3 calculation times")
plt.show()

plt.plot(x, js4_put, 'r', label="JS4 put image")
plt.plot(x, js4_haralick, 'r', label="JS4 compute haralick")
plt.plot(x, js4_get, 'y', label="JS4 get features")
plt.plot(x, js4_total, 'k', label="JS4 total")
plt.ylabel('sec')
plt.legend(loc='upper right')
plt.title("JS4 calculation times")
plt.show()


print "JS1 PUT AVG:", np.average(js1_put)
# print "JS1 TXT AVG:", np.average(js1_txt)
print "JS1 HARALICK AVG:", np.average(js1_haralick)
print "JS1 GET AVG:", np.average(js1_get)
print "JS1 TOTAK AVG:", np.average(js1_total), "\n"

print "JS3 PUT AVG:", np.average(js3_put)
# print "JS3 TXT AVG:", np.average(js3_txt)
print "JS3 HARALICK AVG:", np.average(js3_haralick)
print "JS3 GET AVG:", np.average(js3_get)
print "JS3 TOTAL AVG:", np.average(js3_total), "\n"

print "JS4 PUT AVG:", np.average(js4_put)
# print "JS4 TXT AVG:", np.average(js4_txt)
print "JS4 HARALICK AVG:", np.average(js4_haralick)
print "JS4 GET AVG:", np.average(js4_get)
print "JS4 TOTAL AVG:", np.average(js4_total)