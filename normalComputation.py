import numpy as np



def computeNormal(simplexe):
	e1 = simplexe[0]-simplexe[2]
	e2 = simplexe[1]-simplexe[2]

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

def computeNormalMultiple(arrayOfSimplexes):
	e1 = arrayOfSimplexes[0] - arrayOfSimplexes[2]
	e2 = arrayOfSimplexes[1] - arrayOfSimplexes[2]

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