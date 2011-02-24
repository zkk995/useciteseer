#!/usr/bin/python
#coding=utf-8
# python version< 3.0
# splitCiteSeer.py

import os
def splitCiteSeer(xml="citeseerdata.xml",outpath="xml/",size=40):
	btoken="<ListRecords>"
	stoken="</ListRecords>"

	if not os.path.exists(outpath):os.makedirs(outpath)
	n500=0;intoken=0
	fp=open(xml)
	for line_ in fp:
		line=line_.strip()
		if line==btoken:
			intoken=1;
			sp=open(outpath+'/'+str(1+n500/size)+'.xml','a')
			n500+=1
		if intoken:
			sp.write(line_)
		if line==stoken:
			sp.close()
			intoken=0
			if n500%size==size-1:
				print "finish ",str(1+n500/size),"parts"	
	fp.close()
	
if __name__ == '__main__':
	splitCiteSeer(size=40)
