#!/usr/bin/python
import time
import sys
import fitsio
import aplpy
import os
import gc
from multiprocessing import Pool
import pyfits
#import subprocess
#import shutil

#read and save image preview of a fits file (using aplpy)
def save_fits_preview(filename): 
	print filename
	if os.path.isfile('/picard_preview/'+filename.split('.')[0]+'.png'):
		print "preview exist for:"+filename
	else:	
		if filename.split('.')[-1] == 'gz' and filename.split('.')[-3]=='fits':
			
			try:
				fits=pyfits.open(filename)
				Fig=aplpy.FITSFigure(fits[0].data)
				fits.close()
				Fig.hide_tick_labels()
				Fig.hide_axis_labels()
				Fig.show_colorscale(cmap='gist_heat')
				f='/picard_preview/'+filename.split('.')[0]+'.png'
				d=os.path.dirname(f)
				if not os.path.exists(d):
					os.makedirs(d) 
				Fig.save('/picard_preview/'+filename.split('.')[0]+'.png')
				Fig.close()
				#time.sleep(5)
				#del Fig
				#gc.collect()
			except:
				print "Error: Oops! no imege preview for:"+filename
				f_log=open('picard_db_log.txt','a')
				f_log.write('Error: Oops! no imege preview for:'+filename+'\n')
				f_log.close()
			#"""Generate Solar png files from fits files"""
	    	#command = "/home/sli/Downloads/ds9 "+filename+" -geometry 512x512 -zoom to fit -view info no -view panner no -view magnifier no -view buttons no -cmap heat -zscale -colorbar no -bg black -export png "+filename.replace(".fits",".png")+" -exit"
	    	#process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	    	#file_fits.close()
		else:
			f_log=open('picard_db_log.txt','a')
			f_log.write('ERROR: file type error in creating fits preview: '+filename+'\n')
			f_log.close()




#read and save header information of fits files into a .sql file (using fitsio)
def extract_fits_header_into_sql(filename):
	#print filename
	if filename.split('.')[-1] == 'gz' and filename.split('.')[-2]=='fits':
		print filename
		header_all={}
		try:
			header_all=fitsio.read_header(filename)
		except:
			print "Error: Oops! error in reading header information:"+filename
			f_log=open('picard_db_log.txt','a')
			f_log.write('Error: Oops! error in reading header information:'+filename+'\n')
			f_log.close()
		if header_all!={}:	
			header_useful={
			'filename':"'"+str(filename.split('/')[-1])+"'",
			'dir_fits':"'"+"/sitools/datastorage/user/storagefitspicardsol/"+"/".join(filename.split('/')[2:])+"'",
			'dir_preview':"'"+"/sitools/datastorage/user/storagepreviewpicardsol/"+"/".join(filename.split('/')[2:]).split('.')[0]+'.png'+"'",
			#'naxis1':str(header_all['NAXIS1']),
			#'naxis2':str(header_all['NAXIS2']),
			#'revision':"'"+str(header_all['REVISION'])+"'",
			'instrume':str(check(header_all,'INSTRUME',filename)),
			'telescop':str(check(header_all,'TELESCOP',filename)),
			'datetimeobs':"'"+str(check(header_all,'DATE-OBS',filename))+"'",       
			#'timeobs':"'"+str(check(header_all,'DATE-OBS',filename)).split('T')[1]+"'",
			'obs_mode':str(check(header_all,'OBS_MODE',filename)),       
			'obs_type':str(check(header_all,'OBS_TYPE',filename)),                 
			'level_pro':str(check(header_all,'LEVEL',filename)),
			'lambda':str(check(header_all,'WAVELNTH',filename)), 
			'exposure':str(check(header_all,'EXPOSURE',filename)),   
			'noimage':str(check(header_all,'NOIMAGE',filename)), 
			'xcenter':str(check(header_all,'XCENTER',filename)),
			'ycenter':str(check(header_all,'YCENTER',filename)),	
			#'r_sun':str(header_all['R_SUN']),
			#'rev_in':"'"+str(header_all['REV_IN'])+"'",
			#'file_co':"'"+str(header_all['FILE_CO'])+"'",
			#'file_ffl':"'"+str(header_all['FILE_FFL'])+"'",
			'obs_alt':str(check(header_all,'OBS_ALT',filename)), 
			'dsun':str(check(header_all,'DSUN',filename)),
			'earth_d':str(check(header_all,'EARTH_D',filename)),
			'obs_cr':str(check(header_all,'OBS_CR',filename))
			}
			f_sql=open('picardsol_db.sql','a')
			keys=','.join(header_useful.keys())
			values=','.join(header_useful.values())
			f_sql.write('INSERT INTO picard_play ('+keys+') VALUES ('+values+');'+'\n')	
			f_sql.close()
	else: 	
		f_log=open('picard_db_log.txt','a')
		f_log.write('ERROR: file type error in extracting fits header: '+filename+'\n')
		f_log.close()

def check(header_all,name,filename):
	try:
		if name=='WAVELNTH' or name=='EXPOSURE' or name=='XCENTER' or name=='YCENTER' or name=='OBS_ALT' or name=='DSUN' or name=='EARTH_D' or name=='OBS_CR' or name=="DATE-OBS":
			return header_all[name]
		else:
			return "'"+header_all[name].replace(" ","")+"'"
	except:
		#print "Error: Oops! error in getting header information:"+filename
		f_log=open('picard_db_log.txt','a')
		f_log.write('Error: Oops! error in getting header information: '+filename+' '+name+'\n')
		f_log.close()
		return 'NULL'	

def getwl(filename):
	if filename.split('.')[-1] == 'fits':
		try:
			header_all=fitsio.read_header(filename)
		except:
			print "Error: Oops! error in reading header information:"+filename
			f_log=open('picard_db_log.txt','a')
			f_log.write('Error: Oops! error in reading header information:'+filename+'\n')
			f_log.close()

		if header_all['lambda'] not in wl:
			wl.append(header_all['lambda'])
			f_wl=open('picard_wl.txt','a')
			f_wl.write(str(header_all['lambda'])+'\n')
			f_wl.close()	
	else: 	
		f_log=open('picard_db_log.txt','a')
		f_log.write('ERROR: file type error in extracting fits header: '+filename+'\n')
		f_log.close()		
'''
def rename(filename):
	#print filename
	#filename=filename.split('/')[-1]
	portion = os.path.splitext(filename)
	print portion[0]
	os.rename(filename,portion[0])
'''
#explore the folders iteratively
def folder_travel(folder_path): 
	namelist=os.listdir(folder_path)
	for name in namelist: 
		if os.path.isdir(folder_path+'/'+name):
			print folder_path+'/'+name
			folder_travel(folder_path+'/'+name)
		elif name.split('.')[-1] == 'gz' and name.split('.')[-3]=='fits':
			#listfits.append(folder_path+'/'+name)	
			save_fits_preview(folder_path+'/'+name)
			#extract_fits_header_into_sql(folder_path+'/'+name)
			#getwl(folder_path+'/'+name)

#start the function by using "./extract_fits_preview+header.py 'fits_files_root_directory' 'database sql file saving directory'"
#ex: ./extract_fits_preview+header.py /home/sli/fits /home/sli/Desktop
def main():
	fitsdir=[]
	if sys.argv[1]:
		fitsdir.append(sys.argv[1])
	'''
	if sys.argv[2]:
		fitsdir.append(sys.argv[2])
		
	if sys.argv[3]:	
		fitsdir.append(sys.argv[3])
	if sys.argv[4]:		
		fitsdir.append(sys.argv[4])
	if sys.argv[5]:	
		fitsdir.append(sys.argv[5])
	if sys.argv[6]:	
		fitsdir.append(sys.argv[6])
	if sys.argv[7]:	
		fitsdir.append(sys.argv[7])
	'''
	if os.path.isfile('picardsol_db.sql'):
		f_sql=open('picard_db.sql','a')
		#f_sql.write('/*'+fitsdir+'*/'+'\n')
		f_sql.close()
	else:	
		f_sql=open('picardsol_db.sql','w')
		f_sql.write('/*picard project n1 database sql code*/'+'\n\n\n')
		#f_sql.write('/*'+fitsdir+'*/'+'\n')
		f_sql.close()
	if os.path.isfile('picard_db_log.txt'):
		f_log=open('picard_db_log.txt','a')
		#f_log.write('***'+fitsdir+'***'+'\n')
		f_log.close()
	else:
		f_log=open('picard_db_log.txt','w')
		f_log.write('***PICARD n1 project database -- log***'+'\n\n\n')
		#f_log.write('/*'+fitsdir+'*/'+'\n')
		f_log.close()
	if os.path.isfile('picard_wl.txt'):
		f_wl=open('picard_wl.txt','a')
		#f_wl.write('/*'+fitsdir+'*/'+'\n')
		f_wl.close()
	else:	
		f_wl=open('picard_wl.txt','w')
		f_wl.write('/*picard project all wavelength*/'+'\n\n\n')
		#f_wl.write('/*'+fitsdir+'*/'+'\n')
		f_wl.close()
		
	global listfits
	listfits=[]
	global wl
	wl=[]
	for d in fitsdir:
		folder_travel(d) #start explore folders
	#Pool().map(rename,listfits)
	#Pool().map(extract_fits_header_into_sql,listfits)
	#Pool().map(save_fits_preview,listfits)
	#Pool().map(getwl,listfits)

if __name__ == '__main__':
	main()