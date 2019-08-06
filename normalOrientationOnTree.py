import numpy as np 
from ternaryTreeConstructBis import *

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

# class NormalCompute(object):
# 	"""docstring for normalCompute"""
# 	def __init__(self, FAN):
# 		self.FAN = FAN
# 		self.computeNormals(self.FAN)

# 	def computeNormalForEdges(self,edges):
# 		e1 = edges[0]
# 		e2 = edges[1]

# 		a = e2[0]
# 		b = e2[1]
# 		c = e2[2]


# 		d = e1[0]
# 		e = e1[1]
# 		f = e1[2]

# 		det = -b*d + e*a

# 		x = b*f - c*e
# 		y = c*d - a*f
# 		return (x/det,y/det,1)

# 	def computeNormals(self,FAN):
# 		edges  = FAN.edges.values()
# 		FAN.normal = self.computeNormalForEdges(edges)
# 		for key in FAN.faces.keys():
# 			face= FAN.faces[key]
# 			if (face is not(None)):
# 				self.computeNormals(face)

# def printNormals(FAN):
# 	if (len(FAN.normal)!=3):
# 		exit(1)
# 	for el in FAN.faces.keys():
# 		face=FAN.faces[el]
# 		if (face is not(None)):
# 			printNormals(face)
# 	return 0


class OrientationCompute(object):
	"""docstring for OrientationCompute"""
	class_faceProcessed = 0
	def __init__(self, FAN):
		self.FAN = FAN
		self.FAN.orientation = 1
		self.computeOrientationChild(self.FAN)

	# def printNormal(self):


	def computeOrientationChild(self,FAN):
		ni = FAN.normal
		ci = FAN.insideElement
		for key in  FAN.faces.keys():
			if (FAN.faces[key] is not(None)):
				# nij = FAN.edges[key]
				nj = FAN.faces[key].normal
				cj = FAN.insideElement

				cji = cj-ci
				cij = -cji
				constraint = (cij[0]*nj[0] + cij[1]*nj[1] + cij[2]*nj[2]) * (cji[0]*ni[0] + cji[1]*ni[1] + cji[2]*ni[2])
				if (constraint>0):
					FAN.faces[key].orientation = FAN.orientation
				elif (constraint<0):
					FAN.faces[key].orientation = - FAN.orientation
				elif (constraint ==0):
					if (ni[0]*nj[0] + ni[1]*nj[1] + ni[2]*nj[2]>0):
						FAN.faces[key].orientation = FAN.orientation
					else:
						FAN.faces[key].orientation = -FAN.orientation
				# edgeConstraint = np.sign(ni[0]*nj[0] + ni[1]*nj[1] +ni[2]*nj[2] - (ni[0]*nij[0] + ni[1]*nij[1] + ni[2]*nij[2]) * (nj[0]*nij[0] + nj[1]*nij[1] + nj[2]*nij[2]))
				# FAN.faces[key].orientation = -edgeConstraint*FAN.orientation
				self.computeOrientationChild(FAN.faces[key])

class TreeToListResultConverter(object):
	"""docstring for showOrientation"""
	def __init__(self, FAN):
		self.FAN = FAN
		self.listNormals,self.listInsidePt = [],[]
		self.getOrientedNormals(self.FAN)
		self.listNormals = np.array(self.listNormals)
		self.listInsidePt = np.array(self.listInsidePt)
	def getOrientedNormals(self,FAN):
		self.listNormals.append(FAN.orientation * np.array(FAN.normal))
		self.listInsidePt.append(FAN.insideElement)
		for key in FAN.faces:
			if (FAN.faces[key] is not(None)):
				self.getOrientedNormals(FAN.faces[key])
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

if __name__ == '__main__':
	FAN = pickle.load(open('FANInit.txt','rb'))
	OrientationCompute(FAN)
	showAlgo = TreeToListResultConverter(FAN)
	# listNormals,listInsidePt = [],[]
	# listNormals,listInsidePt = getOrientedNormals(FAN,listNormals,listInsidePt)
	# listNormals = np.array(listNormals)

	# norm = np.sqrt(listNormals[:,0]**2+listNormals[:,1]**2+listNormals[:,2]**2)
	# listNormalsNormalized = [listNormals[i]/norm[i] for i in range(len(norm))]
	# listNormalsNormalized = np.array(listNormalsNormalized)
	# algo = OrientationCompute(FAN)

