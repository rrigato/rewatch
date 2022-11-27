import json
from copy import deepcopy
from datetime import date


from rewatch.entities.rewatch_entity_model import MessageBoardPost


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
        
    return(deepcopy(mock_entities_list))
