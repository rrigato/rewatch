import json
import unittest
from copy import deepcopy
from unittest.mock import MagicMock, patch


class TestRewatchHandler(unittest.TestCase):
    
    @patch("boto3.resource")
    def test_rewatch_external(self,
        boto3_resource_mock: MagicMock):
        """Happy path for reddit post creation"""
        from handlers.rewatch_handler import rewatch_external

        '''Neither lambda event data 
        or context are used by interface'''
        mock_lambda_event = {}
        mock_lambda_context = None

        self.assertIsNone(
            rewatch_external(
                mock_lambda_event,
                mock_lambda_context
            )
        )