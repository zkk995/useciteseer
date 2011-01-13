#!/usr/bin/python
import CiteSeerImporter as cs
import time
import splitCiteSeer as spcs

'''splitdata'''  
#spcs.splitCiteSeer(xml="/media/tool/learningcode/citeseerdata.xml")
files = ["xml/"+str(i)+'.xml' for i in range(1,72+1)]

''' import into mysql'''
start = time.clock()

cs.hostname = 'localhost'
cs.username = 'zkk'
cs.password = 'zkk
cs.CiteSeerImporter(dbtype='mysql',files=files)

print "Time used:",(time.clock() - start)


''' import into sqlite db files'''
start = time.clock()

cs.outpath='./'
cs.CiteSeerImporter(dbtype='sqlite',files=files)

print "Time used:",(time.clock() - start)
