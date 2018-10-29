import numpy as np
from matplotlib import pyplot as plt

x = np.arange(100)

js1_put = np.load("js1p.npy")
js1_txt = np.load("js1t.npy")
js1_haralick = np.load("js1h.npy")
js1_get = np.load("js1g.npy")
js1_total = np.load("js1total.npy")

js3_put = np.load("js3p.npy")
js3_txt = np.load("js3t.npy")
js3_haralick = np.load("js3h.npy")
js3_get = np.load("js3g.npy")
js3_total = np.load("js3total.npy")

js4_put = np.load("js4p.npy")
js4_txt = np.load("js4t.npy")
js4_haralick = np.load("js4h.npy")
js4_get = np.load("js4g.npy")
js4_total = np.load("js4total.npy")


plt.plot(x, js1_put, 'r', label="JS1")
plt.plot(x, js3_put, 'g', label="JS3")
plt.plot(x, js4_put, 'b', label="JS4")
plt.ylabel('sec')
plt.legend(loc='upper left')
plt.title("Image transfer to server")
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
plt.title("Feature computation time in server")
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
print "JS1 TXT AVG:", np.average(js1_txt)
print "JS1 HARALICK AVG:", np.average(js1_haralick)
print "JS1 GET AVG:", np.average(js1_get)
print "JS1 TOTAK AVG:", np.average(js1_total), "\n"

print "JS3 PUT AVG:", np.average(js3_put)
print "JS3 TXT AVG:", np.average(js3_txt)
print "JS3 HARALICK AVG:", np.average(js3_haralick)
print "JS3 GET AVG:", np.average(js3_get)
print "JS3 TOTAL AVG:", np.average(js3_total), "\n"

print "JS4 PUT AVG:", np.average(js4_put)
print "JS4 TXT AVG:", np.average(js4_txt)
print "JS4 HARALICK AVG:", np.average(js4_haralick)
print "JS4 GET AVG:", np.average(js4_get)
print "JS4 TOTAL AVG:", np.average(js4_total)
