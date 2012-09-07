def file2str(fname ,mode = 'r'):
	fobj = open(fname,mode)
	fstr = fobj.read()
	fobj.close()
	return fstr

def str2file(fname, string, mode = 'w'):
	fobj = open(fname,mode)
	fobj.write(string)
	fobj.close()
