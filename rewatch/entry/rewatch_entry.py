

import logging
from typing import Optional

from rewatch.repo.rewatch_backend import (load_message_board_posts,
                                          load_secret_config, remove_post,
                                          submit_reddit_post)


def create_reddit_post() -> Optional[str]:
    """creates a reddit post if matching day is found
    otherwise returns str of error
    """
    
    secret_config = load_secret_config()


    if secret_config is None:
        logging.info(f"create_reddit_post - short circuit credentials")
        return("Error in pre-post setup")

    logging.info(f"create_reddit_post - loaded secrets")

    posts_for_today = load_message_board_posts()

    if posts_for_today is None:
        logging.info(f"create_reddit_post - short circuit post error")
        return("Unable to load what to post today")
    
    if len(posts_for_today) == 0:
        logging.info(f"create_reddit_post - short circuit no posts")
        return("No posts for today")

    logging.info(f"create_reddit_post - len posts_for_today" +
    f"{len(posts_for_today)}")

    message_board_creation_error = submit_reddit_post(
        posts_for_today[0], secret_config
    )

    if message_board_creation_error is not None:
        logging.info(f"create_reddit_post - short circuit post creation")
        return("Error creating reddit post")

    backend_cleanup_error = remove_post(posts_for_today[0])
    
    if backend_cleanup_error is not None:
        logging.info(
            f"create_reddit_post - short circuit bakcend cleanup")
        return("Error cleaning up post creation")

    logging.info(f"create_reddit_post - happy path")

    return(None)



if __name__ == "__main__":
    import logging
    import os
    from time import strftime
    os.environ["AWS_REGION"] = "us-east-1"
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s.%(msecs)03d" + strftime("%z") + " | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S", level=logging.INFO
    )
    creation_result = create_reddit_post()    
    logging.info(f"main - {creation_result}")
    

