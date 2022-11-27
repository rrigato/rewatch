import unittest


class TestRewatchBackend(unittest.TestCase):
    
    @unittest.skip("skipping for now")
    def test_load_message_board_posts(self):
        """TODO - Stub for loading rewatch posts"""
        from rewatch.entities.rewatch_entity_model import MessageBoardPost
        from rewatch.repo.rewatch_backend import load_message_board_posts


        message_board_posts, retrieval_error = load_message_board_posts()


        [
            self.assertIsInstance(message_board_post, MessageBoardPost) 
            for message_board_post in message_board_posts
        ]
        self.assertIsNone(retrieval_error)

