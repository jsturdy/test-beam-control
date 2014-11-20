import matplotlib.pyplot as plt

plt.ion()

def graph(data, xmin = 0, xmax = 0, ymin = 0, ymax = 0):
    plt.plot(data)
    if (xmin != 0 or xmax != 0 or ymin != 0 or ymax != 0):
        plt.axis([xmin, xmax, ymin, ymax])
    plt.draw()
    plt.clf()
