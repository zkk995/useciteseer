#!/usr/bin/python
import os
import sqlite3 as sqlite	
try:
	import MySQLdb
except: 
	print 'can not use mysql'

''' connect sql database  '''
hostname = 'localhost'
username = 'zkk'
password = 'zkk'

dbpath = './'

def connectdb(dbtype='mysql'):
	if dbtype=='mysql':
		conn = MySQLdb.connect(hostname, username, password)
		db = conn.cursor()
		db.execute("use dbCiteSeer;")	
		conn.text_factory = str
		return conn,db
	if dbtype=='sqlite':
		dbfile =dbpath+'/CiteSeer.db'
		conn = sqlite.connect(dbfile)
		db = conn.cursor()
		conn.text_factory = str	
		return conn,db
	print "error: dbtype = mysql or slqite "
	exit()

def int2bin(data):
	return chr(data&255)+chr((data>>8)&255)+chr((data>>16)&255)+chr((data>>24)&255)

def query_db(dbtype='mysql'):
	conn,db=connectdb(dbtype)

	sqlcmd = "select count(*) from CiteSeer;"	
	db.execute(sqlcmd)
	lens=db.fetchone()[0]	
	print ' total num:', lens 

	sqlcmd = "select KEY_,RELATIONS_ from CiteSeer;"
	db.execute(sqlcmd)
	
	keys=[0]*lens	
	keymap={};
	cite=['']*lens

	k=0;res=db.fetchone()
	while not res==None:	
		key,relations=res
		keymap[key]=k
		keys[k]=key
		cite[k]=relations
		k+=1
		res=db.fetchone()
		
	print 'finish query_db'	
	citemap=['']*lens	
	k=0
	while k<lens:
		relations=cite[k].split('_')
		for key in relations:
			if keymap.has_key(key):
				citemap[k]+=int2bin(keymap[key])
		k+=1  
	return keys,citemap

def citemat(dbtype='sqlite',outpath='./'):
	import time
	start =time.clock()	
	keys,citemap=query_db(dbtype)
	print "Times used:", (time.clock()-start)
	
	lens=len(keys)	
	Jc=[0]*(lens+1)
	count = [ len(citemap[j])/4  for j in range(lens) ]
	
	Jc_=int2bin(0)
	for j in range(lens):
		Jc[j+1]=Jc[j]+count[j]
		Jc_+=int2bin(Jc[j+1])		
	Ir=''.join(citemap)	

	fp=open(outpath+"info.txt",'w')
	fp.write('\n'.join(keys))
	fp.close()

	fp=open(outpath+"Jc.bin",'wb')
	fp.write(Jc_)
	fp.close()

	fp=open(outpath+"Ir.bin",'wb')
	fp.write(Ir)
	fp.close()	
	
	num=str(lens)+"\n"+str(lens)+"\n"+str(len(Ir)/4)+"\n"
	fp=open(outpath+"word_doc_entry.txt",'w')
	fp.write(num)
	fp.close()

	print "Times used:", (time.clock()-start)

if __name__ == '__main__':
	outpath='databin/'
	if not os.path.exists(outpath):os.makedirs(outpath)
	citemat('mysql',outpath=outpath)

