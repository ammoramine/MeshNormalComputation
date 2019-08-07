import numpy as np
import pdb
import sys
import time
import cPickle as pickle
import dill
import normalComputation
from faceStructure import *

sys.setrecursionlimit(100000)



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
	

	faces = np.load("bunny_faces.npy")
	vertices = np.load("bunny_vertices.npy")
	algoFacesConstruct = FacesInfo(faces,vertices)
	listOfFaces = algoFacesConstruct.listOfFaces
	start= time.time()
	algo = TernaryTreeEdgeConstruct(listOfFaces)
	stop = time.time()