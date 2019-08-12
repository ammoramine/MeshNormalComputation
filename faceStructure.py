import numpy as np
import pdb
import sys
import time
import cPickle as pickle
import dill
import normalComputation


def NSquareNMapping((i,j)):
	"""a bijetive application from NSquare to N
		the reverse application is useless for this application
		the common 
		"""
	return int((i+j)*(i+j+1)/2+(j+1))


class FaceInfo(object):
	"""docstring for FaceInfo"""
	def __init__(self, normalFaceNO, insideElementOfFace,edgeIndex,indexFace):
		self.normal = normalFaceNO
		self.insideElement = insideElementOfFace
		self.edgeIndex = edgeIndex
		self.indexFace = indexFace

class FacesInfo(object):
	"""docstring for FacesProcessed"""
	def __init__(self, faces, vertices):
		self.faces = faces
		self.vertices = vertices


		self.computeNormals()
		self.computeInsideElement()
		self.constructEdgeIndexAndVertex()
		self.constructFaceIndexes()

		self.constructListOfFaces()


	def computeNormals(self):
		vfaces = self.vertices[self.faces]
		# facesAsEdgeVector = [ [el[2] - el[1] ,el[2] - el[0] ] for el in vfaces]
		vface0 = vfaces[:,0,:]
		vface1 = vfaces[:,1,:]
		vface2 = vfaces[:,2,:]

		self.normalFaces = normalComputation.computeNormalMultiple([vface0,vface1,vface2])

	def computeInsideElement(self):
		vfaces = self.vertices[self.faces]
		self.insideElementOfFaces = np.matmul((0.25,0.25,0.5),vfaces)

	def constructEdgeIndexAndVertex(self):
		self.facesedges = [[ [el[0],el[1]] , [el[1],el[2]] , [el[0],el[2]] ] for el in self.faces]
		self.facesedges = [[[min(el1),max(el1)] for el1 in el] for el in self.facesedges]
		self.facesAsEdgeIndexes = np.array([[NSquareNMapping(el1) for el1 in el] for el in self.facesedges])

	def constructFaceIndexes(self):
		"""the index of the face is its index on the original list"""
		self.indexFaces = np.arange(self.faces.shape[0]).reshape(-1,1)
	def constructListOfFaces(self):

		tmp = np.hstack((self.normalFaces,self.insideElementOfFaces,self.facesAsEdgeIndexes.astype(self.normalFaces.dtype),self.indexFaces.astype(self.normalFaces.dtype)))
		self.listOfFaces = [FaceInfo(el[0:3],el[3:6],el[6:9],el[9]) for el in tmp]


class FaceAsNode(object):
	"""docstring for Node"""
	def __init__(self,faceInfo,nbResEdgeMax=3):
		self.faceInfo = faceInfo 
		self.nbResEdgeMax = nbResEdgeMax
		self.faces = dict.fromkeys(self.faceInfo.edgeIndex)
		self.keys = set(self.faces.keys())
	def addFace(self,AFaceAsNode,edgeIndex):
		self.faces[edgeIndex] = AFaceAsNode
		# AFaceAsNode.nbResEdgeMax-=1
		# self.nbResEdgeMax -= 1

	def checkIntersectionAndAddFace(self,AFaceAsNode):
		listCommonElement = list(self.keys & AFaceAsNode.keys)
		if (len(listCommonElement)==0):
			return False
		else:
			self.addFace(AFaceAsNode,listCommonElement[0])
			return True
		# self.addFace(commonElement)
		# for el1 in self.keys:
			# for el2 in AFaceAsNode.keys:
				# if (el1==el2):
					# self.addFace(AFaceAsNode,el1)
					# return True
		# return False