import logging
from datetime import date
from typing import List, Optional, Tuple

from rewatch.entities.rewatch_entity_model import (MessageBoardPost,
                                                   SecretConfig)


def load_message_board_posts() -> Tuple[
    Optional[List[MessageBoardPost]], Optional[str]]:
    """Loads the MessageBoardPost from persisted storage
    """
    logging.info(f"load_message_board_posts - invocation begin")
    
    logging.info(f"load_message_board_posts - invocation end")
    return(Tuple[Optional[List[MessageBoardPost]], Optional[str]])



def load_secret_config() -> Optional[SecretConfig]:
    """Returns None if unexpected error
    """
    logging.info(f"load_secret_config - invocation begin")
    secretsmanager_client = boto3.client(
        service_name="secretsmanager", 
        region_name="us-east-1"
    )
    logging.info(f"load_secret_config - invocation end")
    return(None)

