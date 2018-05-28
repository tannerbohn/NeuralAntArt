

def clip(m, M, val):
	return min(max(val, m), M)

def toHex(cvec):

	rgb = tuple([int(255*v) for v in cvec])

	return '#%02x%02x%02x' % rgb