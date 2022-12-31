import base64
from http.client import HTTPResponse
import json
import logging
import os
from datetime import date
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import boto3
from boto3.dynamodb.conditions import Key

from rewatch.entities.rewatch_entity_model import (MessageBoardPost,
                                                   SecretConfig)




def _populate_message_posts(dynamodb_query_response: Dict) -> List[MessageBoardPost]:
    """populates entity from external persisted storage
    """
    logging.info(f"_populate_message_posts - invocation begin")
    
    message_board_posts: List[MessageBoardPost] = []

    for dynamodb_item in dynamodb_query_response["Items"]:
        
        new_message_post = MessageBoardPost()

        new_message_post.post_message = dynamodb_item["post_title"]
        new_message_post.post_title = dynamodb_item["post_message"]

        message_board_posts.append(new_message_post)

    logging.info(
        f"_populate_message_posts - len(message_board_posts) - " +
        f"{len(message_board_posts)}")

    return(message_board_posts)



def load_message_board_posts() -> Optional[
        List[MessageBoardPost]]:
    """Loads the MessageBoardPost from persisted storage
    None if unexpected error
    [] if no MessageBoardPost entities were found
    """
    try:

        
        dynamodb_table = boto3.resource(
            "dynamodb", 
            os.environ.get("AWS_REGION")).Table(
                "rewatch_shared_table"
            )

        logging.info("load_message_board_posts - obtained table resource")

        '''TODO - 
        Pass the current date to the partition key
        '''
        dynamodb_response = dynamodb_table.query(
            KeyConditionExpression=Key("PK").eq(
                "rewatch#2022-12-31")
        )

        logging.info("load_message_board_posts - obtained dynamodb_response")

        if len(dynamodb_response["Items"]) == 0:
            logging.info(
                "load_message_board_posts - dynamodb_response Items list has no elements"
            )
            return([])
    
        return(_populate_message_posts(dynamodb_response))

    except Exception as error_suppression:
        logging.exception("load_message_board_posts - unexpected error")
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
        "reddit_api_password"
    ]
    secret_config.reddit_username = deserialized_secret_string[
        "reddit_api_username"
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




def _retrieve_access_token(secret_config: SecretConfig) -> str:
    """retrieves access token from reddit api
    """
    logging.info(f"_retrieve_access_token - invocation begin")
    
    
    

    token_post = Request("https://www.reddit.com/api/v1/access_token")

    token_post.add_header("Authorization", 
    "Basic " + base64.b64encode(
        (f"{secret_config.reddit_client_id}:"+ 
        f"{secret_config.reddit_client_secret}").encode(
            "utf-8"
        )
    ).decode("utf-8"))

    token_post.add_header("user-agent",
        "Lambda:rewatch:v0.0.1 (by /u/toonamiratings)"
    )

    token_post.add_header("Content-Type",
        "application/x-www-form-urlencoded"
    )

    api_response : HTTPResponse

    with urlopen(
            url=token_post, 
            data=urlencode({
                "grant_type": "password",
                "scope": "submit",
                "username": secret_config.reddit_username,
                "password": secret_config.reddit_password
            }).encode("utf-8"), 
            timeout=4
        ) as api_response:

        assert api_response.getcode() == 200, (
            "_retrieve_access_token - "+ 
            "api_response.getcode - " + str(api_response.getcode())
        )


        logging.info(f"_retrieve_access_token - returning access_token")
        return(json.loads(api_response.read())["access_token"])
    



def submit_reddit_post(post_to_submit: MessageBoardPost, 
    secret_config: SecretConfig) -> Optional[str]:
    """submits post_to_submit as a reddit post
    None if operation was successful, str error message otherwise
    """
    logging.info(f"submit_reddit_post - invocation begin")
    
    logging.info(f"submit_reddit_post - invocation end")
    return(_retrieve_access_token(secret_config))



if __name__ == "__main__":
    import logging
    import os
    from time import strftime
    os.environ["AWS_REGION"] = "us-east-1"
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s.%(msecs)03d" + strftime("%z") + " | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S", level=logging.DEBUG
    )
    loaded_secrets = load_secret_config()
    repo_response = submit_reddit_post(None, loaded_secrets)

    print(repo_response)

