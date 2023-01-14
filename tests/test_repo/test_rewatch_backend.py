from datetime import datetime
import json
import unittest
from copy import deepcopy
from unittest.mock import MagicMock, patch



class TestRewatchBackend(unittest.TestCase):

    @patch("rewatch.repo.rewatch_backend.datetime")    
    @patch("boto3.resource")
    def test_load_message_board_posts(self,
        boto3_resource_mock: MagicMock,
        datetime_mock: MagicMock
        ):
        """happy path loaded rewatch posts"""
        from fixtures.rewatch_fixtures import mock_dynamodb_query_response
        from rewatch.entities.rewatch_entity_model import MessageBoardPost
        from rewatch.repo.rewatch_backend import load_message_board_posts

        mock_current_date = datetime(3005, 11, 28)
        datetime_mock.utcnow.return_value = mock_current_date

        (   boto3_resource_mock.return_value.
            Table.return_value.query.return_value
        ) = ( 
            mock_dynamodb_query_response()
        )


        message_board_posts = load_message_board_posts()


        self.assertEqual(
            len(mock_dynamodb_query_response()["Items"]),
            len(message_board_posts)
        )

        args, kwargs = (
            boto3_resource_mock.return_value.Table.
            return_value.query.call_args
        )

        self.assertIn("KeyConditionExpression", kwargs.keys())
        [
            self.assertIsInstance(message_board_post, MessageBoardPost) 
            for message_board_post in message_board_posts
        ]
        (
            datetime_mock.utcnow.assert_called_once_with()
        )


    @patch("boto3.resource")
    def test_load_message_board_posts_unexpected_error(
        self,
        boto3_resource_mock: MagicMock):
        """unhappy path unexpected error suppressed"""
        from fixtures.rewatch_fixtures import mock_dynamodb_query_response
        from rewatch.entities.rewatch_entity_model import MessageBoardPost
        from rewatch.repo.rewatch_backend import load_message_board_posts



        (   boto3_resource_mock.return_value.
            Table.return_value.query.side_effect
        ) = RuntimeError( 
            "Simulating sdk exception"
        )
        message_board_posts = load_message_board_posts()


        self.assertIsNone(message_board_posts)



    @patch("boto3.client")
    def test_load_secret_config(self, 
        boto_client_mock: MagicMock):
        """Environment config successfully loaded"""
        from fixtures.rewatch_fixtures import mock_secret_config
        from rewatch.entities.rewatch_entity_model import SecretConfig
        from rewatch.repo.rewatch_backend import load_secret_config

        mock_reddit_username = "mock2"
        # pragma: allowlist nextline secret
        mock_reddit_password = "mock3"
        boto_client_mock.return_value.get_secret_value.return_value = deepcopy(
            {
                "Name": "prod/v1/credentials",
                "SecretString": json.dumps(
                    {                
                        # pragma: allowlist nextline secret
                        "reddit_api_secret": "mock0",
                        # pragma: allowlist nextline secret
                        "reddit_api_key": "mock1",
                        "reddit_api_username": mock_reddit_username,
                        "reddit_api_password": mock_reddit_password
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

        
        
        populated_secret_properties = [
            attr_name for attr_name in dir(secret_config)
            if not attr_name.startswith("_")
            and getattr(secret_config, attr_name) is not None
        ]

        for populated_secret in populated_secret_properties:
            self.assertIsNotNone(
                getattr(secret_config, populated_secret),
                msg=f"\n\n secrets_config property {populated_secret}"
            )
        self.assertEqual(
            len(populated_secret_properties),
            4,
            msg="incorrect number of SecretConfig attributes populated"
        )
        
        self.assertEqual(
            secret_config.reddit_username,
            mock_reddit_username,
            msg="\n\ne2e bug where username not populated correctly"
        )
        self.assertEqual(
            secret_config.reddit_password,
            mock_reddit_password,
            msg="\n\ne2e bug where password not populated correctly"
        )



    @patch("rewatch.repo.rewatch_backend.urlopen")
    def test_submit_reddit_post(self, 
        urlopen_mock: MagicMock):
        """Environment config successfully loaded"""
        from fixtures.rewatch_fixtures import mock_message_board_posts
        from fixtures.rewatch_fixtures import mock_secret_config
        from rewatch.entities.rewatch_entity_model import SecretConfig
        from rewatch.repo.rewatch_backend import submit_reddit_post
        from urllib.parse import urlencode

        mock_selected_post = mock_message_board_posts(1)[0]
        mockToken = "mock0"
        get_code_mock = MagicMock(
            side_effect=(200, 200)
        )
        read_mock = MagicMock(side_effect=(
                json.dumps(
                    {
                        "access_token": mockToken
                    }
                ).encode("utf-8")
                ,
                json.dumps(
                    {
                        "success": True
                    }
                ).encode("utf-8")
            )
        )
        (
            urlopen_mock.return_value.__enter__.
            return_value.getcode.side_effect
        ) = get_code_mock

        (
            urlopen_mock.return_value.__enter__.
            return_value.read
        ) = read_mock 
        
        


        submission_error = submit_reddit_post(
            mock_selected_post,
            mock_secret_config()
        )


        self.assertIsNone(submission_error)

        urlopen_args, urlopen_kwargs = urlopen_mock.call_args

        self.assertIn(
            urlencode(
                (""), (mock_selected_post.post_message)
            ),
            urlopen_kwargs["data"].decode("utf-8"),
            msg="\n\n post_message not in post body"
        )
        self.assertIn(
            urlencode({
                "title": mock_selected_post.post_title
            }),
            urlopen_kwargs["data"].decode("utf-8"),
            msg="\n\n post_title not in post body"
        )
        self.assertIn(
            urlencode({
                "flair_text": "Rewatch"
            }),
            urlopen_kwargs["data"].decode("utf-8"),
            msg="\n\n flair_text not in post body"
        )
        '''TODO - once we migrate to
        prod message board'''
        '''self.assertIn(
            urlencode({
                "sr": "toonami"
            }),
            urlopen_kwargs["data"].decode("utf-8"),
            msg="\n\n incorrect subreddit in post body"
        )'''
        self.assertEqual(read_mock.call_count, 2)


    @patch("rewatch.repo.rewatch_backend.urlopen")
    def test_submit_reddit_post_unhappy_path(self, 
        urlopen_mock: MagicMock):
        """Success is False on second api call"""
        from fixtures.rewatch_fixtures import mock_message_board_posts
        from fixtures.rewatch_fixtures import mock_secret_config
        from rewatch.entities.rewatch_entity_model import SecretConfig
        from rewatch.repo.rewatch_backend import submit_reddit_post

        mockToken = "mock0"
        get_code_mock = MagicMock(
            side_effect=(200, 200)
        )
        read_mock = MagicMock(side_effect=(
                json.dumps(
                    {
                        "access_token": mockToken
                    }
                ).encode("utf-8")
                ,
                json.dumps(
                    {
                        "success": False
                    }
                ).encode("utf-8")
            )
        )
        (
            urlopen_mock.return_value.__enter__.
            return_value.getcode.side_effect
        ) = get_code_mock

        (
            urlopen_mock.return_value.__enter__.
            return_value.read
        ) = read_mock 
        
        


        submission_error = submit_reddit_post(
            mock_message_board_posts(1)[0],
            mock_secret_config()
        )


        self.assertIsInstance(submission_error, str)


    @patch("rewatch.repo.rewatch_backend.datetime")    
    @patch("boto3.resource")
    def test_remove_post(self,
        boto3_resource_mock: MagicMock,
        datetime_mock: MagicMock
        ):
        """TODO - remove old rewatch post"""
        from fixtures.rewatch_fixtures import mock_dynamodb_query_response
        from rewatch.entities.rewatch_entity_model import MessageBoardPost
        from rewatch.repo.rewatch_backend import load_message_board_posts

        mock_current_date = datetime(3005, 11, 28)
        datetime_mock.utcnow.return_value = mock_current_date

        (   boto3_resource_mock.return_value.
            Table.return_value.query.return_value
        ) = ( 
            mock_dynamodb_query_response()
        )


        message_board_posts = load_message_board_posts()

