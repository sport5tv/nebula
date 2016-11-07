#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from nx.objects import *
db =DB()

db.query("SELECT a.id_object FROM nx_asrun AS r INNER JOIN nx_assets AS a ON a.id_object = r.id_asset INNER JOIN nx_meta AS m ON m.id_object = a.id_object WHERE m.tag LIKE 'identifier/main' AND a.origin='Production' AND a.id_folder in (1,2) AND r.start>=1420066800 ORDER BY m.tag")

seen = []

for id_object, in db.fetchall():
    a = Asset(id_object, db=db)
    
    if a["identifier/main"] not in seen:
    	print a["title"]+';'+a["identifier/main"]
    	seen.append(a["identifier/main"])
