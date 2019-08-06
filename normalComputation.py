import numpy as np


def computeNormal(vectors):
	e1 = vectors[0]
	e2 = vectors[1]

	a = e2[0]
	b = e2[1]
	c = e2[2]


	d = e1[0]
	e = e1[1]
	f = e1[2]

	det = -b*d + e*a

	x = b*f - c*e
	y = c*d - a*f
	normal = (x/det,y/det,1)
	norm = np.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
	normal = [el/norm for el in normal]
	return normal

def computeNormalMultiple(arrayOfVectors):
	e1 = arrayOfVectors[0]
	e2 = arrayOfVectors[1]

	a = e2[:,0]
	b = e2[:,1]
	c = e2[:,2]


	d = e1[:,0]
	e = e1[:,1]
	f = e1[:,2]

	det = -b*d + e*a

	x = b*f - c*e
	y = c*d - a*f


	normal = np.array([x/det,y/det,np.ones(x.shape)])
	norm = np.sqrt(np.sum(normal**2,axis=0))
	normal/=norm
	normal = np.transpose(normal)
	return normal