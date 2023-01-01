import json
import unittest
from copy import deepcopy
from unittest.mock import MagicMock, patch


class TestRewatchHandler(unittest.TestCase):
    
    @patch("handlers.rewatch_handler.create_reddit_post")
    def test_rewatch_external(self,
        create_reddit_post_mock: MagicMock):
        """Unexpected error raises RuntimeError"""
        from handlers.rewatch_handler import rewatch_external

        '''Neither lambda event data 
        or context are used by interface'''
        mock_lambda_event = {}
        mock_lambda_context = None
        mock_error_message = "architecture layer propagated error"

        create_reddit_post_mock.return_value = mock_error_message

        with self.assertRaises(RuntimeError):
            rewatch_external(
                mock_lambda_event,
                mock_lambda_context
            )
        