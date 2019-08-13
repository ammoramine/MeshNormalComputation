import numpy as np 




def checkOrientationConnectedSimplexe(el1,el2):
	"""if the two connected simplexes have normals (or theirs reverses) oriented outwardly ,then return 1 else return -1 """
	ni = el1[0]
	ci = el1[1]

	nj = el2[0]
	cj = el2[1]

	cji = cj-ci
	cij = -cji
	constraint = (cij[0]*nj[0] + cij[1]*nj[1] + cij[2]*nj[2]) * (cji[0]*ni[0] + cji[1]*ni[1] + cji[2]*ni[2])
	if (constraint>0):
		return 1
	elif (constraint<0):
		return -1
	elif (constraint ==0):
		if (ni[0]*nj[0] + ni[1]*nj[1] + ni[2]*nj[2]>0):
			return 1
		else:
			return -1