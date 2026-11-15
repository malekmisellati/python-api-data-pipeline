import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="data/pipeline.log",
    filemode="a"
)

logger = logging.getLogger(__name__)