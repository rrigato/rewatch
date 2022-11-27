import logging
from copy import deepcopy
from datetime import date
from typing import List, Optional, Tuple

from rewatch.entities.rewatch_entity_model import RewatchPost


def load_rewatch_posts() -> Tuple[
    Optional[List[RewatchPost]], Optional[str]]:
    """Loads the RewatchPost from persisted storage
    """
    logging.info(f"load_rewatch_posts - invocation begin")
    
    logging.info(f"load_rewatch_posts - invocation end")
    return(Tuple[Optional[List[RewatchPost]], Optional[str]])

