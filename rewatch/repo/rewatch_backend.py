import base64
import json
import logging
import os
from copy import deepcopy
from datetime import date, datetime
from http.client import HTTPResponse
from typing import Dict, List, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import boto3
from boto3.dynamodb.conditions import Key

from rewatch.entities.rewatch_entity_model import (MessageBoardPost,
                                                   SecretConfig)
from rewatch.repo.rewatch_statics import post_body_markup


def user_agent_header() -> str:
    """thin wrapper for the user-agent http header
    """
    return("Lambda:rewatch:v0.7.0 (by /u/toonamiratings)")


def _post_text_markup() -> str:
    """thin wrapper for the user-agent http header
    """
    return(deepcopy(post_body_markup))




def _populate_message_posts(dynamodb_query_response: Dict,
    post_date: date
    ) -> List[MessageBoardPost]:
    """populates entity from external persisted storage
    """
    logging.info(f"_populate_message_posts - invocation begin")
    
    message_board_posts: List[MessageBoardPost] = []

    for dynamodb_item in dynamodb_query_response["Items"]:
        
        new_message_post = MessageBoardPost()

        new_message_post.post_date = post_date
        new_message_post.post_message = dynamodb_item["post_message"]
        new_message_post.post_title = dynamodb_item["post_title"]
        new_message_post.show_name = dynamodb_item["SK"]
        new_message_post.subreddit = dynamodb_item["subreddit"]

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

        current_utc_date = datetime.utcnow().date()
        
        dynamodb_response = dynamodb_table.query(
            KeyConditionExpression=Key("PK").eq(
                "rewatch#" +
                current_utc_date.strftime("%Y-%m-%d")
            )
        )

        logging.info(f"load_message_board_posts - obtained "
        + f"dynamodb_response for {current_utc_date}")

        if len(dynamodb_response["Items"]) == 0:
            logging.info(
                "load_message_board_posts - dynamodb_response Items list has no elements"
            )
            return([])
    
        return(_populate_message_posts(
            dynamodb_response, current_utc_date
        ))

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
    



def _response_validation(api_response_body: Dict) -> None:
    """Parses response for logging pertinent information
    raises AssertionError if response body does not pass validation
    """

    '''api_response_body structure
    {
        "jquery":[["list"], ["of", "list", "api feedback"]],
        "success": <boolean>

    }'''

    if api_response_body["success"] != True:
        logging.info(f"_response_validation - raising errror")
        logging.error(api_response_body)
    
        raise AssertionError("_response_validation false")





def reddit_post_body(post_to_submit: MessageBoardPost) -> bytes:
    """Applies logic necessary to create api post body
    encoded as bytes
    """
    post_body = {
        "kind": "self",
        
        "sr": post_to_submit.subreddit,
        "text": _post_text_markup().format(
                post_body=post_to_submit.post_message
            ),
        "title": post_to_submit.post_title,
        "type": "json"
    }

    if post_to_submit.flair_id is not None:
        post_body["flair_id"] = post_to_submit.flair_id

    logging.info(f"post_submission_post_body - post_body")

    logging.info(post_body)

    return(
        urlencode(
            post_body
            ).encode("utf-8")
    )




def _reddit_post_submission(
        access_token: str,
        post_to_submit: MessageBoardPost
    ) -> None:
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
            data=reddit_post_body(post_to_submit), 
            timeout=4
        ) as api_response:
        response_body = json.loads(api_response.read())

        _response_validation(response_body)

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
        return(_reddit_post_submission(access_token, post_to_submit))

    except Exception as error_suppression:
        logging.exception("submit_reddit_post - unexpected error")
        return("Unexpected submitting post")




def remove_post(message_board_post: MessageBoardPost
    ) -> Optional[str]:
    """Cleans up persistant storage by removing the 
    corresponding message_board_post
    """
    try:
        dynamodb_table = boto3.resource(
            "dynamodb", 
            os.environ.get("AWS_REGION")
        ).Table(
            "rewatch_shared_table"
        )

        logging.info("load_message_board_posts - obtained table resource")    
        
        dynamodb_table.delete_item(
            Key={
                "PK":(
                    "rewatch#" +
                    message_board_post.post_date.isoformat()
                ),
                "SK": message_board_post.show_name
            }    
        )
        logging.info(f"remove_post - invocation end")
        return(None)

    except Exception as error_suppression:
        logging.exception("remove_post - unexpected error")
        return("Unexpected error cleaning up persistant storage")




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
    message_post_to_delete = mock_message_board_posts(1)[0]
    message_post_to_delete.post_date = date(2023, 1, 14)
    message_post_to_delete.show_name = "cyborg009"
    repo_response = remove_post(
        message_post_to_delete
    )

    print(repo_response)

