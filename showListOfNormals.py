import numpy as np

# class ClassName(object):
# 	"""docstring for ClassName"""
# 	def __init__(self, arg):
# 		super(ClassName, self).__init__()
# 		self.arg = arg
		
	def showOrientation(self,N1,N2,lengthNormal=0.07):
		fig = plt.figure()
		x = self.listInsidePt[:,0];y = self.listInsidePt[:,1];z = self.listInsidePt[:,2]

		xPartial = self.listInsidePt[N1:N2,0];yPartial = self.listInsidePt[N1:N2,1];zPartial = self.listInsidePt[N1:N2,2]
		nxPartial = self.listNormals[N1:N2,0];  nyPartial = self.listNormals[N1:N2,1];nzPartial = self.listNormals[N1:N2,2]

		ax = fig.gca(projection='3d')
		ax.quiver(xPartial, yPartial, zPartial, nxPartial,nyPartial,nzPartial, length=lengthNormal,normalize = True,color = 'r');

		ax1 = fig.gca(projection='3d')
		ax1.plot(x, y, z, c='b')

		plt.show()