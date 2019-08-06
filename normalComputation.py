import numpy as np


def computeNormal(edges):
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
	normal = (x/det,y/det,1)
	norm = np.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
	normal = [el/norm for el in normal]
	return normal