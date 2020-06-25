from numpy import sin, cos
import numpy as np 
import matplotlib.pyplot as plt 
import scipy.integrate as integrate
import matplotlib.animation as animation


class PendulumODESolver:
	def __init__(self,
		         init_state = [120,0,-20,0],
		         L1  = 1.0,
		         L2  = 1.0,
		         M1  = 1.0,
		         M2  = 1.0,
		         G   = 9.8,
		         origin =(0,0)):
		self.init_state = np.asarray(init_state,dtype='float')
		self.params = (L1,L2,M1,M2,G)
		self.origin = origin
		self.time_elapsed = 0 
		self.history = np.zeros([10000,2])
		self.state = self.init_state * np.pi / 180.



	def position(self):
		(L1,L2,M1,M2,G) = self.params

		x = L1 * sin(self.fstate[:,0])
		y = -L1 * cos(self.fstate[:,0])

		return(x,y)


	def position1(self):
		(L1,L2,M1,M2,G) = self.params

		x = np.cumsum([self.origin[0],
					   L1 * sin(self.state[0]),
					   L2 * sin(self.state[2])])

		y = np.cumsum([self.origin[1],
					   -L1 * cos(self.state[0]),
					   -L2 * cos(self.state[2])])			   	

		return(x,y)	

	
	def trac(self):
		(L1,L2,M1,M2,G) = self.params
		
		xt = L1 * sin(self.fstate[:,0]) + L2 * sin(self.fstate[:,2])		
		yt = -L1 * cos(self.fstate[:,0]) - L2 * cos(self.fstate[:,2])

		return(xt,yt)	

	def dstate_dt(self, state, t):
		(M1,M2,L1,L2,G) = self.params
		dydx = np.zeros_like(state)
		dydx[0] = state[1]
		dydx[2] = state[3]
		cos_delta = cos(state[2] - state[0])
		sin_delta = sin(state[2] - state[0])

		den1 = (M1 + M2) * L1 - M2 * L1 * cos_delta * cos_delta
		dydx[1] = (M2 * L1 * state[1] * state[1] * sin_delta * cos_delta
 				   + M2 * G * sin(state[2]) * cos_delta
 				   + M2 * L2 * state[3] * state[3] * sin_delta
 				   - (M1+M2) * G * sin(state[0])) / den1

		den2 = (L2 / L1) * den1

		dydx[3] = (-M2 * L2 * state[3] * state[3] * sin_delta * cos_delta
 				   + (M1+M2) * G * sin(state[0]) * cos_delta
 				   - (M1+M2) * L1 * state[1] * state[1] * sin_delta
 				   - (M1+M2) * G * sin(state[2])) / den2
		return dydx
 		

	def step(self,ts):
		self.fstate = integrate.odeint(self.dstate_dt,self.state,ts)

	def step1(self, dt):

		self.state = integrate.odeint(self.dstate_dt,self.state,[0,dt])[1]
		self.time_elapsed += dt
