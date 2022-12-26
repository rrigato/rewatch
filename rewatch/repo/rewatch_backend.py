import json
import boto3
import logging
from datetime import date
from typing import Dict, List, Optional, Tuple

from rewatch.entities.rewatch_entity_model import (MessageBoardPost,
                                                   SecretConfig)


def load_message_board_posts() -> Tuple[
    Optional[List[MessageBoardPost]], Optional[str]]:
    """Loads the MessageBoardPost from persisted storage
    """
    logging.info(f"load_message_board_posts - invocation begin")
    
    logging.info(f"load_message_board_posts - invocation end")
    return(Tuple[Optional[List[MessageBoardPost]], Optional[str]])



def _populate_secret_config(sdk_response: Dict) -> SecretConfig:
    """https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_secret_value
    """
    secret_config = SecretConfig()

    deserialized_secret_string = json.loads(
        sdk_response["SecretString"]
    )

    logging.info(f"_populate_secret_config - deserialized secrets")
    
    secret_config.reddit_client_id = deserialized_secret_string[
        "reddit_client_id"
    ]
    
    secret_config.reddit_client_secret = deserialized_secret_string[
        "reddit_client_secret"
    ]
    return(secret_config)



def load_secret_config() -> Optional[SecretConfig]:
    """Returns None if unexpected error
    """
    try:
        
        secretsmanager_client = boto3.client(
            service_name="secretsmanager", 
            region_name="us-east-1"
        )

        sdk_secret_response = secretsmanager_client.get_secret_value(
            SecretId="/prod/v1/credentials"
        )
        logging.info(f"load_secret_config - obtained config")
        

        return(_populate_secret_config(
            sdk_secret_response
        ))
    except Exception as errror_suppression:
        logging.exception(errror_suppression)
        return(None)
