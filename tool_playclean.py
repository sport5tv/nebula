#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nebula import *

def get_pairs(id_channel, db=False):
    channel_config = config["playout_channels"][id_channel]
    db = db or DB()
    db.query("SELECT a.id_object, m.value FROM nx_assets AS a, nx_meta AS m WHERE a.id_object = m.id_object AND m.object_type=0 AND m.tag=%s ORDER BY a.ctime ASC", [channel_config["playout_spec"]])
    for id_master, id_playout in db.fetchall():
        mas = Asset(id_master, db=db)
        ply = Asset(id_playout, db=db)
        yield mas, ply


def get_scheduled(id_channel, db=False):
    db = db or DB()

    from_time = int(time.time()) - (48*3600) # nemazem veci, co se poustely v poslednich dvou dnech
    db.query("""
SELECT DISTINCT(i.id_asset) FROM nx_items AS i, nx_events AS e
WHERE e.id_channel = %s
AND   e.id_magic = i.id_bin
AND   e.start > %s
""", [id_channel, from_time]
        )

    return [r[0] for r in db.fetchall()]




def clean(assets=[]):
    i = 0
    s = 0
    for asset in assets:
        if i > 100:
            break

        if type(asset) != Asset:
            logging.warning("{} is not valid asset".format(asset))
            continue

        if asset["status"] != ONLINE:
            continue

        spath = asset.file_path
        tpath = os.path.join(storages[asset["id_storage"]].local_path, "media.trash", os.path.basename(spath))
        logging.info("Moving {} to {}".format(spath, tpath))
        try:
            os.rename(spath, tpath)
        except:
            log_traceback()

        s +=  float(asset["file/size"])
        i += 1

    logging.goodnews("{} GB Freeed".format((s/(1024.0**3))))




def unlist(id_channel):
    db = DB()
    scheduled = get_scheduled(id_channel)
    cscheduled = 0
    for mas, ply in get_pairs(id_channel, db=db):
        if mas["status"] in [TRASHED, ARCHIVED]:
            yield ply
            continue

        if mas.id in scheduled:
            cscheduled += 1
            continue

        yield ply





if __name__ == "__main__":
    clean(unlist(1))
