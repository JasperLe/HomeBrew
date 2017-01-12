import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

counter = 0
t = [0]
data = [1,2,3,4,5,6,7,8,9,4,5,6,5,4,1]
price = [data[1]]


def animate(i):
    global t, counter
    x = t
    y = price
    counter += 1
    x.append(counter)
    y.append(data[counter])
    ax1.clear()
    plt.plot(x, y, color="blue")


ani = animation.FuncAnimation(fig, animate, interval=50)
plt.show()