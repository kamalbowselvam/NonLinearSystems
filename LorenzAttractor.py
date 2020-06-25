import matplotlib, matplotlib.pyplot
import numpy
import types
import mpl_toolkits.mplot3d.axes3d
import matplotlib.animation

def lorenz():
    h = 0.001
    end_time = 10.
    num_steps = int(end_time / h)
 
    sigma = 10.
    beta = 8. / 3.
    rho = 28.
 
    x = numpy.zeros([num_steps + 1, 3])
    y = numpy.zeros([num_steps + 1, 3])
    z = numpy.zeros([num_steps + 1, 3])
    times = h * numpy.array(range(num_steps + 1))
    distance = numpy.zeros([num_steps + 1, 1])
 
    x[0, 0] = 0.
    y[0, 0] = 0.3
    z[0, 0] = 40.
 
    x[0, 1] = 0.
    y[0, 1] = 0.300000000000001
    z[0, 1] = 40.
 
    x[0, 2] = 0.
    y[0, 2] = 0.299999999999999
    z[0, 2] = 40.

    for step in range(num_steps):
      x[step + 1] = x[step] + h * (sigma * (y[step] - x[step]))
      y[step + 1] = y[step] + h * (x[step] * (rho - z[step]) - y[step])
      z[step + 1] = z[step] + h * (x[step] * y[step] - beta * z[step])
      distance[step + 1] = numpy.linalg.norm([x[step, 0] - x[step, 1],y[step, 0] - y[step, 1],z[step, 0] - z[step, 1]])
    return times, distance, x, z, y     

times, distance, x, z, y = lorenz()

def animate_plots(num, x, y, z, plots, cursors, skip):
    for i in range(len(plots)):
        data = numpy.dstack((x[:, i], y[:, i], z[:, i]))[0].transpose()
        plots[i].set_data(data[0:2, :num*skip])
        plots[i].set_3d_properties(data[2, :num*skip])
        cursors[i]._offsets3d = (data[0, num*skip-1:num*skip],
                                 data[1, num*skip-1:num*skip],
                                 data[2, num*skip-1:num*skip])
    return plots

def animation():
 
    fig = matplotlib.pyplot.figure()
    ax = mpl_toolkits.mplot3d.axes3d.Axes3D(fig)
    num_steps, num_plots = x.shape

    colors = ['blue', 'green', 'magenta', 'cyan', 'yellow', 'black']
    markers = ['o', 's', 'p', '*', 'x', '^']
    plots = [ax.plot(x[:, i], y[:, i], z[:, i], c=colors[i % len(colors)])[0] for i in range(num_plots)]
    cursors = [ax.scatter(x[0:1, i], y[0:1, i], z[0:1, i], c=colors[i % len(colors)], marker=markers[i % len(markers)], s=50) for i in range(num_plots)]
 
    # axes labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Lorenz Attractor')
 
    num_frames = 1200             # total number of frames shown in the animation
    skip = int(num_steps / num_frames) # number
    anim = matplotlib.animation.FuncAnimation(fig,
                                              animate_plots,
                                              frames=num_frames,
                                              fargs=(x, y, z, plots, cursors, skip),
                                              interval=30,
                                              blit=False)
 
    #matplotlib.pyplot.show()
    anim.save('Lorenz_system.gif',writer='imagemagick', fps=30)


animation()

