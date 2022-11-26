import unittest

class TestRewatchEntityModel(unittest.TestCase):

    def test_television_rating_bad_input_str_attributes(self):
        """TelevisionRating str attributes passed invalid input raises TypeError"""
        from rewatch.entities.rewatch_entity_model import RewatchPost

        mock_invalid_types = [
            set(["a", "b"]),
            3005,
            11.29,
            (1, 2, 3),
            {},
            ["a", "list"]
        ]

        object_properties = [
            attr_name for attr_name in dir(RewatchPost())
            if not attr_name.startswith("_")
        ]
        for mock_invalid_type in mock_invalid_types:
            with self.subTest(mock_invalid_type=mock_invalid_type):

                mock_entity = RewatchPost()
                
                
                
                for object_property in object_properties:
                    with self.assertRaises(TypeError):
                        setattr(
                            mock_entity, mock_invalid_type
                        )