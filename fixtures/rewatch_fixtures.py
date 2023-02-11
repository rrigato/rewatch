import json
from copy import deepcopy
from datetime import date
from typing import Dict


from rewatch.entities.rewatch_entity_model import MessageBoardPost, SecretConfig




def _validate_drift(message_board_post: MessageBoardPost) -> None:
    """Ensurese that fixture stays in sync with entity
    by making sure every attribute is populated
    """
    
    
    object_properties = [
        attr_name for attr_name in dir(MessageBoardPost)
        if not attr_name.startswith("_")
    ]
    
    for object_property in object_properties:
        assert getattr(
            message_board_post, object_property) is not None,(
                f"\n_validate_drift - {object_property} " +
                "None for fixture"
            ) 
    return(None)



def mock_message_board_posts(
        number_of_entities: int
    ) -> list[MessageBoardPost]:
    """Creates a list of mock MessageBoardPost entities"""
    mock_entities_list = []

    for entity_num in range(number_of_entities):

        mock_entity = MessageBoardPost()

        mock_entity.post_date = date.fromisoformat("2014-01-04")
        mock_entity.post_message = f"mock post_message {entity_num}"
        mock_entity.post_title = f"mock post_title {entity_num}"
        mock_entity.show_name = f"mock show_name {entity_num}"
        mock_entity.subreddit = f"mock subreddit {entity_num}"

        _validate_drift(mock_entity)

        mock_entities_list.append(mock_entity)
        
    return(deepcopy(mock_entities_list))


def mock_secret_config(
    ) -> SecretConfig:
    """Every attribute of the SecretConfig entity is populated
    """
    
    
    object_properties = [
        attr_name for attr_name in dir(SecretConfig)
        if not attr_name.startswith("_")
    ]
    
    mock_entity = SecretConfig()

    mock_entity.reddit_client_id = "mockclientid"
    # pragma: allowlist nextline secret
    mock_entity.reddit_client_secret = "mockvalue"    
    # pragma: allowlist nextline secret
    mock_entity.reddit_password = "mockvalue2"    
    mock_entity.reddit_username = "mockvalue3"    

    for object_property in object_properties:
        assert getattr(
            mock_entity, object_property
        ) is not None, (
            f"mock_secret_config = fixture missing {object_property}"
        )
    
    return(deepcopy(mock_entity))


def mock_dynamodb_query_response(
    ) -> Dict:
    """https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.query
    """
    return(deepcopy(
        {"Items":[
            {
                "PK": "rewatch#3005-11-09",
                "SK": "showname",
                "post_title": "Episode 1 and 2",
                "post_message": "Markdown for Episode 1 and 2",
                "subreddit": "toonami"

            },
            {
                "PK": "rewatch#3005-11-16",
                "SK": "showname",
                "post_title": "Episode 3 and 4",
                "post_message": "Markdown for Episode 3 and 4",
                "subreddit": "toonami"

            },
            {
                "PK": "rewatch#3005-11-23",
                "SK": "showname",
                "post_title": "Episode 5 and 6",
                "post_message": "Markdown for Episode 5 and 6",
                "subreddit": "toonami"

            }
        ],
        
        "Count": 3
        
        }
    ))