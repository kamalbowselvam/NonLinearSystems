import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PendulumODE import PendulumODESolver

pendulum =  PendulumODESolver([180., 0.0, 180.1, 0.0])
pendulum2 =  PendulumODESolver([180, 0.0, 180.1001, 0.0])
dt = 1./30 #30 fps 
ts = np.arange(0,10,0.001)

pendulum.step(ts)
pendulum2.step(ts)

x1,y1 = pendulum.position() 
x2,y2 = pendulum.trac()

x21,y21 = pendulum2.position() 
x22,y22 = pendulum2.trac()

fig = plt.figure()
ax  = plt.axes(aspect='equal',xlim =(-2,2), ylim = (-2,2))
plts = ax.plot([], [], 'o-',lw=2)
tractor = ax.plot([], [], 'r')
plts2 = ax.plot([], [], 'mo-',lw=2)
tractor2 = ax.plot([], [], 'g')
scat = ax.scatter(x2[0], y2[0], s=150,c='k')
scat2 = ax.scatter(x2[0], y2[0], s=150,c='k')

def init():
	plts.set_data([],[])
	plts2.set_data([],[])
	return plts,plts2

def animate(num,x1,y1,x2,y2,x21,y21,x22,y22,plts,plts2,tractor,tractor2,scat,scat2,skip):
	xp = [0,x1[num*skip],x2[num*skip]]
	yp = [0,y1[num*skip],y2[num*skip]]
	plts[0].set_data(xp,yp)
	tractor[0].set_data(x2[:num*skip],y2[:num*skip])
	xp2 = [0,x21[num*skip],x22[num*skip]]
	yp2 = [0,y21[num*skip],y22[num*skip]]
	plts2[0].set_data(xp2,yp2)
	tractor2[0].set_data(x22[:num*skip],y22[:num*skip])


	if num > 0:
		p1 = x2[num * skip - 1:num * skip].tolist()
		p2 = y2[num * skip - 1:num * skip].tolist()
		scat.set_offsets([p1[0], p2[0]])
		p21 = x22[num*skip-1:num*skip].tolist()
		p22 = y22[num*skip-1:num*skip].tolist()
		scat2.set_offsets([p21[0], p22[0]])

	return plts,plts2

skip = 10
ani = animation.FuncAnimation(fig, animate, frames=3000, fargs = (x1,y1,x2,y2,x21,y21,x22,y22,plts,plts2,tractor,tractor2,scat,scat2,skip),interval=30)
ani.save('Double_Pendulum.gif',writer='imagemagick', fps=30)
#ani.save('clock.mp4', fps=50, dpi=250)
#plt.show()