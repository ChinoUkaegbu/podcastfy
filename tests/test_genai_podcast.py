import unittest
import pytest
from unittest.mock import patch, MagicMock
import tempfile
import os
from podcastfy.content_generator import ContentGenerator
from podcastfy.utils.config import Config
from podcastfy.utils.config_conversation import ConversationConfig

#TODO: Should be a fixture
def sample_conversation_config():
    conversation_config = {
        "word_count": 2000,
        "conversation_style": ["formal", "educational"],
        "roles_person1": "professor",
        "roles_person2": "student",
        "dialogue_structure": ["Introduction", "Main Points", "Conclusion"],
        "podcast_name": "Teachfy",
        "podcast_tagline": "Learning Through Conversation",
        "output_language": "English",
        "engagement_techniques": ["examples", "questions", "case studies"],
        "creativity": 0
    }
    return conversation_config

class TestGenAIPodcast(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        config = Config()
        self.api_key = config.GEMINI_API_KEY



    
    def test_generate_qa_content(self):
        """
        Test the generate_qa_content method of ContentGenerator.
        """
        content_generator = ContentGenerator(self.api_key)
        input_text = "United States of America"
        result = content_generator.generate_qa_content(input_text)
        print(result)
        self.assertIsNotNone(result)
        self.assertNotEqual(result, "")
        self.assertIsInstance(result, str)
        self.assertRegex(
            result, r"(<Person1>.*?</Person1>\s*<Person2>.*?</Person2>\s*)+"
        )

    def test_custom_conversation_config(self):
        """
        Test the generation of content using a custom conversation configuration file.
        """
        conversation_config = sample_conversation_config()
        content_generator = ContentGenerator(self.api_key, conversation_config)
        input_text = "Artificial Intelligence in Education"
        
        result = content_generator.generate_qa_content(input_text)

        self.assertIsNotNone(result)
        self.assertNotEqual(result, "")
        self.assertIsInstance(result, str)
        
        # Check for elements from the custom config
        self.assertIn(conversation_config["podcast_name"], result)
        self.assertIn(conversation_config["podcast_tagline"], result)
        self.assertTrue(any(role in result.lower() for role in [conversation_config["roles_person1"], 
                                                                conversation_config["roles_person2"]]))
        
        # Check word count (allow some flexibility)
        word_count = len(result.split())

if __name__ == "__main__":
    unittest.main()
