import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fh = logging.StreamHandler()
fmt = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)
fh.setFormatter(formatter)

logger.addHandler(fh)
