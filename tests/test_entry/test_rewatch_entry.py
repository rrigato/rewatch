import json
import unittest
from copy import deepcopy
from unittest.mock import MagicMock, patch


class TestRewatchEntry(unittest.TestCase):
    
    @patch("boto3.resource")
    def test_create_reddit_post(self,
        boto3_resource_mock: MagicMock):
        """Happy path for reddit post creation"""
        from rewatch.entry.rewatch_entry import create_reddit_post

