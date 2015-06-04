#!/usr/bin/python
import Image
import os
import sys

def resizetosmall(file_name):
	infile = file_name
	infile_array = file_name.split('.')
	infile_array[-2] = infile_array[-2] + '_small'
	outfile = '.'.join(infile_array)
	print 'Input file: ' + infile
	if os.path.isfile(outfile):
		print 'Small image already existes: '+infile
	else:
		print 'Output file: ' + outfile
		im = Image.open(infile)
		(x,y) = im.size #read image size
		x_s = 50 #define standard width
		y_s = y * x_s / x #calc height based on standard width
		out = im.resize((x_s,y_s),Image.ANTIALIAS) #resize image with high-quality
		out.save(outfile)

def folder_travel(folder_path): 
	namelist=os.listdir(folder_path)
	for name in namelist: 
		if os.path.isdir(folder_path+'/'+name):
			print folder_path+'/'+name
			folder_travel(folder_path+'/'+name)
		elif name.split('.')[-1] == 'png' and name.find('small')==-1:	
			resizetosmall(folder_path+'/'+name)


def main():
	fitsdir=[]
	if sys.argv[1]:
		fitsdir.append(sys.argv[1])		
	global listfits
	listfits=[]
	global wl
	wl=[]
	for d in fitsdir:
		folder_travel(d)

if __name__ == '__main__':
	main()