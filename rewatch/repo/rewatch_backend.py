import json
import logging
import os
from datetime import date
from typing import Dict, List, Optional, Tuple

import boto3
from boto3.dynamodb.conditions import Key

from rewatch.entities.rewatch_entity_model import (MessageBoardPost,
                                                   SecretConfig)


def load_message_board_posts() -> Tuple[
    Optional[List[MessageBoardPost]]]:
    """Loads the MessageBoardPost from persisted storage
    None if unexpected error
    [] if no MessageBoardPost entities were found
    """
    logging.info(f"load_message_board_posts - invocation begin")
    dynamodb_table = boto3.resource(
        "dynamodb", 
        os.environ.get("AWS_REGION")).Table(
            "prod_toonami_ratings"
        )

    logging.info("load_message_board_posts - obtained table resource")

    dynamodb_response = dynamodb_table.query(
        KeyConditionExpression=Key("PK").eq(
            "rewatch#")
    )

    logging.info("load_message_board_posts - obtained dynamodb_response")

    if len(dynamodb_response["Items"]) == 0:
        logging.info(
            "load_message_board_posts - dynamodb_response Items list has no elements"
        )
        return([])

    logging.info(f"load_message_board_posts - invocation end")
    return(None)



def _populate_secret_config(sdk_response: Dict) -> SecretConfig:
    """https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_secret_value
    """
    secret_config = SecretConfig()

    deserialized_secret_string = json.loads(
        sdk_response["SecretString"]
    )

    logging.info(f"_populate_secret_config - deserialized secrets")
    
    secret_config.reddit_client_id = deserialized_secret_string[
        "reddit_api_key"
    ]
    
    secret_config.reddit_client_secret = deserialized_secret_string[
        "reddit_api_secret"
    ]
    secret_config.reddit_password = deserialized_secret_string[
        "reddit_api_username"
    ]
    secret_config.reddit_username = deserialized_secret_string[
        "reddit_api_password"
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



if __name__ == "__main__":
    import logging
    import os
    from time import strftime
    os.environ["AWS_REGION"] = "us-east-1"
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s.%(msecs)03d" + strftime("%z") + " | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S", level=logging.INFO
    )
    secret_config = load_secret_config()

    print(secret_config)

