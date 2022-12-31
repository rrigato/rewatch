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



def user_agent_header() -> str:
    """thin wrapper for the user-agent http header
    """
    return("Lambda:rewatch:v0.0.1 (by /u/toonamiratings)")




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
        user_agent_header()
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
    



def _reddit_post_submission(access_token: str, post_to_submit: MessageBoardPost) -> None:
    """Orchestrates reddit api submission
    """
    logging.info(f"_reddit_post_submission - invocation begin")
    submit_request = Request("https://oauth.reddit.com/api/submit")


    submit_request.add_header("Authorization",
        f"Bearer {access_token}"
    )
    
    submit_request.add_header("Content-Type",
        "application/x-www-form-urlencoded"
    )
    
    submit_request.add_header("user-agent",
        user_agent_header()
    )

    api_response : HTTPResponse

    with urlopen(
            url=submit_request, 
            data=urlencode({
                "kind": "self",
                "sr": "test",
                "text": "Sample automated post",
                "title": "Sample reddit title",
                "type": "json"
            }).encode("utf-8"), 
            timeout=4
        ) as api_response:
        response_body = json.loads(api_response.read())

        assert response_body["success"] == True, (
            "_reddit_post_submission - "+ 
            "api_response.getcode - " + str(api_response.getcode())
        )
    
    

        logging.info(f"_reddit_post_submission - invocation end")
        return(None)



def submit_reddit_post(post_to_submit: MessageBoardPost, 
    secret_config: SecretConfig) -> Optional[str]:
    """submits post_to_submit as a reddit post
    None if operation was successful, str error message otherwise
    """
    try:
        logging.info(f"submit_reddit_post - invocation begin")
        
        access_token = _retrieve_access_token(secret_config)

        
        logging.info(f"submit_reddit_post - invocation end")
        return(_reddit_post_submission(access_token, secret_config))

    except Exception as error_suppression:
        logging.exception("submit_reddit_post - unexpected error")
        return("Unexpected submitting post")


if __name__ == "__main__":
    import logging
    import os
    from time import strftime
    os.environ["AWS_REGION"] = "us-east-1"
    from fixtures.rewatch_fixtures import mock_message_board_posts
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s.%(msecs)03d" + strftime("%z") + " | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S", level=logging.INFO
    )
    loaded_secrets = load_secret_config()
    repo_response = submit_reddit_post(
        mock_message_board_posts(1)[0], loaded_secrets)

    print(repo_response)

