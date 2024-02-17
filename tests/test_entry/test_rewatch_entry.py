import unittest
from unittest.mock import MagicMock, patch


class TestRewatchEntry(unittest.TestCase):
    
    
    @patch("rewatch.entry.rewatch_entry.remove_post")
    @patch("rewatch.entry.rewatch_entry.submit_reddit_post")
    @patch("rewatch.entry.rewatch_entry.load_message_board_posts")
    @patch("rewatch.entry.rewatch_entry.load_secret_config")
    def test_create_reddit_post(self,
        load_secret_config_mock: MagicMock,
        load_message_board_posts_mock: MagicMock,
        submit_reddit_post_mock: MagicMock,
        remove_post_mock: MagicMock
        ):
        """Happy path for reddit post creation"""
        from fixtures.rewatch_fixtures import (mock_message_board_posts,
                                               mock_secret_config)
        from rewatch.entry.rewatch_entry import create_reddit_post


        load_secret_config_mock.return_value = mock_secret_config()
        load_message_board_posts_mock.return_value = (
            mock_message_board_posts(1)
        )
        submit_reddit_post_mock.return_value = None
        remove_post_mock.return_value = None

        post_creation_error = create_reddit_post()


        self.assertIsNone(post_creation_error)
        
        submit_reddit_post_mock.assert_called_once()
        remove_post_mock.assert_called_once()


    @patch("rewatch.entry.rewatch_entry.remove_post")
    @patch("rewatch.entry.rewatch_entry.submit_reddit_post")
    @patch("rewatch.entry.rewatch_entry.load_message_board_posts")
    @patch("rewatch.entry.rewatch_entry.load_secret_config")
    def test_create_reddit_post_e2e_bug_no_posts(self,
        load_secret_config_mock: MagicMock,
        load_message_board_posts_mock: MagicMock,
        submit_reddit_post_mock: MagicMock,
        remove_post_mock: MagicMock
        ):
        """no posts returns None"""
        from fixtures.rewatch_fixtures import (mock_message_board_posts,
                                               mock_secret_config)
        from rewatch.entry.rewatch_entry import create_reddit_post


        load_secret_config_mock.return_value = mock_secret_config()
        load_message_board_posts_mock.return_value = []
        submit_reddit_post_mock.return_value = None
        remove_post_mock.return_value = None

        post_creation_error = create_reddit_post()


        self.assertIsNone(post_creation_error)
        
        submit_reddit_post_mock.assert_not_called()
        remove_post_mock.assert_not_called()

