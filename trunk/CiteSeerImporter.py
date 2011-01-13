#!/usr//bin/python
import sqlite3 as sqlite
import re,glob
try:
	import MySQLdb
except: 
	print 'can not use mysql'

''' connect sql database  '''
hostname = 'localhost'
username = 'zkk'
password = 'zkk'

datapath ='/media/tool/learningcode/xml/'
outpath='/media/tool/learningcode/'


'''
identifier
datestamp  
dc:creator
dc:title
dc:relation
dc:source 

create table CiteSeer(
KEY_	        varchar(20)	        not null primary key, 
DATE_	    varchar(32)	        not null, 
TITLE_	    varchar(1000),
SOURCE_	        varchar(512),
CREATORS_	    varchar(1000),
RELATIONS_	    varchar(20000)
);  
'''
''' patterns for these tags    '''
pat_article =re.compile("<record>(.*?)</record>")
pat_key     =re.compile("<identifier>(.*?)</identifier>")
pat_date    =re.compile("<datestamp>(.*?)</datestamp>")
pat_title   =re.compile("<dc:title>(.*?)</dc:title>")
pat_source  =re.compile("<dc:source>(.*?)</dc:source>")

pat_creators =re.compile("<dc:creator>(.*?)</dc:creator>")
pat_relations=re.compile("<dc:relation>(.*?)</dc:relation>")

def importCiteSeer(xml,db):
	contents=xml.read().replace('\n',' ').replace('\r',' ')
	for article in pat_article.findall(contents):
		key=pat_key.search(article).group(1).split(':')[-1]
		date=pat_date.search(article).group(1)
		
		try:title=pat_title.search(article).group(1)
		except:title=''
		try:source=pat_source.search(article).group(1)
		except:source=''
		
		tmp=pat_creators.findall(article)
		if len(tmp)>=10:continue
		creators='_'.join(tmp)
		tmp=pat_relations.findall(article)
		if len(tmp)>=500 or len(tmp)==0:continue
		relations='_'.join(tmp)

		sqlcmd="insert into CiteSeer values('"+key+"','"+date+"','"+title+"','"+source+"','"+creators+"','"+relations+"')"
		try:
			db.execute(sqlcmd)
		except:
			print key

def connectdb(dbtype='sqlite'):
	if dbtype=='mysql':
		conn = MySQLdb.connect(hostname, username, password)
		db = conn.cursor()
		db.execute("drop database if exists dbCiteSeer;")
		db.execute("create database dbCiteSeer;")
		db.execute("use dbCiteSeer;")

		conn.text_factory = str
		db.execute('''
create table CiteSeer(
KEY_	        varchar(20)	        not null primary key, 
DATE_	    varchar(32)	        not null, 
TITLE_	    varchar(1000),
SOURCE_	        varchar(512),
CREATORS_	    varchar(1000),
RELATIONS_	    varchar(20000)
);
''')
		print "mysql is connected."
		return conn,db	
		
	if dbtype=='sqlite':
		dbfile =outpath+'/CiteSeer.db'
		conn = sqlite.connect(dbfile)
		db = conn.cursor()
		conn.text_factory = str
		db.execute('''
create table if not exists CiteSeer
(KEY_ text not null  primary key, 
DATE_ text not null, 
TITLE_ text not null,
SOURCE_ text not null,
CREATORS_ text,
RELATIONS_ text) 
''')
		print "sqlite is connected."
		return conn,db	
	print "error: dbtype = mysql or slqite "
	exit()	
	
import time
def CiteSeerImporter(dbtype,files=glob.glob(datapath+'/*.xml')):
	conn,db=connectdb(dbtype)	
	for filename in files:
		
		print 'to process',filename
		xml = open(filename);
		
		start = time.clock()
		importCiteSeer(xml,db);
		print "Time used:",(time.clock() - start)
		
		xml.close()
		conn.commit()
	db.close()

if __name__=="__main__":
	files=glob.glob(datapath+'/*.xml')
	num_files=len(files);
	files = [datapath+"/"+str(i)+'.xml' for i in range(1,num_files+1)]
	CiteSeerImporter('mysql',files)
