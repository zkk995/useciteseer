#!/usr/bin/python
#coding=utf-8
# downloadciteseer.py

import urllib2
import os,re


resumptionfile="resumptionToken.txt"
xmldata="citeseerdata.xml"

url="http://citeseerx.ist.psu.edu/oai2?verb=ListRecords&metadataPrefix=oai_dc"
baseUrl="http://citeseerx.ist.psu.edu/oai2?verb=ListRecords&resumptionToken="
pattern = re.compile("<resumptionToken>(.*?)</resumptionToken>");

def downURL(url, filename):
	print "Download %s, save as %s"%(url, filename)
	try:
		fp = urllib2.urlopen(url)
	except:
		print "download exception"
		return 0
	paths = os.getcwd()+'/'+filename
	op = open(paths, "w")
	while 1:
		s = fp.read()
		if not s:break
		op.write(s)
	fp.close( )
	op.close( )
	return 1
	
def dataappend(xmldata,xmldata_tmp):
	fp=open(xmldata_tmp)
	op = open(xmldata, "a")
	while 1:
		s = fp.read()
		if not s:break
		op.write(s)
	fp.close( )
	op.close( )

def readtoken(resumptionfile):
	fp=open(resumptionfile)
	line=fp.read()
	fp.close()
	token=line.split('\n')[0]
	return token


if not os.path.isfile(resumptionfile):fp=open(resumptionfile,'w');fp.close()
xmldata_tmp="citeseerdata_.xml"
k=0
while 1:
	# download data
	token=readtoken(resumptionfile)
	if len(token)>1:url=baseUrl+token
	else:
		if k>0:break
	
	downURL(url,xmldata_tmp)
		
	# retrive the resumption token
	token=''
	fp=open(xmldata_tmp)
	for s in fp:
		us = pattern.findall(s)
		if us:	
			token=us[0]
	fp.close()
	if token=='':break
	
	# save data
	dataappend(xmldata,xmldata_tmp)
	
	fp2=open(resumptionfile,'w')
	fp2.write(token)
	fp2.close()     

	# print result
	k+=1
	print "finish ", k," parts" 
