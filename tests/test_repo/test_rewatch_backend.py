import unittest

class TestRewatchBackend(unittest.TestCase):
    
    @unittest.skip("skipping for now")
    def test_load_rewatch_posts(self):
        """TODO - Stub for loading rewatch posts"""
        from rewatch.entities.rewatch_entity_model import RewatchPost
        from rewatch.repo.rewatch_backend import load_rewatch_posts


        rewatch_posts, retrieval_error = load_rewatch_posts()


        [
            self.assertIsInstance(rewatch_post, RewatchPost) 
            for rewatch_post in rewatch_posts
        ]
        self.assertIsNone(retrieval_error)

