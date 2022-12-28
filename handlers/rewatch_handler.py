

import logging
from typing import Dict, Optional



def rewatch_external(lambda_event: Dict, lambda_context) -> None:
    """Lambda handler for application
    
        Raises
        ------
        ValueError - if we were unable to successfully create
        a reddit post
    """
    logging.info(f"rewatch_external - invocation begin")
    
    logging.info(f"rewatch_external - invocation end")
    return(None)

