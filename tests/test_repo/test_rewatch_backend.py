import json
import unittest
from copy import deepcopy
from datetime import date, datetime
from unittest.mock import MagicMock, patch
from urllib.parse import urlencode


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
        mock_dynamodb_response = mock_dynamodb_query_response()
        
        
        possible_post_messages = [
            dynamodb_item["post_message"] for dynamodb_item 
            in mock_dynamodb_response["Items"]
            
        ]
        
        (   boto3_resource_mock.return_value.
            Table.return_value.query.return_value
        ) = deepcopy( 
            mock_dynamodb_response
        )


        message_board_posts = load_message_board_posts()


        self.assertEqual(
            len(mock_dynamodb_response["Items"]),
            len(message_board_posts)
        )

        args, kwargs = (
            boto3_resource_mock.return_value.Table.
            return_value.query.call_args
        )

        self.assertIn("KeyConditionExpression", kwargs.keys())
        for message_board_post in message_board_posts:
        
            self.assertIsInstance(
                message_board_post, 
                MessageBoardPost
            )

            self.assertIsNotNone(
                message_board_post.flair_id,
                msg="""\n\nflair_id attribute not populated from dynamodb_response"""
            )             
        
        [
            self.assertIn(
                message_board_post.post_message, 
                possible_post_messages
            ) 
            for message_board_post in message_board_posts
        ]
        (
            datetime_mock.utcnow.assert_called_once_with()
        )

        self.assertEqual(
            len(mock_dynamodb_response["Items"]), 
            len(message_board_posts)
        )


    @patch("rewatch.repo.rewatch_backend.datetime")    
    @patch("boto3.resource")
    def test_load_message_board_posts_new_attributes(self,
        boto3_resource_mock: MagicMock,
        datetime_mock: MagicMock
        ):
        """All properties added to MessageBoardPosts entity"""
        from fixtures.rewatch_fixtures import mock_dynamodb_query_response
        from rewatch.repo.rewatch_backend import load_message_board_posts

        mock_current_date = datetime(3005, 11, 28)
        datetime_mock.utcnow.return_value = mock_current_date
        mock_dynamodb_response = mock_dynamodb_query_response()
        
        (   boto3_resource_mock.return_value.
            Table.return_value.query.return_value
        ) = deepcopy( 
            mock_dynamodb_response
        )


        message_board_posts = load_message_board_posts()



        for message_board_post in message_board_posts:
        
            self.assertIsNotNone(
                message_board_post.show_name, 
                msg="\n\nshow_name extension not working e2e"
            ) 
            self.assertIsNotNone(
                message_board_post.subreddit, 
                msg="\n\nsubreddit extension not working e2e"
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


    @patch("rewatch.repo.rewatch_backend.datetime")    
    @patch("boto3.resource")
    def test_load_message_board_posts_e2e_bugs(self,
        boto3_resource_mock: MagicMock,
        datetime_mock: MagicMock
        ):
        """post_date field is not populated"""
        from fixtures.rewatch_fixtures import mock_dynamodb_query_response
        from rewatch.entities.rewatch_entity_model import MessageBoardPost
        from rewatch.repo.rewatch_backend import load_message_board_posts

        mock_current_date = datetime(3005, 11, 28)
        datetime_mock.utcnow.return_value = mock_current_date
        mock_dynamodb_response = mock_dynamodb_query_response()
        
        
        possible_post_messages = [
            dynamodb_item["post_message"] for dynamodb_item 
            in mock_dynamodb_response["Items"]
            
        ]
        
        (   boto3_resource_mock.return_value.
            Table.return_value.query.return_value
        ) = deepcopy( 
            mock_dynamodb_response
        )


        message_board_posts = load_message_board_posts()


        for message_board_post in message_board_posts:
            self.assertIsNotNone(
                message_board_post.post_date
            )

    @patch("boto3.client")
    def test_load_secret_config(self, 
        boto_client_mock: MagicMock):
        """Environment config successfully loaded"""
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

    def test_reddit_post_body(self):
        """post_body is properly formed"""
        from fixtures.rewatch_fixtures import mock_message_board_posts
        from rewatch.repo.rewatch_backend import reddit_post_body


        mock_post = mock_message_board_posts(1)[0]


        reddit_api_post_body = reddit_post_body(
            mock_post
        )
        self.assertIn(
            urlencode(
                (""), (mock_post.post_message)
            ),
            reddit_api_post_body.decode("utf-8"),
            msg="\n\n post_message not in post body"
        )
        self.assertIn(
            urlencode({
                "title": mock_post.post_title
            }),
            reddit_api_post_body.decode("utf-8"),
            msg="\n\n post_title not in post body"
        )
        
        self.assertIn(
            urlencode({
                "sr": mock_post.subreddit
            }),
            reddit_api_post_body.decode("utf-8"),
            msg="\n\n incorrect subreddit in post body"
        )


    def test_reddit_post_body_flags(self):
        """flair_id included in post body when not None"""
        from fixtures.rewatch_fixtures import mock_message_board_posts
        from rewatch.repo.rewatch_backend import reddit_post_body

        mock_dev_post = mock_message_board_posts(1)[0]
        mock_prod_post = mock_message_board_posts(1)[0]
        mock_dev_post.flair_id = None
        mock_flair_id = "mock_flair_id"
        mock_prod_post.flair_id = mock_flair_id
        

        dev_post_body = reddit_post_body(
            mock_dev_post
        )
        prod_post_body = reddit_post_body(
            mock_prod_post
        )


        self.assertIn(
            urlencode({
                "flair_id": mock_flair_id
            }),
            prod_post_body.decode("utf-8"),
            msg="\n\n flair_id not in post body"
        )

        
        
    @patch("rewatch.repo.rewatch_backend.urlopen")
    def test_submit_reddit_post(self, 
        urlopen_mock: MagicMock):
        """Environment config successfully loaded"""
        from fixtures.rewatch_fixtures import (mock_message_board_posts,
                                               mock_secret_config)
        from rewatch.repo.rewatch_backend import submit_reddit_post

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
                        "jquery": [[14, 15, ["Link to post"]]],
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
        self.assertEqual(read_mock.call_count, 2)


    @patch("rewatch.repo.rewatch_backend.urlopen")
    def test_submit_reddit_post_unhappy_path(self, 
        urlopen_mock: MagicMock):
        """Success is False on second api call"""
        from fixtures.rewatch_fixtures import (mock_message_board_posts,
                                               mock_secret_config)
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

    
    @patch("boto3.resource")
    def test_remove_post(self,
        boto3_resource_mock: MagicMock
        ):
        """Happy Path no errors"""
        from fixtures.rewatch_fixtures import mock_message_board_posts
        from rewatch.repo.rewatch_backend import remove_post

        mock_delete_item = MagicMock()

        (   boto3_resource_mock.return_value.
            Table.return_value.delete_item
        ) = mock_delete_item


        remove_posts_response = remove_post(
            mock_message_board_posts(1)[0]
        )


        args, kwargs = mock_delete_item.call_args


        self.assertIn(
            "PK",
            kwargs["Key"].keys(),
            msg="\n\nOutgoing delete_item call has no PK"
        )

        self.assertIn(
            "SK",
            kwargs["Key"].keys(),
            msg="\n\nOutgoing delete_item call has no SK"
        )
        self.assertIsNone(remove_posts_response)


    @patch("boto3.resource")
    def test_remove_post_unexpected_error(self,
        boto3_resource_mock: MagicMock
        ):
        """Unhappy path unexpected error suppressed"""
        from fixtures.rewatch_fixtures import mock_message_board_posts
        from rewatch.repo.rewatch_backend import remove_post
        
        (   boto3_resource_mock.return_value.
            Table.return_value.delete_item.side_effect
        ) = RuntimeError(
            "The provided element does not match the key schema")


        remove_posts_response = remove_post(
            mock_message_board_posts(1)[0]
        )


        self.assertIsInstance(remove_posts_response, str)

        
    def test_populte_message_posts_handles_no_flair_id(self):
        """flair_id key does not exist in dyanmodb_query_response"""
        from rewatch.repo.rewatch_backend import _populate_message_posts
        from fixtures.rewatch_fixtures import mock_dynamodb_query_response

        mock_dynamodb_response = mock_dynamodb_query_response()

        mock_dynamodb_response["Items"][0].pop("flair_id")


        mock_message_posts = _populate_message_posts(
            mock_dynamodb_response,
            date(3005, 11, 28)
        )


        self.assertIsNone(
            mock_message_posts[0].flair_id
        )

        