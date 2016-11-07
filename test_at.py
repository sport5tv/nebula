#!/usr/bin/env python
from nx.objects import *

class ATStorage():
    def __init__(self):
        import ftplib
        self.ftp = ftplib.FTP('ftp.sport5.cz','full','Sport5prg0109')
        self.ftp.cwd("Reklama")

    @property
    def files(self):
        return self.ftp.nlst()

    @property 
    def data(self):
        """list of tuples (filename, IDEC, secondary_id, nice name)"""

        for fname in self.files:
            if os.path.splitext(fname)[1] != ".mpg":
                continue
            try:
                l = fname.split("_")
                idec = "AT" + l[0].zfill(6)
                idec2 = int(l[1].strip("#"))
                nicename = " ".join(l[2:]).replace(".mpg", "").encode("utf-8")
            except:
                logging.warning("Strange file name {}".format(fname))

            yield fname, idec, idec2, nicename

    def age(self, fname):
        try:
            mtime = self.ftp.sendcmd('MDTM ' + fname)
        except:
            return 0
        t = time.strptime(mtime[4:], "%Y%m%d%H%M%S")
        return time.time() - time.mktime(t)

    def download(self, fname, target):
        f = open(target, "wb")
        self.ftp.retrbinary("RETR {}".format(fname), f.write)
        f.close()

    def __del__(self):
        self.ftp.quit()






db = DB()
db.query("SELECT m.value FROM nx_meta as m, nx_assets as a WHERE a.origin='Production' and a.id_object = m.id_object and m.object_type = 0 and m.tag='identifier/main' and m.value like 'AT%' ")
idecs = [i[0] for i in db.fetchall()]

at = ATStorage()
i = 0
for fname, idec, idec2, nicename in at.data:
    print fname, idec, idec2, nicename
    if idec in idecs:
        continue

    age = at.age(fname)
    if not age:
        continue

    if age < 3600:
        logging.debug("{} : is pretty new ({} min). skipping".format( idec,  (age/60)))
        continue


    

    continue


    asset = Asset(db=db)
    asset["media_type"] = FILE
    asset["content_type"] = VIDEO

    asset["id_folder"] = 11
    asset["origin"] = "Production"
    asset["title"] = nicename
    asset["commercials/client"] = "ATMedia"
    asset["identifier/main"]    = idec
    asset["identifier/atmedia"] = idec2
    asset["id_storage"] = 1
    asset["path"]= "media.dir/commercials/{}.mpeg".format(asset["identifier/main"])


    logging.info("Downloading {}".format(idec))
    try:
        at.download(fname, asset.file_path)
    except:
        logging.error("Download failed: {}".format(str(sys.exc_info())))
    else:
        asset.save()

