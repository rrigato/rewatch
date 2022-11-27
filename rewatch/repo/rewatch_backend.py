import logging
from copy import deepcopy
from datetime import date
from typing import List, Optional, Tuple

from rewatch.entities.rewatch_entity_model import MessageBoardPost


def load_message_board_posts() -> Tuple[
    Optional[List[MessageBoardPost]], Optional[str]]:
    """Loads the MessageBoardPost from persisted storage
    """
    logging.info(f"load_message_board_posts - invocation begin")
    
    logging.info(f"load_message_board_posts - invocation end")
    return(Tuple[Optional[List[MessageBoardPost]], Optional[str]])

