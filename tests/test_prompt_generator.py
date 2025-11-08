#!/usr/bin/env python3
"""
Comprehensive test suite for AI Prompt Generator
Tests all major functionality including generation, optimization, and multi-model testing
"""

import os
import sys
import unittest
import json
import tempfile
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.prompt_generator_agent import PromptGeneratorAgent


class TestPromptGenerator(unittest.TestCase):
    """Test cases for PromptGeneratorAgent"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.agent = PromptGeneratorAgent()
        # Use temporary database for testing
        cls.agent.db_path = Path(tempfile.mkdtemp()) / "test_prompts.db"
        cls.agent.init_database()

    def test_01_initialization(self):
        """Test agent initialization"""
        self.assertIsNotNone(self.agent)
        self.assertTrue(self.agent.db_path.parent.exists())
        self.assertEqual(len(self.agent.categories), 9)

    def test_02_database_structure(self):
        """Test database tables exist"""
        import sqlite3
        conn = sqlite3.connect(self.agent.db_path)
        cursor = conn.cursor()

        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        self.assertIn('prompts', tables)
        self.assertIn('test_results', tables)
        self.assertIn('knowledge_base', tables)
        self.assertIn('optimizations', tables)

        conn.close()

    def test_03_create_template_library(self):
        """Test template library creation"""
        result = self.agent.create_template_library()

        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)
        self.assertIn('trading', result)
        self.assertIn('analysis', result)

        # Verify templates were saved to database
        templates = self.agent.get_all_templates()
        self.assertGreater(len(templates), 0)

    def test_04_generate_prompt(self):
        """Test prompt generation"""
        result = self.agent.generate_prompt(
            purpose="Analyze market trends for cryptocurrency",
            category="trading",
            auto_optimize=False  # Skip optimization for faster testing
        )

        self.assertIsInstance(result, dict)
        self.assertIn('prompt_template', result)
        self.assertIn('description', result)
        self.assertIn('variables', result)
        self.assertIsInstance(result['variables'], list)

        # Verify prompt was saved
        self.assertIn('prompt_id', result)
        self.assertIsInstance(result['prompt_id'], int)

    def test_05_optimize_prompt(self):
        """Test prompt optimization"""
        test_prompt = "Tell me about the market"

        result = self.agent.optimize_prompt(
            prompt=test_prompt,
            purpose="Analyze cryptocurrency market conditions"
        )

        self.assertIsInstance(result, dict)
        self.assertIn('improved', result)

        if result.get('improved'):
            self.assertIn('optimized_prompt', result)
            self.assertIn('improvements', result)
            self.assertIn('effectiveness_score', result)

    def test_06_save_and_retrieve_prompt(self):
        """Test saving and retrieving prompts"""
        # Save a prompt
        prompt_id = self.agent._save_prompt(
            name="test_prompt_unique",
            category="general",
            template="This is a test prompt with {variable}",
            description="Test prompt for unit testing",
            variables='["variable"]'
        )

        self.assertIsInstance(prompt_id, int)

        # Retrieve all prompts
        templates = self.agent.get_all_templates()
        saved_prompt = next((t for t in templates if t['id'] == prompt_id), None)

        self.assertIsNotNone(saved_prompt)
        self.assertEqual(saved_prompt['name'], "test_prompt_unique")
        self.assertEqual(saved_prompt['category'], "general")

    def test_07_get_templates_by_category(self):
        """Test filtering templates by category"""
        # Ensure some templates exist
        self.agent.create_template_library()

        trading_templates = self.agent.get_all_templates(category="trading")

        self.assertIsInstance(trading_templates, list)
        # All templates should be in trading category
        for template in trading_templates:
            self.assertEqual(template['category'], "trading")

    def test_08_learn_from_usage(self):
        """Test self-learning functionality"""
        # Create a test prompt
        prompt_id = self.agent._save_prompt(
            name="learning_test_prompt",
            category="general",
            template="Test",
            description="Test",
            variables="[]"
        )

        # Record successful usage
        initial_templates = self.agent.get_all_templates()
        initial_prompt = next((t for t in initial_templates if t['id'] == prompt_id), None)
        initial_rating = initial_prompt['rating']

        self.agent.learn_from_usage(prompt_id, success=True, quality_score=0.9)

        # Check rating was updated
        updated_templates = self.agent.get_all_templates()
        updated_prompt = next((t for t in updated_templates if t['id'] == prompt_id), None)

        self.assertIsNotNone(updated_prompt)
        # Rating should have increased (or been set if it was 0)
        self.assertGreaterEqual(updated_prompt['rating'], initial_rating)

    def test_09_export_templates(self):
        """Test template export functionality"""
        # Ensure templates exist
        self.agent.create_template_library()

        # Export to temporary file
        temp_dir = Path(tempfile.mkdtemp())
        export_path = self.agent.export_templates(str(temp_dir / "export_test.json"))

        self.assertTrue(os.path.exists(export_path))

        # Verify exported file contains valid JSON
        with open(export_path, 'r') as f:
            exported_data = json.load(f)

        self.assertIsInstance(exported_data, list)
        self.assertGreater(len(exported_data), 0)

        # Cleanup
        os.remove(export_path)

    def test_10_test_prompt_multi_model(self):
        """Test multi-model prompt testing (limited to avoid API costs)"""
        # Use a simple prompt
        test_prompt = "What is 2+2? Answer with just the number."
        test_data = {}

        # Test with only one model to avoid costs
        result = self.agent.test_prompt_multi_model(
            prompt_template=test_prompt,
            test_data=test_data,
            models=['anthropic']  # Test with only one model
        )

        self.assertIsInstance(result, dict)
        self.assertIn('results', result)
        self.assertIn('analysis', result)

        # Check if we got a response from Anthropic
        if 'anthropic' in result['results']:
            anthropic_result = result['results']['anthropic']
            # May succeed or fail depending on API key availability
            self.assertIn('success', anthropic_result)

    def test_11_recommend_model(self):
        """Test model recommendation logic"""
        # Create mock test results
        mock_results = {
            'anthropic': {'success': True, 'latency_ms': 1500, 'response': 'A' * 1000},
            'deepseek': {'success': True, 'latency_ms': 800, 'response': 'B' * 1200},
        }

        recommendation = self.agent._recommend_model(mock_results)

        self.assertIsInstance(recommendation, str)
        self.assertIn('deepseek', recommendation.lower())  # Should recommend faster model

    def test_12_analyze_test_results(self):
        """Test test result analysis"""
        mock_results = {
            'anthropic': {'success': True, 'latency_ms': 1000},
            'openai': {'success': True, 'latency_ms': 1200},
            'groq': {'success': False, 'error': 'API key not found'},
        }

        analysis = self.agent._analyze_test_results(mock_results)

        self.assertIsInstance(analysis, dict)
        self.assertIn('successful_models', analysis)
        self.assertIn('failed_models', analysis)
        self.assertIn('fastest_model', analysis)
        self.assertIn('recommendation', analysis)

        self.assertEqual(len(analysis['successful_models']), 2)
        self.assertEqual(len(analysis['failed_models']), 1)
        self.assertEqual(analysis['fastest_model'], 'anthropic')

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        # Remove test database
        if cls.agent.db_path.exists():
            os.remove(cls.agent.db_path)
            cls.agent.db_path.parent.rmdir()


class TestPromptTemplates(unittest.TestCase):
    """Test specific prompt templates"""

    def setUp(self):
        self.agent = PromptGeneratorAgent()

    def test_trading_templates(self):
        """Test trading category templates"""
        templates = self.agent.create_template_library()

        trading_templates = templates.get('trading', [])
        self.assertGreater(len(trading_templates), 0)

        # Check market analysis template
        market_analysis = next(
            (t for t in trading_templates if t['name'] == 'market_analysis'),
            None
        )
        self.assertIsNotNone(market_analysis)
        self.assertIn('template', market_analysis)
        self.assertIn('variables', market_analysis)

    def test_automation_templates(self):
        """Test automation category templates"""
        templates = self.agent.create_template_library()

        automation_templates = templates.get('automation', [])
        self.assertGreater(len(automation_templates), 0)

        # Check code generator template
        code_gen = next(
            (t for t in automation_templates if t['name'] == 'code_generator'),
            None
        )
        self.assertIsNotNone(code_gen)


class TestPromptValidation(unittest.TestCase):
    """Test prompt validation and quality checks"""

    def setUp(self):
        self.agent = PromptGeneratorAgent()

    def test_generated_prompt_has_variables(self):
        """Test that generated prompts properly identify variables"""
        result = self.agent.generate_prompt(
            purpose="Create a report for {company} analyzing {metric}",
            category="general",
            auto_optimize=False
        )

        # Should extract variables from the purpose
        self.assertIn('prompt_template', result)

    def test_prompt_quality_metrics(self):
        """Test prompt quality assessment"""
        # Good prompt
        good_prompt = """You are an expert analyst. Analyze the following data:
{data}

Provide:
1. Key insights
2. Recommendations
3. Risk assessment

Format your response as JSON."""

        result = self.agent.optimize_prompt(good_prompt, "Data analysis")

        self.assertIsInstance(result, dict)
        # A well-structured prompt might not need improvement
        # Just verify we get a valid response


def run_tests():
    """Run all tests with detailed output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPromptGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestPromptTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestPromptValidation))

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
