import numpy as np
import pdb
import sys
import time
import cPickle as pickle
import dill

sys.setrecursionlimit(100000)
def NSquareNMapping((i,j)):
	return int((i+j)*(i+j+1)/2+(j+1))


class FaceVerboseInfo(object):
	"""docstring for FaceVerboseInfo"""
	def __init__(self, facesAsEdgeIndexToVector,normalFaceNO):
		self.facesAsEdgeIndexToVector = facesAsEdgeIndexToVector
		self.normalFaceNO = normalFaceNO		

class FacesVerboseInfo(object):
	"""docstring for FacesProcessed"""
	def __init__(self, faces, vertices):
		self.faces = faces
		self.vertices = vertices

		self.constructEdgeIndexAndVertex()

		self.computeNormals()

		self.constructListOfFaces()

	def computeEdgeIndexAndVector(self):
		vfaces = self.vertices[self.faces]
		for i in range(len(self.faces)):
			face = self.faces[i]
			vface = vfaces[i]
			indexEdge = NSquareNMapping(face[0],face[1])
			vectorEdge = vface[1] - vface[0]

			indexEdge = NSquareNMapping(face[1],face[2])
			vectorEdge = vface[1] - vface[0]

	def computeNormals(self):
		self.normalFacesNO = [ self.computeNormal(edges.values()) for edges  in self.facesAsEdgeIndexToVector]

	# @staticmethod
	def computeNormal(self,edges):
		e1 = edges[0]
		e2 = edges[1]

		a = e2[0]
		b = e2[1]
		c = e2[2]


		d = e1[0]
		e = e1[1]
		f = e1[2]

		det = -b*d + e*a

		x = b*f - c*e
		y = c*d - a*f
		return (x/det,y/det,1)

	def constructEdgeIndexAndVertex(self):
		facesedges = [[ [el[0],el[1]] , [el[1],el[2]] , [el[0],el[2]] ] for el in self.faces]
		facesedges = [[[min(el1),max(el1)] for el1 in el] for el in facesedges]
		facesAsEdgeIndexes = np.array([[NSquareNMapping(el1) for el1 in el] for el in facesedges])

		vfaces = vertices[self.faces]
		facesAsEdgeVector = [ [el[1] - el[0] , el[2] - el[1] ,el[2] - el[0] ] for el in vfaces]

		self.facesAsEdgeIndexToVector = [dict(zip(facesAsEdgeIndexes[i],facesAsEdgeVector[i])) for i in range(len(facesAsEdgeIndexes)) ]
	def constructListOfFaces(self):
		self.listOfFaces = [FaceVerboseInfo(self.facesAsEdgeIndexToVector[i],self.normalFacesNO[i]) for i in range(len(self.facesAsEdgeIndexToVector))]


class FaceAsNode(object):
	"""docstring for Node"""
	def __init__(self,faceVerboseInfo,nbResEdgeMax=3):
		self.edges = faceVerboseInfo.facesAsEdgeIndexToVector
		self.normal = faceVerboseInfo.normalFaceNO
		self.nbResEdgeMax = nbResEdgeMax
		self.faces = dict.fromkeys(self.edges.keys())

	def addFace(self,AFaceAsNode,edgeIndex):
		if (edgeIndex is not(None)):
			self.faces[edgeIndex] = AFaceAsNode
			self.nbResEdgeMax -= 1
			return True
		return False

	def checkIntersection(self,AFaceAsNode):
		for el1 in self.edges.keys():
			for el2 in AFaceAsNode.edges.keys():
				if (el1==el2):
					return el1

	def checkIntersectionAndAddFace(self,AFaceAsNode):
		edgeIndex = self.checkIntersection(AFaceAsNode)
		faceAdded = self.addFace(AFaceAsNode,edgeIndex)
		return faceAdded


class TernaryTreeEdgeConstruct(object):
	"""docstring for TernaryTreeEdgeConstruct"""
	def __init__(self, listOfFaces):
		self.listOfFacesAsNode = [FaceAsNode(el) for el in listOfFaces]
		self.FANInit = self.listOfFacesAsNode[0]
		del self.listOfFacesAsNode[0]

		print(len(self.listOfFacesAsNode))
		pdb.runcall(self.TernaryConstruct,self.FANInit)
		# self.TernaryConstruct(self.FANInit)

	def TernaryConstruct(self,FAN):
		# indexesToRemove = []
		# index=0
		# listOfFacesAsNodeCopy = self.listOfFacesAsNode.copy()
		for el in list(self.listOfFacesAsNode):
			faceAdded = FAN.checkIntersectionAndAddFace(el)
			if(faceAdded):
				self.listOfFacesAsNode.remove(el)
				#TODO : change for loop with iterator on list
			# index+=1
		# for el in indexesToRemove:
			# del self.listOfFacesAsNode[el]

		# print("\n")
		# print(len(indexesToRemove))
		print(len(self.listOfFacesAsNode))
		# print(FAN.edges)
		# print("\n")

		for key in FAN.faces.keys():
			# face = FAN.faces[key]
			if (FAN.faces[key] is not(None)):
				self.TernaryConstruct(FAN.faces[key])


		

if __name__ == '__main__':
	
	# filename='/tmp/shelve.out'
	# my_shelf = shelve.open(filename,'n') # 'n' for new
	filename = 'globalsave.pkl'
	faces = np.load("bunny_faces.npy")
	vertices = np.load("bunny_vertices.npy")
	algoFacesConstruct = FacesVerboseInfo(faces,vertices)
	listOfFaces = algoFacesConstruct.listOfFaces

	algo = TernaryTreeEdgeConstruct(listOfFaces)
	# start=time.time()
	# algo = TernaryTreeEdgeConstruct(faces)
	# stop = time.time()
	# dill.dump_session(filename)

	# my_shelf.close()
	# algo.computeFacesFromEdges()
	# algo.TernaryConstruct()