from authenticate import client
from variables import FUNCTION_NAME, FUNCTION_EXTERNAL_ID
from logging_config import configure_logger

logger = configure_logger(__name__)


logger.info(
    client.functions.create(
        name=FUNCTION_NAME,
        external_id=FUNCTION_EXTERNAL_ID,
        folder="./",
        description="Scrape finn realestate data",
        )
    )

