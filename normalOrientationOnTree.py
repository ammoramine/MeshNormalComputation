import numpy as np 
import localConstraint

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

class OrientationComputer(object):
	"""docstring for OrientationCompute"""
	class_faceProcessed = 0
	def __init__(self, FAN):
		self.FAN = FAN
		self.FAN.faceInfo.orientation = 1
		self.computeOrientationChild(self.FAN)

	# def printNormal(self):


	def computeOrientationChild(self,FAN):
		OrientationComputer.class_faceProcessed+=1
		print(OrientationComputer.class_faceProcessed)
		ni = FAN.faceInfo.normal
		ci = FAN.faceInfo.insideElement
		for key in  FAN.faces.keys():
			if (FAN.faces[key] is not(None)):
				# nij = FAN.edges[key]
				for face in  FAN.faces[key]:
					nj = face.faceInfo.normal
					cj = FAN.faceInfo.insideElement

					sign = localConstraint.checkOrientationConnectedSimplexe([ni,ci],[nj,cj])
					face.faceInfo.orientation = sign * FAN.faceInfo.orientation
					self.computeOrientationChild(face)

class TreeToListResultConverter(object):
	"""docstring for showOrientation"""
	def __init__(self, FAN):
		self.FAN = FAN
		self.listNormals,self.listInsidePt,self.listIndexFaces = [],[],[]
		self.getOrientedNormalsOfFace(self.FAN)
		self.listNormals = np.array(self.listNormals)
		self.listInsidePt = np.array(self.listInsidePt)
		self.listIndexFaces = np.array(self.listIndexFaces)

		self.orderTheLists()
	def getOrientedNormalsOfFace(self,FAN):
		self.listNormals.append(FAN.faceInfo.orientation * np.array(FAN.faceInfo.normal))
		self.listInsidePt.append(FAN.faceInfo.insideElement)
		self.listIndexFaces.append(FAN.faceInfo.indexFace)
		for key in FAN.faces:
			if (FAN.faces[key] is not(None)):
				for face in FAN.faces[key]:
					self.getOrientedNormalsOfFace(face)

	def orderTheLists(self):
		"""order the list or normals starting from the face of index 0 to the face of last index"""
		orderedIndexOfFaces = np.argsort(self.listIndexFaces)
		self.listNormals = self.listNormals[orderedIndexOfFaces]
		self.listInsidePt = self.listInsidePt[orderedIndexOfFaces]

	# def saveNormalOfFaces(self,faceNormalsFile = "face_normals.npy"):
		# np.save(faceNormalsFile,self.listNormals)

# 	def showOrientation(self,N1,N2,lengthNormal=0.07):
# 		fig = plt.figure()
# 		x = self.listInsidePt[:,0];y = self.listInsidePt[:,1];z = self.listInsidePt[:,2]

# 		xPartial = self.listInsidePt[N1:N2,0];yPartial = self.listInsidePt[N1:N2,1];zPartial = self.listInsidePt[N1:N2,2]
# 		nxPartial = self.listNormals[N1:N2,0];  nyPartial = self.listNormals[N1:N2,1];nzPartial = self.listNormals[N1:N2,2]

# 		ax = fig.gca(projection='3d')
# 		ax.quiver(xPartial, yPartial, zPartial, nxPartial,nyPartial,nzPartial, length=lengthNormal,normalize = True,color = 'r');

# 		ax1 = fig.gca(projection='3d')
# 		ax1.plot(x, y, z, c='b')

# 		plt.show()

# class OrientationVertexComputer(object):
# 	"""docstring for ClassName"""
# 	def __init__(self, FAN):
# 		self.FAN = FAN
		

if __name__ == '__main__':
	FAN = pickle.load(open('FANInitBis.txt','rb'))
	OrientationComputer(FAN)
	treeToListResultConverter = TreeToListResultConverter(FAN)


	# listNormals,listInsidePt = [],[]
	# listNormals,listInsidePt = getOrientedNormalsOfFace(FAN,listNormals,listInsidePt)
	# listNormals = np.array(listNormals)

	# norm = np.sqrt(listNormals[:,0]**2+listNormals[:,1]**2+listNormals[:,2]**2)
	# listNormalsNormalized = [listNormals[i]/norm[i] for i in range(len(norm))]
	# listNormalsNormalized = np.array(listNormalsNormalized)
	# algo = OrientationComputer(FAN)

