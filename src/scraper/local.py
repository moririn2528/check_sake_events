from dotenv import load_dotenv
from logging.config import fileConfig
from google.auth import default
from logging import getLogger


from const import ROOT_DIR
from main import crawl


if __name__ == "__main__":
    credentials, _ = default()
    fileConfig(ROOT_DIR.joinpath("settings/logging_local.conf"))
    load_dotenv(dotenv_path=ROOT_DIR.joinpath("settings/local.env"))
    logger = getLogger(__name__)
    logger.warning(credentials.token)
    crawl()
