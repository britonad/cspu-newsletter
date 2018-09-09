import os
import logging

from core.settings import LOGS_DIR

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(os.path.join(LOGS_DIR, 'newsletter.log'))
fmt = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)
fh.setFormatter(formatter)

logger.addHandler(fh)
