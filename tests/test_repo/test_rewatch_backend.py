from copy import deepcopy
import json
import unittest
from unittest.mock import MagicMock, patch


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


    @patch("boto3.client")
    def test_load_secret_config(self, 
        boto_client_mock: MagicMock):
        """Environment config successfully loaded"""
        from fixtures.rewatch_fixtures import mock_secret_config
        from rewatch.entities.rewatch_entity_model import SecretConfig
        from rewatch.repo.rewatch_backend import load_secret_config

        boto_client_mock.return_value.get_secret_value.return_value = deepcopy(
            {
                "Name": "prod/v1/credentials",
                "SecretString": json.dumps(
                    {                
                        # pragma: allowlist nextline secret
                        "reddit_client_secret": "mock0",
                        "reddit_client_id": "mock1",
                        "reddit_username": "mock2",
                        # pragma: allowlist nextline secret
                        "reddit_password": "mock3"
                    }
                )

            }
        )


        secret_config = load_secret_config()

        get_secret_args, get_secret_kwargs = (
            boto_client_mock.return_value.get_secret_value.call_args
        )

        self.assertIsInstance(secret_config, SecretConfig)

        self.assertIn("SecretId", get_secret_kwargs.keys())


