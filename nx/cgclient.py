import os
import time
import requests

from .core import *

def cg_download(target_path, method, **kwargs):
    start_time = time.time()
    target_dir = os.path.dirname(target_path)
    cg_server = config.get("cg_server", "https://cg.immstudios.org")
    if not os.path.isdir(target_dir):
        try:
            os.makedirs(target_dir)
        except Exception:
            logging.error("Unable to create output directory {}".format(target_dir))
            return False
    url = "{}/render/{}/{}".format(
            cg_server,
            config["site_name"],
            method
        )
    response = requests.get(url, params=kwargs)
    if response.status_code != 200:
        logging.error("CG Download failed with code {}".format(response.status_code))
        return False
    with open(target_path, "wb") as f:
        f.write(response.content)

    logging.info("CG {} downloaded in {:.02f}s".format(method, time.time() - start_time))
    return True

