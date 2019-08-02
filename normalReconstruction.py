import numpy as np
import pdb
import sys
import time
import pickle
sys.setrecursionlimit(100000)
def NSquareNMapping((i,j)):
	return int((i+j)*(i+j+1)/2+(j+1))

class FaceAsNode(object):
	"""docstring for Node"""
	def __init__(self,facesFromEdge,nbResEdgeMax=3):
		self.edgeIndex = [ facesFromEdge[i] for i in range(3)]
		self.nbResEdgeMax = nbResEdgeMax
		self.faces = []
	# @classmethod
	def addFace(self,AFaceAsNode):
		self.faces.append(AFaceAsNode)
		self.nbResEdgeMax-=1
	# def testLink(self,face):

	# def addChild(self):
		# while()
		# self.normal = self.computeNormal()

		# def computeNormal

class TernaryTreeEdgeConstruct(object):
	"""docstring for TernaryTreeEdgeConstruct"""
	def __init__(self, faces):
		self.faces = faces
		self.computeFacesFromEdges()
		self.FAN = FaceAsNode(self.facesAsEdgeIndexes[0])
		self.facesAsEdgeIndexes = np.delete(self.facesAsEdgeIndexes,0,0)

		# pdb.runcall(self.TernaryConstruct,FAN)
		self.TernaryConstruct(self.FAN)
	def computeFacesFromEdges(self):
		self.facesBis = [[list(el[0:2]),list(el[1:3]),[el[0],el[2]]] for el in self.faces]
		self.facesBis = [[[min(el1),max(el1)] for el1 in el] for el in self.facesBis]
		self.facesAsEdgeIndexes = np.array([[NSquareNMapping(el1) for el1 in el] for el in self.facesBis])

	@staticmethod
	def intersect(ar1,ar2):
		for el1 in ar1:
			for el2 in ar2:
				if (el1==el2):
					return True
		return False

	def TernaryConstruct(self,FAN):
		# it = np.nditer(self.facesAsEdgeIndexes, flags=['f_index'])
		indexesToRemove = []
		# while not it.finished:
		index=0
		for el in self.facesAsEdgeIndexes:
			if (FAN.nbResEdgeMax == 0):
				break;
			# el=it[0]
			if (self.intersect(el,FAN.edgeIndex)):
				indexesToRemove.append(index)
				FAN.addFace(FaceAsNode(el,2))
			# it.iternext()
			index+=1
		self.facesAsEdgeIndexes = np.delete(self.facesAsEdgeIndexes,indexesToRemove,0)
		print(len(self.facesAsEdgeIndexes))
		# start = time.time()
		for i in range(len(FAN.faces)):
			self.TernaryConstruct(FAN.faces[i])
		# stop= time.time()
		# print(stop-start)



if __name__ == '__main__':
	faces = np.load("bunny_faces.npy")
	vertices = np.load("bunny_vertices.npy")
	algo = TernaryTreeEdgeConstruct(faces)
	# algo.computeFacesFromEdges()
	# algo.TernaryConstruct()