import numpy as np
import pdb
import sys
import time
import cPickle as pickle
import dill
import normalComputation

sys.setrecursionlimit(100000)
def NSquareNMapping((i,j)):
	"""a bijetive application from NSquare to N
		the reverse application is useless for this application
		the common 
		"""
	return int((i+j)*(i+j+1)/2+(j+1))


class FaceInfo(object):
	"""docstring for FaceInfo"""
	def __init__(self, normalFaceNO, insideElementOfFace,edgeIndex):
		self.normal = normalFaceNO
		self.insideElement = insideElementOfFace
		self.edgeIndex = edgeIndex

class FacesInfo(object):
	"""docstring for FacesProcessed"""
	def __init__(self, faces, vertices):
		self.faces = faces
		self.vertices = vertices


		self.computeNormals()
		self.computeInsideElement()
		self.constructEdgeIndexAndVertex()

		self.constructListOfFaces()


	def computeNormals(self):
		vfaces = vertices[self.faces]
		# facesAsEdgeVector = [ [el[2] - el[1] ,el[2] - el[0] ] for el in vfaces]
		vface0 = vfaces[:,0,:]
		vface1 = vfaces[:,1,:]
		vface2 = vfaces[:,2,:]

		v21 = vface2 - vface1
		v20 = vface2 - vface0
		self.normalFaces = normalComputation.computeNormalMultiple([v20,v21])

	def computeInsideElement(self):
		vfaces = self.vertices[self.faces]
		self.insideElementOfFaces = np.matmul((0.25,0.25,0.5),vfaces)

	def constructEdgeIndexAndVertex(self):
		facesedges = [[ [el[0],el[1]] , [el[1],el[2]] , [el[0],el[2]] ] for el in self.faces]
		facesedges = [[[min(el1),max(el1)] for el1 in el] for el in facesedges]
		self.facesAsEdgeIndexes = np.array([[NSquareNMapping(el1) for el1 in el] for el in facesedges])
	def constructListOfFaces(self):

		tmp = np.hstack((self.normalFaces,self.insideElementOfFaces,self.facesAsEdgeIndexes.astype(self.normalFaces.dtype)))
		self.listOfFaces = [FaceInfo(el[0:3],el[3:6],el[6:9]) for el in tmp]


class FaceAsNode(object):
	"""docstring for Node"""
	def __init__(self,faceInfo,nbResEdgeMax=3):
		self.faceInfo = faceInfo 
		self.nbResEdgeMax = nbResEdgeMax
		self.faces = dict.fromkeys(self.faceInfo.edgeIndex)

	def addFace(self,AFaceAsNode,edgeIndex):
		self.faces[edgeIndex] = AFaceAsNode
		self.nbResEdgeMax -= 1

	def checkIntersectionAndAddFace(self,AFaceAsNode):
		for el1 in self.faces.keys():
			for el2 in AFaceAsNode.faces.keys():
				if (el1==el2):
					self.addFace(AFaceAsNode,el1)
					return True
		return False


class TernaryTreeEdgeConstruct(object):
	"""docstring for TernaryTreeEdgeConstruct"""
	def __init__(self, listOfFaces):
		self.listOfFacesAsNode = [FaceAsNode(el) for el in listOfFaces]
		self.FANInit = self.listOfFacesAsNode[0]
		del self.listOfFacesAsNode[0]

		print(len(self.listOfFacesAsNode))
		self.TernaryConstruct(self.FANInit)

	def TernaryConstruct(self,FAN):
		for el in list(self.listOfFacesAsNode):
			faceAdded = FAN.checkIntersectionAndAddFace(el)
			if(faceAdded):
				self.listOfFacesAsNode.remove(el)
		print(len(self.listOfFacesAsNode))
		for key in FAN.faces.keys():
			if (FAN.faces[key] is not(None)):
				self.TernaryConstruct(FAN.faces[key])


		

if __name__ == '__main__':
	
	# filename='/tmp/shelve.out'
	# my_shelf = shelve.open(filename,'n') # 'n' for new
	# filename = 'globalsave.pkl'
	faces = np.load("bunny_faces.npy")
	vertices = np.load("bunny_vertices.npy")
	algoFacesConstruct = FacesInfo(faces,vertices)
	listOfFaces = algoFacesConstruct.listOfFaces
	start= time.time()
	algo = TernaryTreeEdgeConstruct(listOfFaces)
	stop = time.time()
	# start=time.time()
	# algo = TernaryTreeEdgeConstruct(faces)
	# stop = time.time()
	# dill.dump_session(filename)

	# my_shelf.close()
	# algo.computeFacesFromEdges()
	# algo.TernaryConstruct()