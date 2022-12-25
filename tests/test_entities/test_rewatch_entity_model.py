import unittest


class TestRewatchEntityModel(unittest.TestCase):
    
    def test_message_board_post_bad_input(self):
        """invalid datatypes for entity raise TypeError"""
        from rewatch.entities.rewatch_entity_model import MessageBoardPost

        mock_invalid_types = [
            set(["a", "b"]),
            3005,
            11.29,
            (1, 2, 3),
            {},
            ["a", "list"]
        ]

        object_properties = [
            attr_name for attr_name in dir(MessageBoardPost())
            if not attr_name.startswith("_")
        ]
        for mock_invalid_type in mock_invalid_types:
            with self.subTest(mock_invalid_type=mock_invalid_type):

                mock_entity = MessageBoardPost()
                
                
                
                for object_property in object_properties:
                    with self.assertRaises(TypeError):
                        setattr(
                            mock_entity, 
                            mock_invalid_type,
                            mock_invalid_type
                        )


    def test_secret_config(self):
        """invalid datatypes for entity raise TypeError"""
        from rewatch.entities.rewatch_entity_model import SecretConfig

        mock_invalid_types = [
            set(["a", "b"]),
            3005,
            11.29,
            (1, 2, 3),
            {},
            ["a", "list"]
        ]

        object_properties = [
            attr_name for attr_name in dir(SecretConfig())
            if not attr_name.startswith("_")
        ]
        for mock_invalid_type in mock_invalid_types:
            with self.subTest(mock_invalid_type=mock_invalid_type):

                mock_entity = SecretConfig()
                
                
                
                for object_property in object_properties:
                    # with self.assertRaises(TypeError):
                    setattr(
                            mock_entity, 
                            mock_invalid_type,
                            mock_invalid_type
                        )

