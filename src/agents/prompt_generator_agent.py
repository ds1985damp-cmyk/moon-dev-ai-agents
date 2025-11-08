#!/usr/bin/env python3
"""
Ultimate AI Prompt Generator Agent
Generates, optimizes, and manages prompts for all agents in the system.
Includes template library, multi-model testing, and self-learning capabilities.
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from termcolor import colored

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.model_factory import ModelFactory
from config import AI_MODEL, AI_MAX_TOKENS, AI_TEMPERATURE


class PromptGeneratorAgent:
    """
    Ultimate AI Prompt Generator with comprehensive features:
    - Template library management
    - Multi-model prompt testing
    - Automatic prompt optimization
    - Knowledge base integration
    - Self-learning from successful patterns
    - Version control for prompts
    """

    def __init__(self):
        self.name = "Prompt Generator Agent"
        self.data_dir = Path(__file__).parent.parent / "data" / "prompt_generator"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Initialize database for prompt management
        self.db_path = self.data_dir / "prompts.db"
        self.init_database()

        # Template categories
        self.categories = [
            "trading", "analysis", "risk_management", "content_creation",
            "research", "strategy", "market_data", "automation", "general"
        ]

        # Model providers for testing
        self.model_providers = ['anthropic', 'openai', 'deepseek', 'groq', 'gemini']

        print(colored(f"✓ {self.name} initialized", "green"))

    def init_database(self):
        """Initialize SQLite database for prompt management"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Prompts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                template TEXT NOT NULL,
                description TEXT,
                variables TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                version INTEGER DEFAULT 1,
                rating REAL DEFAULT 0.0,
                usage_count INTEGER DEFAULT 0
            )
        """)

        # Test results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_id INTEGER,
                model_provider TEXT,
                model_name TEXT,
                input_data TEXT,
                output TEXT,
                latency_ms INTEGER,
                token_count INTEGER,
                cost_usd REAL,
                quality_score REAL,
                tested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (prompt_id) REFERENCES prompts (id)
            )
        """)

        # Knowledge base table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                relevance_score REAL DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Optimization history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS optimizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_id INTEGER,
                original_template TEXT,
                optimized_template TEXT,
                improvement_score REAL,
                optimization_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (prompt_id) REFERENCES prompts (id)
            )
        """)

        conn.commit()
        conn.close()

    def generate_prompt(self,
                       purpose: str,
                       context: Dict = None,
                       category: str = "general",
                       auto_optimize: bool = True) -> Dict:
        """
        Generate a new prompt based on purpose and context

        Args:
            purpose: What the prompt should accomplish
            context: Additional context (domain, constraints, examples)
            category: Prompt category for classification
            auto_optimize: Whether to auto-optimize with AI

        Returns:
            Dict with generated prompt and metadata
        """
        print(colored(f"\n🎯 Generating prompt for: {purpose}", "cyan"))

        # Build generation request
        system_prompt = """You are an expert prompt engineer specializing in creating
highly effective prompts for AI systems. Your prompts are clear, specific, and optimized
for different AI models. You understand prompt engineering best practices including:
- Clear instruction formatting
- Appropriate context inclusion
- Role-based prompting
- Few-shot examples when beneficial
- Output format specification
- Constraint definition

Generate production-ready prompts that achieve optimal results."""

        context_str = json.dumps(context, indent=2) if context else "No additional context"

        user_content = f"""Generate an optimal AI prompt for the following purpose:

PURPOSE: {purpose}

CATEGORY: {category}

CONTEXT:
{context_str}

REQUIREMENTS:
1. Create a clear, specific prompt that achieves the stated purpose
2. Include necessary role definition if applicable
3. Specify output format requirements
4. Add relevant constraints or guidelines
5. Include variable placeholders in {{variable_name}} format for dynamic content
6. Make it production-ready and reusable

Return a JSON object with:
{{
    "prompt_template": "the complete prompt with {{variables}}",
    "variables": ["list", "of", "variables"],
    "description": "what this prompt does",
    "best_practices": ["tips", "for", "using", "this", "prompt"],
    "example_usage": "concrete example with filled variables"
}}"""

        try:
            model = ModelFactory.create_model('anthropic')
            response = model.generate_response(
                system_prompt=system_prompt,
                user_content=user_content,
                temperature=0.7,
                max_tokens=2000
            )

            # Parse response
            result = json.loads(response)

            # Auto-optimize if requested
            if auto_optimize:
                optimized = self.optimize_prompt(result['prompt_template'], purpose)
                if optimized.get('improved'):
                    result['prompt_template'] = optimized['optimized_prompt']
                    result['optimization_notes'] = optimized.get('improvements', [])

            # Save to database
            prompt_id = self._save_prompt(
                name=f"{category}_{purpose[:30].replace(' ', '_')}",
                category=category,
                template=result['prompt_template'],
                description=result.get('description', purpose),
                variables=json.dumps(result.get('variables', []))
            )

            result['prompt_id'] = prompt_id
            result['category'] = category

            print(colored("✓ Prompt generated successfully", "green"))
            return result

        except Exception as e:
            print(colored(f"✗ Error generating prompt: {e}", "red"))
            return {"error": str(e)}

    def optimize_prompt(self, prompt: str, purpose: str) -> Dict:
        """
        Optimize an existing prompt using AI analysis

        Args:
            prompt: The prompt to optimize
            purpose: What the prompt should accomplish

        Returns:
            Dict with optimized prompt and improvements
        """
        print(colored("🔧 Optimizing prompt...", "yellow"))

        system_prompt = """You are an expert prompt optimization specialist. Analyze prompts
and suggest improvements for clarity, specificity, effectiveness, and token efficiency.
Consider factors like:
- Instruction clarity and specificity
- Appropriate context provision
- Output format definition
- Constraint specification
- Token efficiency
- Model-specific optimizations"""

        user_content = f"""Analyze and optimize this prompt:

ORIGINAL PROMPT:
{prompt}

PURPOSE:
{purpose}

Provide optimization suggestions and an improved version. Return JSON:
{{
    "improved": true/false,
    "optimized_prompt": "improved version",
    "improvements": ["list of specific improvements made"],
    "effectiveness_score": 0-100,
    "reasoning": "why these changes improve the prompt"
}}"""

        try:
            model = ModelFactory.create_model('anthropic')
            response = model.generate_response(
                system_prompt=system_prompt,
                user_content=user_content,
                temperature=0.5,
                max_tokens=1500
            )

            result = json.loads(response)
            print(colored(f"✓ Optimization complete (Score: {result.get('effectiveness_score', 'N/A')})", "green"))
            return result

        except Exception as e:
            print(colored(f"✗ Optimization failed: {e}", "red"))
            return {"improved": False, "error": str(e)}

    def test_prompt_multi_model(self,
                               prompt_template: str,
                               test_data: Dict,
                               models: List[str] = None) -> Dict:
        """
        Test a prompt across multiple AI models and compare results

        Args:
            prompt_template: The prompt with {variables}
            test_data: Data to fill variables
            models: List of model providers to test (default: all available)

        Returns:
            Comparison results across models
        """
        print(colored("\n🧪 Running multi-model prompt testing...", "cyan"))

        if models is None:
            models = self.model_providers

        # Fill template variables
        filled_prompt = prompt_template
        for key, value in test_data.items():
            filled_prompt = filled_prompt.replace(f"{{{key}}}", str(value))

        results = {}

        for provider in models:
            print(colored(f"  Testing with {provider}...", "yellow"))
            try:
                start_time = datetime.now()
                model = ModelFactory.create_model(provider)

                response = model.generate_response(
                    system_prompt="You are a helpful AI assistant.",
                    user_content=filled_prompt,
                    temperature=AI_TEMPERATURE,
                    max_tokens=AI_MAX_TOKENS
                )

                latency = (datetime.now() - start_time).total_seconds() * 1000

                results[provider] = {
                    "response": response,
                    "latency_ms": latency,
                    "token_count": len(response.split()),  # Rough estimate
                    "success": True
                }

                print(colored(f"    ✓ {provider}: {latency:.0f}ms", "green"))

            except Exception as e:
                results[provider] = {
                    "error": str(e),
                    "success": False
                }
                print(colored(f"    ✗ {provider}: {e}", "red"))

        # Analyze results
        analysis = self._analyze_test_results(results)

        return {
            "results": results,
            "analysis": analysis,
            "prompt_used": filled_prompt
        }

    def _analyze_test_results(self, results: Dict) -> Dict:
        """Analyze and compare test results across models"""
        successful = [p for p, r in results.items() if r.get('success')]

        if not successful:
            return {"error": "All models failed"}

        latencies = {p: results[p]['latency_ms'] for p in successful}
        fastest = min(latencies, key=latencies.get)

        return {
            "successful_models": successful,
            "failed_models": [p for p in results if not results[p].get('success')],
            "fastest_model": fastest,
            "fastest_latency_ms": latencies[fastest],
            "avg_latency_ms": sum(latencies.values()) / len(latencies),
            "recommendation": self._recommend_model(results)
        }

    def _recommend_model(self, results: Dict) -> str:
        """Recommend best model based on test results"""
        successful = [(p, r) for p, r in results.items() if r.get('success')]

        if not successful:
            return "No successful models"

        # Simple scoring: balance speed and likely quality
        scores = {}
        for provider, result in successful:
            latency_score = 1000 / result['latency_ms']  # Faster = better
            response_length = len(result['response'])
            quality_score = min(response_length / 1000, 1.0)  # Prefer detailed responses

            scores[provider] = latency_score * 0.3 + quality_score * 0.7

        best = max(scores, key=scores.get)
        return f"{best} (balanced speed and quality)"

    def create_template_library(self) -> Dict:
        """
        Create a comprehensive library of prompt templates for common tasks
        """
        print(colored("\n📚 Building prompt template library...", "cyan"))

        templates = {
            "trading": [
                {
                    "name": "market_analysis",
                    "template": """Analyze the following market data for {token_symbol}:

Price: ${current_price}
24h Change: {price_change_24h}%
Volume: ${volume_24h}
Market Cap: ${market_cap}

Additional metrics:
{additional_metrics}

Provide a comprehensive analysis including:
1. Price action interpretation
2. Volume analysis
3. Support/resistance levels
4. Trend identification
5. Risk assessment
6. Trading recommendation (BUY/SELL/HOLD)

Format your response as JSON with clear reasoning for each point.""",
                    "description": "Comprehensive market analysis prompt",
                    "variables": ["token_symbol", "current_price", "price_change_24h", "volume_24h", "market_cap", "additional_metrics"]
                },
                {
                    "name": "strategy_generation",
                    "template": """Generate a trading strategy based on the following requirements:

Strategy Type: {strategy_type}
Asset Class: {asset_class}
Risk Tolerance: {risk_tolerance}
Time Horizon: {time_horizon}
Capital: ${capital}

Constraints:
{constraints}

Create a detailed strategy including:
1. Entry conditions with specific indicators
2. Exit conditions (profit targets and stop losses)
3. Position sizing rules
4. Risk management parameters
5. Backtestable pseudocode

Return as executable Python code using the backtesting.py library.""",
                    "description": "AI-driven trading strategy generation",
                    "variables": ["strategy_type", "asset_class", "risk_tolerance", "time_horizon", "capital", "constraints"]
                }
            ],
            "analysis": [
                {
                    "name": "data_interpretation",
                    "template": """Interpret the following data and provide insights:

Data Type: {data_type}
Data:
{data}

Context:
{context}

Provide:
1. Key patterns and trends
2. Anomalies or outliers
3. Statistical significance
4. Actionable insights
5. Confidence level for each insight

Format as structured JSON.""",
                    "description": "General data interpretation and insight extraction",
                    "variables": ["data_type", "data", "context"]
                }
            ],
            "content_creation": [
                {
                    "name": "tweet_generator",
                    "template": """Create an engaging tweet about:

Topic: {topic}
Key Points: {key_points}
Tone: {tone}
Include Hashtags: {include_hashtags}

Requirements:
- Maximum 280 characters
- Engaging and shareable
- Clear call-to-action if applicable
- Professional yet accessible

Return the tweet text only.""",
                    "description": "Social media content generation",
                    "variables": ["topic", "key_points", "tone", "include_hashtags"]
                }
            ],
            "automation": [
                {
                    "name": "code_generator",
                    "template": """Generate production-ready code for the following task:

Task: {task_description}
Language: {programming_language}
Framework: {framework}
Requirements:
{requirements}

Additional Context:
{context}

Generate:
1. Complete, working code
2. Inline comments explaining logic
3. Error handling
4. Type hints (if applicable)
5. Usage example

Follow best practices and modern patterns for {programming_language}.""",
                    "description": "Automated code generation",
                    "variables": ["task_description", "programming_language", "framework", "requirements", "context"]
                }
            ]
        }

        # Save templates to database
        saved_count = 0
        for category, template_list in templates.items():
            for template_data in template_list:
                try:
                    self._save_prompt(
                        name=f"{category}_{template_data['name']}",
                        category=category,
                        template=template_data['template'],
                        description=template_data['description'],
                        variables=json.dumps(template_data['variables'])
                    )
                    saved_count += 1
                except Exception as e:
                    print(colored(f"  Warning: Could not save {template_data['name']}: {e}", "yellow"))

        print(colored(f"✓ Template library created ({saved_count} templates)", "green"))
        return templates

    def _save_prompt(self, name: str, category: str, template: str,
                    description: str, variables: str) -> int:
        """Save a prompt to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO prompts (name, category, template, description, variables)
                VALUES (?, ?, ?, ?, ?)
            """, (name, category, template, description, variables))
            conn.commit()
            prompt_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Update existing
            cursor.execute("""
                UPDATE prompts
                SET template=?, description=?, variables=?, updated_at=CURRENT_TIMESTAMP, version=version+1
                WHERE name=?
            """, (template, description, variables, name))
            conn.commit()
            cursor.execute("SELECT id FROM prompts WHERE name=?", (name,))
            prompt_id = cursor.fetchone()[0]

        conn.close()
        return prompt_id

    def get_all_templates(self, category: str = None) -> List[Dict]:
        """Retrieve all prompt templates, optionally filtered by category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if category:
            cursor.execute("""
                SELECT id, name, category, template, description, variables, rating, usage_count
                FROM prompts WHERE category=? ORDER BY rating DESC, usage_count DESC
            """, (category,))
        else:
            cursor.execute("""
                SELECT id, name, category, template, description, variables, rating, usage_count
                FROM prompts ORDER BY category, rating DESC
            """)

        templates = []
        for row in cursor.fetchall():
            templates.append({
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "template": row[3],
                "description": row[4],
                "variables": json.loads(row[5]) if row[5] else [],
                "rating": row[6],
                "usage_count": row[7]
            })

        conn.close()
        return templates

    def learn_from_usage(self, prompt_id: int, success: bool, quality_score: float = None):
        """
        Self-learning: Update prompt ratings based on usage outcomes

        Args:
            prompt_id: ID of the prompt used
            success: Whether the prompt achieved desired outcome
            quality_score: Optional quality score (0-1)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Update usage count
        cursor.execute("UPDATE prompts SET usage_count=usage_count+1 WHERE id=?", (prompt_id,))

        # Update rating based on success
        if quality_score is not None:
            cursor.execute("""
                UPDATE prompts
                SET rating = (rating * usage_count + ?) / (usage_count + 1)
                WHERE id=?
            """, (quality_score, prompt_id))
        elif success:
            cursor.execute("""
                UPDATE prompts
                SET rating = CASE
                    WHEN rating = 0 THEN 0.7
                    ELSE (rating * 0.9 + 0.1)
                END
                WHERE id=?
            """, (prompt_id,))

        conn.commit()
        conn.close()

    def export_templates(self, output_file: str = None) -> str:
        """Export all templates to JSON file"""
        if output_file is None:
            output_file = self.data_dir / f"prompt_library_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        templates = self.get_all_templates()

        with open(output_file, 'w') as f:
            json.dump(templates, f, indent=2)

        print(colored(f"✓ Templates exported to {output_file}", "green"))
        return str(output_file)

    def run(self):
        """Main execution for standalone mode"""
        print(colored("\n" + "="*60, "cyan"))
        print(colored("  ULTIMATE AI PROMPT GENERATOR", "cyan", attrs=["bold"]))
        print(colored("="*60 + "\n", "cyan"))

        # Initialize template library
        self.create_template_library()

        # Example: Generate a custom prompt
        print(colored("\n📝 Example: Generating custom trading prompt...", "cyan"))
        result = self.generate_prompt(
            purpose="Analyze whale wallet movements and predict market impact",
            context={
                "domain": "cryptocurrency trading",
                "data_sources": ["blockchain transactions", "wallet balances", "price data"],
                "output_format": "JSON with confidence scores"
            },
            category="trading",
            auto_optimize=True
        )

        print(colored("\nGenerated Prompt:", "green"))
        print(result.get('prompt_template', 'Error'))

        # Example: Test prompt across models
        if result.get('prompt_template'):
            print(colored("\n🧪 Testing prompt across multiple AI models...", "cyan"))
            test_results = self.test_prompt_multi_model(
                prompt_template=result['prompt_template'],
                test_data={var: f"sample_{var}" for var in result.get('variables', [])},
                models=['anthropic', 'deepseek']  # Test with 2 models
            )

            print(colored("\nTest Results:", "green"))
            print(json.dumps(test_results.get('analysis', {}), indent=2))

        # Show library stats
        all_templates = self.get_all_templates()
        print(colored(f"\n📊 Template Library: {len(all_templates)} templates across {len(self.categories)} categories", "cyan"))

        # Export templates
        export_path = self.export_templates()
        print(colored(f"\n💾 Templates exported to: {export_path}", "green"))


if __name__ == "__main__":
    agent = PromptGeneratorAgent()
    agent.run()
