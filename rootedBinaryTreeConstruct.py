import numpy as np
import pdb
import sys
import time
import cPickle as pickle
import dill
import normalComputation
from faceStructure import *

sys.setrecursionlimit(100000)

class Bucket(object):
	"""docstring for Bucket:
		a bucket contains a list of faces sharing the same edge, surprisingly, it can contains more than 2 faces, each (simplexe) face is contained in 3 differents buckets, representing each a different edge!
	"""
	def __init__(self, faces,commonEdge):
		self.faces = faces
		self.commonEdge = commonEdge
		
class RootedBinaryTreeEdgeConstruct(object):
# 	"""docstring for RootedBinaryTreeEdgeConstruct"""
	nbLinked = 0
	def __init__(self, FANInit):
		self.FANInit = FANInit
		self.FANInit.linked = True
		self.constructTernaryTree(self.FANInit)

	def constructTernaryTree(self,FAN):
		for bucket in FAN.buckets:
			for face in bucket.faces:
				if(not(face.linked)):
					FAN.addFace(face,bucket.commonEdge)
					face.linked = True
					RootedBinaryTreeEdgeConstruct.nbLinked+=1
					print(RootedBinaryTreeEdgeConstruct.nbLinked)
					self.constructTernaryTree(face)


class BucketConstructor(object):
	"""docstring for BucketConstructor:
		a class constructing bucket
	"""
	def __init__(self, algoFacesConstruct):
		self.algoFacesConstruct = algoFacesConstruct
		listOfFaces = self.algoFacesConstruct.listOfFaces
		self.listOfFacesAsNode = [FaceAsNode(el) for el in listOfFaces]

		self.getListOfFaceSharingEdges()
		self.constructBuckets()

	def getIndexOfChange(self,a):
		"""the array a contains groups of consecutives elements of same values,the method returns the beginning index of each groupe, and its ending index"""
		# a = np.array([el[0] for el in faceAsEdgeIndexesWithIndexFaceEdgeSorted])

		indexChangeEnd = np.where(a[1:]!=a[:-1])[0]
		indexChangeBegin = indexChangeEnd+1

		indexChangeEnd = np.hstack((indexChangeEnd,a.shape[0]-1))
		indexChangeBegin = np.hstack((0,indexChangeBegin))
		return indexChangeBegin,indexChangeEnd		
	def getListOfFaceSharingEdges(self):
		tmp = np.array([el.faceInfo.edgeIndex for el in self.listOfFacesAsNode])
		tmp = np.vstack([(tmp[:,i].reshape(-1,1)) for i in range(3)])

		tmp1tmp1 = np.array([el.faceInfo.indexFace for el in self.listOfFacesAsNode]).reshape(-1,1)
		tmp1 = np.vstack([tmp1tmp1 for i in range(3)])

		faceAsEdgeIndexesWithIndexFace =  np.hstack((tmp,tmp1))
		faceAsEdgeIndexesWithIndexFaceEdgeSorted = faceAsEdgeIndexesWithIndexFace[np.argsort(tmp,axis=0).reshape(-1)]

		s = (self.listOfFacesAsNode+self.listOfFacesAsNode+self.listOfFacesAsNode)
		facesAsNodeWithEdgeIndex = [[el[0],s[int(el[1])]] for el in faceAsEdgeIndexesWithIndexFaceEdgeSorted]

		a = np.array([el[0] for el in faceAsEdgeIndexesWithIndexFaceEdgeSorted])


		indexChangeBegin,indexChangeEnd = self.getIndexOfChange(a)

		self.listOfListOfFacesSharingEdges = [facesAsNodeWithEdgeIndex[indexChangeBegin[i]:indexChangeEnd[i]+1] for i in range(indexChangeBegin.shape[0])]
		# return listOfListOfFacesSharingEdges

	def constructBuckets(self):
		for bucket in self.listOfListOfFacesSharingEdges:
			facesTmp = [el[1] for el in bucket]
			commonEdge = bucket[0][0]
			for el in bucket:
				face= el[1]
				face.buckets.append(Bucket(facesTmp,commonEdge))

	def findInitFace(self,faceInfoOO):
		for bucket in self.listOfListOfFacesSharingEdges:
			for el in bucket:
				currentFaceInfo = el[1].faceInfo
				if (currentFaceInfo == faceInfoOO):
					# self.FANOO = el[1]
					return el[1]
	# 	lastedgeIndex = 0
	# 	newBucketIndex = [lastedgeIndex]
	# 	for el in self.facesAsNodeWithEdgeIndex:
	# 		if (el[0]!=lastedgeIndex):
	# 			newBucket = [el]
	# 		else:
	# 			newBucket.append(el)


# def processListOfBuckets(listOfBuckets):
	# for el in listOfBuckets:
		# for
if __name__ == '__main__':
	

	facesWithRedondancy = np.load("bunny_faces.npy")
	faces = np.unique(np.sort(facesWithRedondancy,axis=1),axis=0) # remove redundant faces
	vertices = np.load("bunny_vertices.npy")
	algoFacesConstruct = FacesInfo(faces,vertices)


	algoBucket = BucketConstructor(algoFacesConstruct)


	# s = algoBucket.findInitFace(algoFacesConstruct.listOfFaces[10])
	binaryConstructAlgo = RootedBinaryTreeEdgeConstruct(algoBucket.listOfFacesAsNode[10])

	# binaryConstructAlgo = pdb.runcall(RootedBinaryTreeEdgeConstruct,algoBucket.listOfFacesAsNode[10])
	# listOfFaces = algoFacesConstruct.listOfFaces
	# listOfFacesAsNode = [FaceAsNode(el) for el in listOfFaces]

	# listOfFacesAsNode = algoBucket.listOfFacesAsNode
	# start=time.time()
	# faceAsEdgeIndexes = algoFacesConstruct.facesAsEdgeIndexes
	# indexFaces = np.linspace(0,faceAsEdgeIndexes.shape[0]-1,faceAsEdgeIndexes.shape[0])
	# tmp = np.vstack([faceAsEdgeIndexes[:,i].reshape(-1,1) for i in range(3)])
	# tmp1 = np.vstack([indexFaces.reshape(-1,1) for i in range(3)])
	# faceAsEdgeIndexesWithIndexFace =  np.hstack((tmp,tmp1))

	# stop=time.time()
	# print(stop-start)
	# faceAsEdgeIndexesWithIndexFaceEdgeSorted = faceAsEdgeIndexesWithIndexFace[np.argsort(tmp,axis=0).reshape(-1)]

	# s = (listOfFacesAsNode+listOfFacesAsNode+listOfFacesAsNode)
	# facesAsNodeWithEdgeIndex = [[el[0],s[int(el[1])]] for el in faceAsEdgeIndexesWithIndexFaceEdgeSorted]

	# a = np.array([el[0] for el in faceAsEdgeIndexesWithIndexFaceEdgeSorted])

	# indexChangeEnd = np.where(a[1:]!=a[:-1])[0]
	# indexChangeBegin = indexChangeEnd+1

	# indexChangeEnd = np.hstack((indexChangeEnd,a.shape[0]-1))
	# indexChangeBegin = np.hstack((0,indexChangeBegin))

	# listOfBuckets = [facesAsNodeWithEdgeIndex[indexChangeBegin[i]:indexChangeEnd[i]+1] for i in range(indexChangeBegin.shape[0])]

	# for bucket in listOfBuckets:
	# 	facesTmp = [el[1] for el in bucket]
	# 	commonEdge = bucket[0][0]
	# 	for el in bucket:
	# 		face= el[1]
	# 		face.buckets.append(Bucket(facesTmp,commonEdge))

	# # algoBucket = BucketConstructor(algoFacesConstruct)
	# print(listOfBuckets == algoBucket.listOfListOfFacesSharingEdges)
	# algo = TernaryTreeEdgeConstruct(listOfFacesAsNode[0])
	# pickle.dump(algo.FANInit,open('FANInit.txt', 'wb'))

	# groupSameEdges = tmp