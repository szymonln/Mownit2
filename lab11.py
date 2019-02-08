import socket
from struct import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate.quadrature import tupleset


def simpson(y, x, dx=1, axis=-1):
    nd = len(y.shape)

    N = y.shape[axis]
    start = 0
    stop = N-2
    step = 2

    slice_all = (slice(None),)*nd
    slice0 = tupleset(slice_all, axis, slice(start, stop, step))
    slice1 = tupleset(slice_all, axis, slice(start+1, stop+1, step))
    slice2 = tupleset(slice_all, axis, slice(start+2, stop+2, step))

    if x is None:
        result = np.sum(dx/3.0 * (y[slice0]+4*y[slice1]+y[slice2]), axis=axis)
    else:
        h = np.diff(x, axis=axis)
        sl0 = tupleset(slice_all, axis, slice(start, stop, step))
        sl1 = tupleset(slice_all, axis, slice(start+1, stop+1, step))
        h0 = h[sl0]
        h1 = h[sl1]
        hsum = h0 + h1
        hprod = h0 * h1
        h0divh1 = h0 / h1
        tmp = hsum/6.0 * (y[slice0]*(2-1.0/h0divh1) +
                          y[slice1]*hsum*hsum/hprod +
                          y[slice2]*(2-h0divh1))
        result = np.sum(tmp, axis=axis)
    return result

UDP_IP = "192.168.43.248"
UDP_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))
print("CONNECTED to {}".format(UDP_IP))

ticks = np.array([], dtype=np.float)

xs = np.array([], dtype=np.float)
ys = np.array([], dtype=np.float)
zs = np.array([], dtype=np.float)

xspd = np.array([], dtype=np.float)
yspd = np.array([], dtype=np.float)
zspd = np.array([], dtype=np.float)
xspd = np.append(xspd, np.float(0))
yspd = np.append(yspd, np.float(0))
zspd = np.append(zspd, np.float(0))

xrd = np.array([], dtype=np.float)
yrd = np.array([], dtype=np.float)
zrd = np.array([], dtype=np.float)
xrd = np.append(xrd, np.float(0))
yrd = np.append(yrd, np.float(0))
zrd = np.append(zrd, np.float(0))

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

tick_count = np.float(0)
it = 0

while True:
    tick_count += 1.0
    plt.cla()
    data = sock.recv(1024)
    x = unpack_from ('!f', data, 0)
    y = unpack_from ('!f', data, 4)
    z = unpack_from('!f', data, 8)
    xs = np.append(xs, x[0])
    ys = np.append(ys, y[0])
    zs = np.append(zs, z[0])
    ticks = np.append(ticks, 1*tick_count)


    # Rysowanie wykresu drogi 3D
    if it > 40:
        # Wektory prędkości
        xspd = np.append(xspd, xspd[-1] + simpson(xs[-5:-1], ticks[-5:-1]))
        yspd = np.append(yspd, yspd[-1] + simpson(ys[-5:-1], ticks[-5:-1]))
        zspd = np.append(zspd, zspd[-1] + simpson(zs[-5:-1], ticks[-5:-1]))

        # Korzystam z własności całek nieoznaczonych
        if it > 45 and it % 3 == 0:
            xrd = np.append(xrd, xrd[-1] + simpson(xspd[-5:-1], ticks[-5:-1]))
            yrd = np.append(yrd, yrd[-1] + simpson(yspd[-5:-1], ticks[-5:-1]))
            zrd = np.append(zrd, zrd[-1] + simpson(zspd[-5:-1], ticks[-5:-1]))

        ax.plot3D(xrd, yrd, zrd)
        plt.draw()
        plt.pause(0.0000001)

    it += 1