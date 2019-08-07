import numpy as np 
from scipy.spatial import ConvexHull
import normalComputation
import localConstraint

class GlobalConstraint(object):
	"""docstring for globalConstraint
		the global constraint can give the "outward" orientation of a face of an arbitrary mesh whose faces are belonging to the border of a connex 3D form
	"""
	def __init__(self, faces,vertices):
		self.facesOriginalHull = faces
		self.facesOriginalHull = np.sort(self.facesOriginalHull)
		self.vertices = vertices
		self.constructConvexHull()

	def constructConvexHull(self):
		hull = ConvexHull(self.vertices)
		self.facesConvexHull = np.sort(hull.simplices,axis=1)

	def checkCommonFaces(self):
		for i in range(self.facesConvexHull.shape[0]):
			for j in range(self.facesOriginalHull.shape[0]):
				if (np.all(self.facesConvexHull[i]==self.facesOriginalHull[j])):
					return (i,j)
	
	def computeNormalOutwardOrientedConvexHull(self,faceConvexHull):
		# verticesFace = self.vertices[faceConvexHull]

		IndexverticeNotInFaceConvexHull = -1
		for i in range(self.vertices.shape[0]):
			if (i not in faceConvexHull):
				IndexverticeNotInFaceConvexHull = i;
				break
		verticesFaceConvexHull = self.vertices[faceConvexHull]
		verticeNotInFaceConvexHull = self.vertices[IndexverticeNotInFaceConvexHull]

		normalNonOriented = normalComputation.computeNormal(verticesFaceConvexHull)

		scalarProduct = np.sum(np.array(normalNonOriented)* (verticesFaceConvexHull[0]-verticeNotInFaceConvexHull))

		# insidePt = np.matmul((0.25,0.25,0.5),verticesFaceConvexHull)
		insidePt = self.getInsidePointOfSimplexe(verticesFaceConvexHull)
		if (scalarProduct>0):
			return insidePt, np.array(normalNonOriented)
		else : 
			return insidePt, -np.array(normalNonOriented)

	def getInsidePointOfSimplexe(self,verticesSimplexe):
		insidePt = np.matmul((0.25,0.25,0.5),verticesSimplexe)
		return insidePt


	def getFaceOnOriginalHullOutwardlyOriented(self):
		"""for the first face of the convex hull's list "self.facesConvexHull" that is not in the original hull, return a face of the original hull with its normal that is oriented 
		inward the (unique) 3D connexe component that is inside the convex hull and outside the original hull,
		for the returned face, the normal is oriented outward th original hull
		 """

		for el in self.facesConvexHull:
			if (el not in self.facesOriginalHull):
				faceNotInOriginalHull = el
		for el in self.facesOriginalHull:
			if (el not in self.facesConvexHull):
				faceNotInConvexHull = el			

		face1 = [faceNotInOriginalHull[0],faceNotInOriginalHull[1],faceNotInConvexHull[2]]
		face2 = [faceNotInOriginalHull[0],faceNotInConvexHull[1],faceNotInConvexHull[2]]


		facesConnected = [faceNotInOriginalHull,face1,face2,faceNotInConvexHull] # list of edge-connected face, the first one is on the convex hull and not in the original hull, the last one is on the original hull and not in the convex hull

		verticesFacesConnected = [self.vertices[face] for face in facesConnected]

		simplexes = [( self.getInsidePointOfSimplexe(verticesFace),np.array(normalComputation.computeNormal(verticesFace)) ) for verticesFace in verticesFacesConnected]

		simplexes[0] = tuple(self.computeNormalOutwardOrientedConvexHull(faceNotInOriginalHull))

		outwardOrientation = -1*np.product(np.array([ localConstraint.checkOrientationConnectedSimplexe(simplexes[i],simplexes[i+1]) for i in range(2)]))

		return faceNotInConvexHull,simplexes[-1][0],simplexes[-1][1]*outwardOrientation


	# def compute(self):
	# 	result = self.checkCommonFaces()
	# 	if (result is not(None)):
	# 		self.faceIndex = result[1]
	# 		self.face = faces[self.faceIndex]
			# self.orientedNormal = self.computeNormalOutwardOrientedConvexHull(self.face)

		# else :

		# 	result = self.checkCommonEdges() # could not exit !




if __name__ == '__main__':
	faces = np.load("bunny_faces.npy")
	vertices = np.load("bunny_vertices.npy")

	algoGlobalConstraint = GlobalConstraint(faces,vertices)
	

	#check if there is a common face

