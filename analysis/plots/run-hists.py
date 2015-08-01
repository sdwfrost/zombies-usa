import numpy as np
import scipy as sp
from matplotlib.widgets import Slider
from matplotlib.colors import Normalize
from matplotlib import cm
import matplotlib.pyplot as pl

sizes = np.array([64,128,256,512,1024,2048])
data = np.array([np.loadtxt("./raw-%i.txt" % i) for i in sizes])
dev = np.array([91./48+d.mean() for d in data])
std = np.array([d.std() for d in data])

colors = cm.copper(Normalize()(np.arange(len(dev))))

x,y = [],[]
for t in data:
    ty, tx = np.histogram(t, bins=30, normed=True)
    x.append((tx[:1]+tx[:-1])/2)
    y.append(ty)
x = np.array(x).T
y = np.array(y).T

def rescale(sizes, xs, ys, dfc, tau):
    return (xs+dfc)*sizes**tau, ys*sizes**-tau

def plotall():
    fig = pl.figure(1)
    for s,tx,ty,tc in zip(sizes,x.T,y.T,colors):
        pl.plot(tx, ty, 'o-', lw=2, c=tc, label=str(s))
    pl.xlabel(r"$d_f$")
    pl.ylabel(r"$P(d_f)$")
    pl.legend(loc='lower right', prop={"size": 20})

    ox, oy = rescale(sizes, x, y, dfc=91./48, tau=0.29)
    ax = fig.add_axes([0.58, 0.58, 0.30, 0.30])
    for tx,ty,c in zip(ox.T, oy.T, colors):
        ax.loglog(tx, ty, 'o-', lw=2, c=c)
    ax.set_xlim(0.33, 2.15)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(r"$(d_f - d_f^{\infty}) / L^{\sigma}$", fontsize=20)
    ax.set_ylabel(r"$L^{-\sigma}P(d_f)$", fontsize=20)

def slider_plot(sizes, xs, ys, dfc=91./48, tau=0.25):
    fig = pl.figure(2)
    pl.subplots_adjust(left=0.25, bottom=0.25)
    pl.clf()

    lines = []
    ox, oy = rescale(sizes, xs, ys, dfc, tau)
    for x,y,c in zip(ox.T, oy.T, colors):
        lines.append(pl.loglog(x, y, 'o-', c=c)[0])

    axcolor = 'white'
    axalpha = pl.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
    axtau = pl.axes([0.25, 0.20, 0.65, 0.03], axisbg=axcolor)

    print dfc, tau
    salpha = Slider(axalpha, r"$d_f$", 1.5, 2.0, valinit=dfc)
    stau = Slider(axtau, r"$\tau$", -1.0, 2.0, valinit=tau)

    def update(val):
        dfc = salpha.val
        tau = stau.val
        print "dfc =", dfc, 'tau = ', tau

        ox, oy = rescale(sizes, xs, ys, dfc, tau)
        for line,x,y in zip(lines, ox.T, oy.T):
            line.set_xdata(x)
            line.set_ydata(y)

            fig.canvas.draw_idle()

    salpha.on_changed(update)
    stau.on_changed(update)
