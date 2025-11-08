#!/usr/bin/env python3
"""
Prompt Generator Integration Script
Integrates the prompt generator with existing Moon Dev AI Agents system
"""

import os
import sys
from pathlib import Path
from termcolor import colored

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.prompt_generator_agent import PromptGeneratorAgent
from config import MONITORED_TOKENS, AI_MODEL


class PromptGeneratorIntegration:
    """
    Integration layer between Prompt Generator and existing agents
    """

    def __init__(self):
        self.prompt_agent = PromptGeneratorAgent()
        print(colored("✓ Prompt Generator Integration initialized", "green"))

    def generate_agent_specific_prompts(self):
        """
        Generate custom prompts for each existing agent in the system
        """
        print(colored("\n🔧 Generating agent-specific prompts...", "cyan", attrs=["bold"]))

        agent_configs = {
            "trading_agent": {
                "purpose": "Analyze cryptocurrency token data and make trading decisions with risk assessment",
                "context": {
                    "data_sources": ["BirdEye API", "price data", "volume", "liquidity"],
                    "output_format": "JSON with action (BUY/SELL/NOTHING), confidence, and reasoning",
                    "constraints": "Must consider risk management and position sizing"
                },
                "category": "trading"
            },
            "risk_agent": {
                "purpose": "Evaluate trading risks and enforce position limits and circuit breakers",
                "context": {
                    "metrics": ["current positions", "P&L", "balance", "exposure"],
                    "actions": ["approve", "deny", "close positions"],
                    "safety": "Must prioritize capital preservation"
                },
                "category": "risk_management"
            },
            "sentiment_agent": {
                "purpose": "Analyze social media sentiment and community discussion for trading signals",
                "context": {
                    "sources": ["Twitter", "Discord", "Reddit"],
                    "metrics": ["sentiment score", "volume", "influencer activity"],
                    "output": "Sentiment score -100 to +100 with reasoning"
                },
                "category": "analysis"
            },
            "whale_agent": {
                "purpose": "Track large wallet movements and whale trading activity for market impact prediction",
                "context": {
                    "data": ["wallet balances", "transaction history", "holder distribution"],
                    "insights": ["accumulation", "distribution", "whale signals"],
                    "timeframe": "Real-time and historical analysis"
                },
                "category": "analysis"
            },
            "strategy_agent": {
                "purpose": "Generate and backtest trading strategies based on market conditions",
                "context": {
                    "inputs": ["market data", "indicators", "risk parameters"],
                    "outputs": ["strategy code", "backtest results", "performance metrics"],
                    "format": "Python code using backtesting.py library"
                },
                "category": "strategy"
            },
            "rbi_agent": {
                "purpose": "Extract trading strategies from educational content (videos, PDFs, text)",
                "context": {
                    "inputs": ["YouTube URLs", "PDF documents", "strategy descriptions"],
                    "processing": ["content extraction", "strategy identification", "code generation"],
                    "output": "Backtestable Python strategy code"
                },
                "category": "research"
            },
            "chat_agent": {
                "purpose": "Provide intelligent conversational assistance for trading and market analysis",
                "context": {
                    "capabilities": ["answer questions", "explain concepts", "analyze data"],
                    "knowledge": ["trading", "crypto markets", "technical analysis"],
                    "tone": "Professional yet accessible"
                },
                "category": "content_creation"
            },
            "chartanalysis_agent": {
                "purpose": "Perform technical analysis on price charts and identify trading patterns",
                "context": {
                    "analysis": ["support/resistance", "trend lines", "patterns", "indicators"],
                    "output": ["chart insights", "trading levels", "pattern predictions"],
                    "timeframes": "Multiple timeframes from 5m to 1D"
                },
                "category": "analysis"
            }
        }

        generated_prompts = {}

        for agent_name, config in agent_configs.items():
            print(colored(f"\n  Generating prompt for {agent_name}...", "yellow"))

            result = self.prompt_agent.generate_prompt(
                purpose=config["purpose"],
                context=config.get("context"),
                category=config.get("category", "general"),
                auto_optimize=True
            )

            if 'error' not in result:
                generated_prompts[agent_name] = result
                print(colored(f"    ✓ Generated (ID: {result['prompt_id']})", "green"))

                # Save to file for easy access
                output_file = self.prompt_agent.data_dir / f"{agent_name}_prompt.txt"
                with open(output_file, 'w') as f:
                    f.write(f"# {agent_name.upper()} PROMPT\n\n")
                    f.write(f"Purpose: {config['purpose']}\n\n")
                    f.write("="*80 + "\n\n")
                    f.write(result['prompt_template'])
                    f.write("\n\n" + "="*80 + "\n\n")
                    f.write(f"Variables: {result.get('variables', [])}\n")
                    f.write(f"Description: {result.get('description', '')}\n")

                print(colored(f"    💾 Saved to {output_file}", "cyan"))
            else:
                print(colored(f"    ✗ Error: {result['error']}", "red"))

        print(colored(f"\n✓ Generated {len(generated_prompts)} agent prompts", "green", attrs=["bold"]))
        return generated_prompts

    def optimize_existing_agent_prompts(self):
        """
        Find and optimize prompts currently used in agents
        """
        print(colored("\n🔧 Optimizing existing agent prompts...", "cyan", attrs=["bold"]))

        # Map of agents and their current system prompts (simplified examples)
        current_prompts = {
            "trading_agent": "You are a trading expert. Analyze the data and make a decision.",
            "risk_agent": "Evaluate the risk and decide if the trade should proceed.",
            "sentiment_agent": "Analyze sentiment from social media data.",
        }

        optimizations = {}

        for agent_name, current_prompt in current_prompts.items():
            print(colored(f"\n  Optimizing {agent_name}...", "yellow"))

            result = self.prompt_agent.optimize_prompt(
                prompt=current_prompt,
                purpose=f"Optimize prompt for {agent_name}"
            )

            if result.get('improved'):
                optimizations[agent_name] = result
                print(colored(f"    ✓ Optimized (Score: {result['effectiveness_score']}/100)", "green"))

                for improvement in result.get('improvements', []):
                    print(colored(f"      • {improvement}", "cyan"))
            else:
                print(colored("    ✓ Already optimal", "green"))

        return optimizations

    def setup_continuous_learning(self):
        """
        Set up hooks for continuous learning from agent performance
        """
        print(colored("\n🎓 Setting up continuous learning hooks...", "cyan", attrs=["bold"]))

        learning_code = '''
# Add this to your agents to enable continuous learning

from src.agents.prompt_generator_agent import PromptGeneratorAgent

class YourAgent:
    def __init__(self):
        self.prompt_gen = PromptGeneratorAgent()
        self.current_prompt_id = None  # Set when using generated prompt

    def run_with_learning(self, data):
        # Run your agent logic
        result = self.run_analysis(data)

        # Report results for learning
        if self.current_prompt_id:
            success = result.get('confidence', 0) > 0.7
            quality = result.get('confidence', 0.5)

            self.prompt_gen.learn_from_usage(
                prompt_id=self.current_prompt_id,
                success=success,
                quality_score=quality
            )

        return result
'''

        output_file = self.prompt_agent.data_dir / "continuous_learning_integration.py"
        with open(output_file, 'w') as f:
            f.write(learning_code)

        print(colored(f"  ✓ Integration code saved to {output_file}", "green"))
        print(colored("  📝 Add this pattern to your agents to enable learning", "yellow"))

    def create_main_py_integration(self):
        """
        Create integration code for main.py orchestrator
        """
        print(colored("\n🔗 Creating main.py integration...", "cyan", attrs=["bold"]))

        integration_code = '''
# Add to src/main.py for prompt generator integration

from agents.prompt_generator_agent import PromptGeneratorAgent

class MainOrchestrator:
    def __init__(self):
        # Existing agents...
        self.prompt_generator = PromptGeneratorAgent()

    def optimize_all_agent_prompts(self):
        """Run weekly optimization on all agent prompts"""
        print("Optimizing all agent prompts...")

        templates = self.prompt_generator.get_all_templates()

        # Find low-performing prompts
        for template in templates:
            if template['usage_count'] > 10 and template['rating'] < 0.6:
                print(f"Optimizing {template['name']}...")

                optimized = self.prompt_generator.optimize_prompt(
                    template['template'],
                    template['description']
                )

                if optimized.get('improved'):
                    print(f"  Improved: {optimized['effectiveness_score']}/100")

    def run_agent_with_custom_prompt(self, agent_name, data):
        """Use custom generated prompt for agent"""

        # Get best prompt for this agent
        templates = self.prompt_generator.get_all_templates(category='trading')
        best_prompt = max(templates, key=lambda x: x['rating'])

        # Use it in your agent
        # ... agent logic with best_prompt['template']

        # Learn from results
        self.prompt_generator.learn_from_usage(
            best_prompt['id'],
            success=True,  # Based on actual performance
            quality_score=0.85
        )
'''

        output_file = self.prompt_agent.data_dir / "main_py_integration.py"
        with open(output_file, 'w') as f:
            f.write(integration_code)

        print(colored(f"  ✓ Integration code saved to {output_file}", "green"))
        print(colored("  📝 Add these methods to your main.py orchestrator", "yellow"))

    def test_integration_with_sample_data(self):
        """
        Test the prompt generator with sample trading data
        """
        print(colored("\n🧪 Testing integration with sample data...", "cyan", attrs=["bold"]))

        # Sample token data (simulated)
        sample_token_data = {
            "symbol": "SOL/USDT",
            "price": 98.45,
            "price_change_24h": 5.2,
            "volume_24h": "1250000000",
            "liquidity": "85000000"
        }

        # Generate analysis prompt
        print(colored("\n  1. Generating trading analysis prompt...", "yellow"))
        analysis_prompt = self.prompt_agent.generate_prompt(
            purpose=f"Analyze {sample_token_data['symbol']} for trading opportunity",
            context={"token_data": sample_token_data},
            category="trading"
        )

        print(colored(f"     ✓ Generated prompt (ID: {analysis_prompt['prompt_id']})", "green"))
        print(colored(f"\n     Preview:\n     {analysis_prompt['prompt_template'][:200]}...", "cyan"))

        # Test across multiple models
        print(colored("\n  2. Testing prompt across models...", "yellow"))

        test_results = self.prompt_agent.test_prompt_multi_model(
            prompt_template=analysis_prompt['prompt_template'],
            test_data={var: f"sample_{var}" for var in analysis_prompt.get('variables', [])},
            models=['anthropic', 'deepseek']  # Test with 2 models
        )

        if test_results.get('analysis'):
            analysis = test_results['analysis']
            print(colored(f"     ✓ Fastest: {analysis.get('fastest_model', 'N/A')}", "green"))
            print(colored(f"     ✓ Recommendation: {analysis.get('recommendation', 'N/A')}", "green"))

        print(colored("\n✓ Integration test complete", "green", attrs=["bold"]))

    def generate_trading_strategy_prompts(self):
        """
        Generate specialized prompts for different trading strategies
        """
        print(colored("\n📊 Generating trading strategy prompts...", "cyan", attrs=["bold"]))

        strategies = [
            {
                "name": "Mean Reversion",
                "purpose": "Generate a mean reversion trading strategy using RSI and Bollinger Bands",
                "context": {"indicators": ["RSI", "Bollinger Bands"], "timeframe": "15m"}
            },
            {
                "name": "Momentum",
                "purpose": "Create a momentum trading strategy based on moving averages and volume",
                "context": {"indicators": ["EMA", "Volume"], "timeframe": "1h"}
            },
            {
                "name": "Breakout",
                "purpose": "Develop a breakout strategy identifying support/resistance levels",
                "context": {"patterns": ["consolidation", "breakout"], "timeframe": "4h"}
            }
        ]

        generated_strategies = []

        for strategy in strategies:
            print(colored(f"\n  Generating {strategy['name']} strategy prompt...", "yellow"))

            result = self.prompt_agent.generate_prompt(
                purpose=strategy['purpose'],
                context=strategy['context'],
                category="strategy"
            )

            if 'error' not in result:
                generated_strategies.append(result)
                print(colored(f"    ✓ Generated", "green"))

                # Save strategy prompt
                output_file = self.prompt_agent.data_dir / f"strategy_{strategy['name'].replace(' ', '_').lower()}.txt"
                with open(output_file, 'w') as f:
                    f.write(result['prompt_template'])

                print(colored(f"    💾 Saved to {output_file}", "cyan"))

        print(colored(f"\n✓ Generated {len(generated_strategies)} strategy prompts", "green", attrs=["bold"]))
        return generated_strategies

    def run_full_integration(self):
        """
        Run complete integration setup
        """
        print(colored("\n" + "="*80, "cyan"))
        print(colored("  PROMPT GENERATOR - FULL INTEGRATION", "cyan", attrs=["bold"]))
        print(colored("="*80 + "\n", "cyan"))

        # 1. Generate agent-specific prompts
        agent_prompts = self.generate_agent_specific_prompts()

        # 2. Optimize existing prompts
        # optimizations = self.optimize_existing_agent_prompts()

        # 3. Generate trading strategy prompts
        strategy_prompts = self.generate_trading_strategy_prompts()

        # 4. Setup continuous learning
        self.setup_continuous_learning()

        # 5. Create main.py integration
        self.create_main_py_integration()

        # 6. Test with sample data
        self.test_integration_with_sample_data()

        # Summary
        print(colored("\n" + "="*80, "green"))
        print(colored("  INTEGRATION COMPLETE!", "green", attrs=["bold"]))
        print(colored("="*80, "green"))

        print(colored(f"\n  Generated Prompts:", "yellow"))
        print(colored(f"    • Agent prompts: {len(agent_prompts)}", "white"))
        print(colored(f"    • Strategy prompts: {len(strategy_prompts)}", "white"))

        print(colored(f"\n  Next Steps:", "yellow"))
        print(colored(f"    1. Review generated prompts in:", "white"))
        print(colored(f"       {self.prompt_agent.data_dir}", "cyan"))
        print(colored(f"    2. Integrate continuous learning into your agents", "white"))
        print(colored(f"    3. Update main.py with integration code", "white"))
        print(colored(f"    4. Test agents with new optimized prompts", "white"))

        print(colored(f"\n  Access Dashboard:", "yellow"))
        print(colored(f"    python src/scripts/prompt_dashboard.py", "green"))
        print(colored(f"    → http://localhost:5000", "cyan"))

        print()


def main():
    """Main integration execution"""
    integration = PromptGeneratorIntegration()
    integration.run_full_integration()


if __name__ == "__main__":
    main()
