import numpy as np 
import globalConstraint
import localConstraint
import rootedBinaryTreeConstruct
import faceStructure
import normalOrientationOnTree
import cPickle as pickle
import time
import pdb
# def mainAlgo():
	# pass

if __name__ == '__main__':

	start= time.time()

	facesWithRedundancy = np.load("bunny_faces.npy")
	faces,indexOfFacesWithRedundancyToIndexOfFaces = np.unique(np.sort(facesWithRedundancy,axis=1),axis=0,return_inverse=True) # remove redundant faces
	vertices = np.load("bunny_vertices.npy")
	algoFacesConstruct = faceStructure.FacesInfo(faces,vertices)



	algoBucket = rootedBinaryTreeConstruct.BucketConstructor(algoFacesConstruct)

	listOfFacesAsNode = algoBucket.listOfFacesAsNode

	# facesWithRedondancy = np.load("bunny_faces.npy")
	# faces = np.unique(np.sort(facesWithRedondancy,axis=1),axis=0) # remove redundant faces
	# vertices = np.load("bunny_vertices.npy")
	# algoFacesConstruct = FacesInfo(faces,vertices)
	# listOfFaces = algoFacesConstruct.listOfFaces
	# listOfFacesAsNode = [FaceAsNode(el) for el in listOfFaces]

	#construct face with normal outwardly oriented using the the global constraint computed by algoGlobalConstraint
	# the face is represented by the FaceInfo structure
	algoGlobalConstraint = globalConstraint.GlobalConstraint(faces,vertices)

	face, normalOriented = algoGlobalConstraint.getFaceOnOriginalHullOutwardlyOriented()

	# pdb.runcall(algoFacesConstruct.lookForFaceInfoWithSameEdgeAndUpdateNormal,face,normalOriented)

	faceInfoOO = algoFacesConstruct.lookForFaceInfoWithSameEdgeAndUpdateNormal(face,normalOriented)

	initFace = algoBucket.findInitFace(faceInfoOO)


	binaryConstructAlgo = rootedBinaryTreeConstruct.RootedBinaryTreeEdgeConstruct(initFace)


	normalOrientationOnTree.OrientationComputer(binaryConstructAlgo.FANInit)
	treeToListResultConverter = normalOrientationOnTree.TreeToListResultConverter(binaryConstructAlgo.FANInit)

	listNormalsAllFaces =  treeToListResultConverter.listNormals[indexOfFacesWithRedundancyToIndexOfFaces] # listNormals and faces are indexed with correspondance

	faceNormalsFile = "faceNormals.npy"
	np.save(faceNormalsFile,listNormalsAllFaces)


	#compute Normals on vertices 
	for el in listOfFacesAsNode:
		for vertices in el.faceInfo.vertices:
			vertices.normalsFaces.append(el.faceInfo.normal)

	for vertice in algoFacesConstruct.listVertices:
		vertice.normal = np.mean(np.array(vertice.normalsFaces),axis=0)

	nbVertices = (algoFacesConstruct.vertices).shape[0]

	a=np.array([[el.indexVertice,el.normal] for el in algoFacesConstruct.listVertices])

	A = set(np.linspace(0,nbVertices-1,nbVertices))

	B = set(a[:,0])

	acomp = list(A-B)

	aRes = np.array(list(A-B)).reshape(-1,1).astype("int")

	aRes = np.array([(el[0],np.zeros(3)) for el in aRes])

	e = np.vstack((a,aRes))

	z = e[np.argsort(e[:,0]),:]

	listNormalVertexes = [[el[1][0],el[1][1],el[1][2]] for el in z]

	vertexNormalsFile = "vertexNormals.npy"
	np.save(vertexNormalsFile,listNormalVertexes)

	stop=time.time()

	print(stop-start)
	# treeToListResultConverter.saveNormalOfFaces()

	# # construct a ternary tree starting by the node (face with correctly oriented normal)
	# start=time.time()
	# algo = ternaryTreeConstruct.TernaryTreeEdgeConstruct(listOfFaces,faceInfoOO)
	# stop=time.time()

	# pickle.dump(algo.FANInit,open('FANInit.txt', 'wb'))

	# normalOrientationOnTree.OrientationCompute(algo.FANInit)
	# treeToListResultConverter = normalOrientationOnTree.TreeToListResultConverter(algo.FANInit)
	# showAlgo = normalOrientationOnTree.TreeToListResultConverter(algo.FANInit)

	# showAlgo = TreeToListResultConverter(FAN)


	# ternaryTreeConstruct.getFirstNode
	# indexFaceWithKnownOrientation = np.where(np.all(np.sort(faces,axis=1)==face[0],axis=1))[0][0]
	# print(indexFaceWithKnownOrientation)

