import json
from copy import deepcopy
from datetime import date
from typing import Dict


from rewatch.entities.rewatch_entity_model import MessageBoardPost, SecretConfig


def mock_message_board_posts(
        number_of_entities: int
    ) -> list[MessageBoardPost]:
    """Creates a list of mock MessageBoardPost entities

        Parameters
        ----------
        number_of_entities
            defaults to 3 
        
    """
    mock_entities_list = []

    for entity_num in range(number_of_entities):

        mock_entity = MessageBoardPost()

        mock_entity.post_date = date.fromisoformat("2014-01-04")
        mock_entity.post_message = f"mock post_message {entity_num}"
        mock_entity.post_title = f"mock post_title {entity_num}"

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
                "PK": "rewatch#showname",
                "SK": "3005-11-09",
                "post_title": "Episode 1 and 2",
                "post_message": "Markdown for Episode 1 and 2"

            },
            {
                "PK": "rewatch#showname",
                "SK": "3005-11-16",
                "post_title": "Episode 3 and 4",
                "post_message": "Markdown for Episode 3 and 4"

            },
            {
                "PK": "rewatch#showname",
                "SK": "3005-11-23",
                "post_title": "Episode 5 and 6",
                "post_message": "Markdown for Episode 5 and 6"

            }
        ],
        
        "Count": 3
        
        }
    ))