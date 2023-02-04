

import json
import logging
from typing import Dict

from rewatch.entry.rewatch_entry import create_reddit_post

logging.getLogger().setLevel(logging.INFO)

def rewatch_external(lambda_event: Dict, lambda_context) -> None:
    """Lambda handler for application
    
        Raises
        ------
        ValueError - if we were unable to successfully create
        a reddit post
    """
    logging.info(f"rewatch_external - invocation begin")
    logging.info(json.dumps(lambda_event, indent=4))

    rewatch_post_error = create_reddit_post()

    if rewatch_post_error is not None:
        logging.info(rewatch_post_error)
        logging.info(
            f"rewatch_external - short circuiting {rewatch_post_error}"
        )
        raise RuntimeError("Unexpected error from architecture")

    logging.info(f"rewatch_external - invocation successful")

    




if __name__ == "__main__":
    from time import strftime
    import logging
    import os
    os.environ["AWS_REGION"] = "us-east-1"
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s.%(msecs)03d" + strftime("%z") + " | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S", level=logging.INFO
    )
    logging.info(rewatch_external({"not": "used"}, None))

