#!/usr/bin/env python3
"""
AI Prompt Generator CLI
Interactive command-line interface for the prompt generator system
"""

import os
import sys
import json
import argparse
from pathlib import Path
from termcolor import colored
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.prompt_generator_agent import PromptGeneratorAgent


class PromptCLI:
    """Interactive CLI for AI Prompt Generator"""

    def __init__(self):
        self.agent = PromptGeneratorAgent()
        self.commands = {
            'generate': self.cmd_generate,
            'optimize': self.cmd_optimize,
            'test': self.cmd_test,
            'list': self.cmd_list,
            'search': self.cmd_search,
            'export': self.cmd_export,
            'stats': self.cmd_stats,
            'help': self.cmd_help,
            'exit': self.cmd_exit
        }

    def cmd_generate(self, args=None):
        """Generate a new prompt interactively"""
        print(colored("\n🎯 Prompt Generator", "cyan", attrs=["bold"]))

        purpose = prompt(colored("Purpose: ", "green"))
        category = prompt(
            colored("Category (trading/analysis/content_creation/automation/general): ", "green"),
            default="general"
        )

        print(colored("\nOptional context (press Enter to skip):", "yellow"))
        domain = prompt(colored("  Domain: ", "yellow"), default="")
        constraints = prompt(colored("  Constraints: ", "yellow"), default="")

        context = {}
        if domain:
            context['domain'] = domain
        if constraints:
            context['constraints'] = constraints

        auto_optimize = prompt(colored("Auto-optimize? (y/n): ", "yellow"), default="y").lower() == 'y'

        print(colored("\n⏳ Generating prompt...", "cyan"))

        result = self.agent.generate_prompt(
            purpose=purpose,
            context=context if context else None,
            category=category,
            auto_optimize=auto_optimize
        )

        if 'error' in result:
            print(colored(f"\n✗ Error: {result['error']}", "red"))
            return

        print(colored("\n" + "="*80, "green"))
        print(colored("GENERATED PROMPT:", "green", attrs=["bold"]))
        print(colored("="*80, "green"))
        print(result['prompt_template'])
        print(colored("="*80 + "\n", "green"))

        print(colored("Variables:", "cyan"), result.get('variables', []))
        print(colored("Description:", "cyan"), result.get('description', ''))

        if 'optimization_notes' in result:
            print(colored("\nOptimizations applied:", "yellow"))
            for note in result['optimization_notes']:
                print(f"  • {note}")

        # Ask to save
        save = prompt(colored("\nSave to file? (y/n): ", "yellow"), default="n").lower() == 'y'
        if save:
            filename = prompt(colored("Filename: ", "green"), default=f"prompt_{result['prompt_id']}.txt")
            filepath = self.agent.data_dir / filename
            with open(filepath, 'w') as f:
                f.write(result['prompt_template'])
            print(colored(f"✓ Saved to {filepath}", "green"))

    def cmd_optimize(self, args=None):
        """Optimize an existing prompt"""
        print(colored("\n🔧 Prompt Optimizer", "cyan", attrs=["bold"]))

        print("Enter your prompt (press Ctrl+D or Ctrl+Z when done):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass

        prompt_text = "\n".join(lines)
        purpose = prompt(colored("\nPurpose of this prompt: ", "green"))

        print(colored("\n⏳ Optimizing...", "cyan"))

        result = self.agent.optimize_prompt(prompt_text, purpose)

        if not result.get('improved'):
            print(colored("\n✓ Prompt is already optimal!", "green"))
            return

        print(colored("\n" + "="*80, "green"))
        print(colored("OPTIMIZED PROMPT:", "green", attrs=["bold"]))
        print(colored("="*80, "green"))
        print(result['optimized_prompt'])
        print(colored("="*80 + "\n", "green"))

        print(colored(f"Effectiveness Score: {result.get('effectiveness_score', 'N/A')}/100", "cyan"))
        print(colored("\nImprovements:", "yellow"))
        for improvement in result.get('improvements', []):
            print(f"  • {improvement}")

        print(colored(f"\nReasoning: {result.get('reasoning', '')}", "cyan"))

    def cmd_test(self, args=None):
        """Test a prompt across multiple models"""
        print(colored("\n🧪 Multi-Model Prompt Tester", "cyan", attrs=["bold"]))

        # Get prompt from template or manual entry
        use_template = prompt(colored("Use saved template? (y/n): ", "yellow"), default="n").lower() == 'y'

        if use_template:
            templates = self.agent.get_all_templates()
            print(colored("\nAvailable templates:", "cyan"))
            for i, t in enumerate(templates[:10]):  # Show first 10
                print(f"  {i+1}. {t['name']} ({t['category']})")

            choice = int(prompt(colored("Select template #: ", "green"))) - 1
            if 0 <= choice < len(templates):
                template = templates[choice]
                prompt_text = template['template']
                variables = template['variables']

                # Fill variables
                test_data = {}
                print(colored("\nFill template variables:", "yellow"))
                for var in variables:
                    test_data[var] = prompt(colored(f"  {var}: ", "green"))
            else:
                print(colored("Invalid choice", "red"))
                return
        else:
            print("Enter your prompt (press Ctrl+D or Ctrl+Z when done):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            prompt_text = "\n".join(lines)
            test_data = {}

        # Select models
        print(colored("\nAvailable models:", "cyan"))
        print("  1. Anthropic Claude")
        print("  2. OpenAI GPT-4")
        print("  3. DeepSeek")
        print("  4. Groq")
        print("  5. Google Gemini")
        print("  6. All models")

        model_choice = prompt(colored("Select models (comma-separated) or 6 for all: ", "green"))

        if '6' in model_choice:
            models = ['anthropic', 'openai', 'deepseek', 'groq', 'gemini']
        else:
            model_map = {
                '1': 'anthropic', '2': 'openai', '3': 'deepseek',
                '4': 'groq', '5': 'gemini'
            }
            models = [model_map.get(c.strip()) for c in model_choice.split(',') if c.strip() in model_map]

        print(colored(f"\n⏳ Testing with {len(models)} models...", "cyan"))

        results = self.agent.test_prompt_multi_model(prompt_text, test_data, models)

        print(colored("\n" + "="*80, "green"))
        print(colored("TEST RESULTS", "green", attrs=["bold"]))
        print(colored("="*80 + "\n", "green"))

        for model, result in results['results'].items():
            if result.get('success'):
                print(colored(f"✓ {model.upper()}", "green", attrs=["bold"]))
                print(f"  Latency: {result['latency_ms']:.0f}ms")
                print(f"  Response length: {len(result['response'])} chars")
                print(f"  Preview: {result['response'][:100]}...")
            else:
                print(colored(f"✗ {model.upper()}", "red", attrs=["bold"]))
                print(f"  Error: {result.get('error', 'Unknown')}")
            print()

        analysis = results.get('analysis', {})
        if analysis:
            print(colored("ANALYSIS", "cyan", attrs=["bold"]))
            print(f"Successful: {', '.join(analysis.get('successful_models', []))}")
            print(f"Fastest: {analysis.get('fastest_model', 'N/A')} ({analysis.get('fastest_latency_ms', 0):.0f}ms)")
            print(f"Average latency: {analysis.get('avg_latency_ms', 0):.0f}ms")
            print(f"Recommendation: {analysis.get('recommendation', 'N/A')}")

    def cmd_list(self, args=None):
        """List all saved prompts"""
        category = prompt(colored("Filter by category (or 'all'): ", "green"), default="all")

        if category.lower() == 'all':
            templates = self.agent.get_all_templates()
        else:
            templates = self.agent.get_all_templates(category)

        print(colored(f"\n📚 Found {len(templates)} templates\n", "cyan"))

        current_category = None
        for t in templates:
            if t['category'] != current_category:
                current_category = t['category']
                print(colored(f"\n{current_category.upper()}", "yellow", attrs=["bold"]))

            print(colored(f"  [{t['id']}] {t['name']}", "green"))
            print(f"      {t['description']}")
            print(f"      Rating: {t['rating']:.2f} | Usage: {t['usage_count']}")

    def cmd_search(self, args=None):
        """Search for prompts"""
        query = prompt(colored("Search query: ", "green"))

        templates = self.agent.get_all_templates()
        matches = [
            t for t in templates
            if query.lower() in t['name'].lower() or
               query.lower() in t['description'].lower() or
               query.lower() in t['template'].lower()
        ]

        print(colored(f"\n🔍 Found {len(matches)} matches\n", "cyan"))

        for t in matches:
            print(colored(f"[{t['id']}] {t['name']} ({t['category']})", "green"))
            print(f"    {t['description']}")

    def cmd_export(self, args=None):
        """Export all templates"""
        filename = prompt(colored("Export filename (or press Enter for auto): ", "green"), default="")

        if filename:
            filepath = self.agent.export_templates(self.agent.data_dir / filename)
        else:
            filepath = self.agent.export_templates()

        print(colored(f"✓ Exported to {filepath}", "green"))

    def cmd_stats(self, args=None):
        """Show statistics"""
        templates = self.agent.get_all_templates()

        print(colored("\n📊 PROMPT GENERATOR STATISTICS", "cyan", attrs=["bold"]))
        print(colored("="*60 + "\n", "cyan"))

        # Category breakdown
        categories = {}
        for t in templates:
            categories[t['category']] = categories.get(t['category'], 0) + 1

        print(colored("Templates by Category:", "yellow"))
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")

        # Top rated
        top_rated = sorted(templates, key=lambda x: x['rating'], reverse=True)[:5]
        print(colored("\nTop Rated Prompts:", "yellow"))
        for i, t in enumerate(top_rated, 1):
            print(f"  {i}. {t['name']} ({t['rating']:.2f})")

        # Most used
        most_used = sorted(templates, key=lambda x: x['usage_count'], reverse=True)[:5]
        print(colored("\nMost Used Prompts:", "yellow"))
        for i, t in enumerate(most_used, 1):
            print(f"  {i}. {t['name']} ({t['usage_count']} uses)")

        print(colored(f"\nTotal Templates: {len(templates)}", "green", attrs=["bold"]))

    def cmd_help(self, args=None):
        """Show help"""
        print(colored("\n📖 PROMPT GENERATOR CLI - COMMANDS", "cyan", attrs=["bold"]))
        print(colored("="*60 + "\n", "cyan"))

        commands = {
            'generate': 'Generate a new AI prompt',
            'optimize': 'Optimize an existing prompt',
            'test': 'Test a prompt across multiple AI models',
            'list': 'List all saved prompts',
            'search': 'Search for prompts',
            'export': 'Export all templates to JSON',
            'stats': 'Show statistics',
            'help': 'Show this help message',
            'exit': 'Exit the CLI'
        }

        for cmd, desc in commands.items():
            print(colored(f"  {cmd:<12}", "green") + desc)

        print()

    def cmd_exit(self, args=None):
        """Exit the CLI"""
        print(colored("\n👋 Goodbye!", "cyan"))
        sys.exit(0)

    def run(self):
        """Main CLI loop"""
        print(colored("\n" + "="*60, "cyan"))
        print(colored("  🤖 AI PROMPT GENERATOR CLI", "cyan", attrs=["bold"]))
        print(colored("="*60, "cyan"))
        print(colored("  Type 'help' for commands, 'exit' to quit\n", "yellow"))

        completer = WordCompleter(list(self.commands.keys()), ignore_case=True)

        while True:
            try:
                user_input = prompt(
                    colored("prompt> ", "green", attrs=["bold"]),
                    completer=completer
                ).strip()

                if not user_input:
                    continue

                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else None

                if command in self.commands:
                    self.commands[command](args)
                else:
                    print(colored(f"Unknown command: {command}. Type 'help' for available commands.", "red"))

            except KeyboardInterrupt:
                print(colored("\n\nUse 'exit' to quit", "yellow"))
            except EOFError:
                self.cmd_exit()
            except Exception as e:
                print(colored(f"\n✗ Error: {e}", "red"))


def main():
    parser = argparse.ArgumentParser(description='AI Prompt Generator CLI')
    parser.add_argument('--init-library', action='store_true',
                       help='Initialize prompt template library')
    parser.add_argument('--generate', type=str, help='Generate prompt for purpose')
    parser.add_argument('--category', type=str, default='general',
                       help='Category for generated prompt')

    args = parser.parse_args()

    cli = PromptCLI()

    if args.init_library:
        print(colored("Initializing prompt template library...", "cyan"))
        cli.agent.create_template_library()
        return

    if args.generate:
        result = cli.agent.generate_prompt(
            purpose=args.generate,
            category=args.category
        )
        print("\n" + result.get('prompt_template', 'Error'))
        return

    # Interactive mode
    cli.run()


if __name__ == "__main__":
    main()
