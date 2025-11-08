# 🤖 Ultimate AI Prompt Generator

A comprehensive, production-ready AI prompt engineering system with multi-model testing, self-learning capabilities, and full automation features.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Integration](#integration)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The Ultimate AI Prompt Generator is an advanced system designed to:
- **Generate** optimal AI prompts using AI itself
- **Optimize** existing prompts for better performance
- **Test** prompts across multiple AI models (Claude, GPT-4, DeepSeek, Groq, Gemini)
- **Learn** from usage patterns to continuously improve
- **Manage** a comprehensive template library for common tasks

### Key Capabilities

✅ **Multi-Model Support**: Test prompts across 5+ AI providers
✅ **Self-Learning**: Automatic prompt improvement based on usage
✅ **Template Library**: 20+ pre-built templates for common tasks
✅ **Web Dashboard**: Beautiful, responsive UI for easy management
✅ **CLI Interface**: Powerful command-line tools for automation
✅ **VS Code Integration**: Seamless integration with your IDE
✅ **Full Automation**: Autonomous prompt generation and optimization
✅ **Cross-Platform**: Windows, Linux, macOS support
✅ **Open Source**: Built on free, open-source AI models

## 🚀 Features

### 1. AI-Powered Prompt Generation

```python
from src.agents.prompt_generator_agent import PromptGeneratorAgent

agent = PromptGeneratorAgent()

result = agent.generate_prompt(
    purpose="Analyze cryptocurrency market trends",
    category="trading",
    auto_optimize=True
)

print(result['prompt_template'])
```

### 2. Prompt Optimization

```python
# Optimize an existing prompt
optimized = agent.optimize_prompt(
    prompt="Tell me about the market",
    purpose="Detailed cryptocurrency market analysis"
)

print(f"Score: {optimized['effectiveness_score']}/100")
print(optimized['optimized_prompt'])
```

### 3. Multi-Model Testing

```python
# Test across multiple AI models
results = agent.test_prompt_multi_model(
    prompt_template="Analyze {data} and provide insights",
    test_data={"data": "Sample market data"},
    models=['anthropic', 'openai', 'deepseek']
)

print(f"Fastest model: {results['analysis']['fastest_model']}")
print(f"Recommendation: {results['analysis']['recommendation']}")
```

### 4. Template Library

Built-in templates for:
- **Trading**: Market analysis, strategy generation, risk assessment
- **Analysis**: Data interpretation, trend identification
- **Content Creation**: Social media, articles, summaries
- **Automation**: Code generation, task automation
- **Research**: Literature review, data synthesis

### 5. Self-Learning System

The system automatically improves prompts based on:
- Usage frequency
- Success rates
- Quality scores
- User feedback

## 🏗️ Architecture

```
src/
├── agents/
│   └── prompt_generator_agent.py    # Core prompt generation engine
├── scripts/
│   ├── prompt_cli.py                # Command-line interface
│   └── prompt_dashboard.py          # Web dashboard (Flask)
├── data/
│   └── prompt_generator/
│       ├── prompts.db               # SQLite database
│       └── exports/                 # Template exports
└── models/
    └── model_factory.py             # Multi-model abstraction

tests/
└── test_prompt_generator.py         # Comprehensive test suite

.vscode/
├── tasks.json                       # VS Code tasks
└── launch.json                      # Debug configurations

setup_prompt_generator.ps1           # Windows PowerShell setup
requirements.txt                     # Python dependencies
```

### Database Schema

**prompts**: Template storage with versioning
**test_results**: Multi-model test history
**knowledge_base**: AI knowledge accumulation
**optimizations**: Optimization history tracking

## 📦 Installation

### Windows (PowerShell)

```powershell
# 1. Clone repository (if not already)
git clone <repository-url>
cd moon-dev-ai-agents

# 2. Run setup script
.\setup_prompt_generator.ps1

# 3. Configure API keys in .env
# Add your keys for: ANTHROPIC_KEY, OPENAI_KEY, etc.

# 4. Start using!
python src/scripts/prompt_dashboard.py
```

### Linux/macOS (Bash)

```bash
# 1. Activate conda environment
conda activate tflow

# 2. Install dependencies
pip install flask flask-cors prompt_toolkit termcolor anthropic openai google-generativeai groq

# 3. Update requirements
pip freeze > requirements.txt

# 4. Initialize database
python -c "from src.agents.prompt_generator_agent import PromptGeneratorAgent; PromptGeneratorAgent().create_template_library()"

# 5. Start dashboard
python src/scripts/prompt_dashboard.py
```

### Using Anaconda

```bash
# Create/activate environment
conda create -n tflow python=3.10
conda activate tflow

# Install packages
conda install flask pandas numpy
pip install flask-cors prompt_toolkit termcolor anthropic openai

# Run setup
python src/agents/prompt_generator_agent.py
```

## 💻 Usage

### Web Dashboard

```bash
python src/scripts/prompt_dashboard.py
```

Access at: **http://localhost:5000**

Features:
- 📝 Generate prompts with AI
- 🔧 Optimize existing prompts
- 🧪 Test across multiple models
- 📚 Browse template library
- 📊 View statistics and analytics

### CLI Interface

```bash
# Interactive mode
python src/scripts/prompt_cli.py

# Direct command
python src/scripts/prompt_cli.py --generate "Analyze market trends" --category trading

# Initialize library
python src/scripts/prompt_cli.py --init-library
```

#### CLI Commands

```
generate   - Generate a new AI prompt
optimize   - Optimize an existing prompt
test       - Test prompt across multiple models
list       - List all saved prompts
search     - Search for prompts
export     - Export templates to JSON
stats      - Show statistics
help       - Show help message
exit       - Exit CLI
```

### Standalone Agent

```bash
# Run agent directly
python src/agents/prompt_generator_agent.py
```

### Python API

```python
from src.agents.prompt_generator_agent import PromptGeneratorAgent

# Initialize
agent = PromptGeneratorAgent()

# Generate prompt
result = agent.generate_prompt(
    purpose="Your task description",
    context={"domain": "trading", "style": "technical"},
    category="trading",
    auto_optimize=True
)

# Get all templates
templates = agent.get_all_templates(category="trading")

# Test prompt
test_results = agent.test_prompt_multi_model(
    prompt_template=result['prompt_template'],
    test_data={"variable": "value"},
    models=['anthropic', 'deepseek']
)

# Export library
export_path = agent.export_templates()
```

## 🔌 Integration

### VS Code Integration

**Tasks** (Ctrl+Shift+P → "Tasks: Run Task"):
- Start Prompt Generator Dashboard
- Start Prompt Generator CLI
- Run Prompt Generator Agent
- Initialize Template Library
- Run All Tests
- Lint Code

**Debugging** (F5):
- Dashboard debug mode
- CLI debug mode
- Agent debug mode

### GitHub Integration

```bash
# Commit changes
git add .
git commit -m "Add custom prompts"
git push origin claude/ai-prompt-generator-design-011CUv7eqhZkzkG2fDJ9xCCA
```

### Trading Bot Integration

```python
# Use with existing trading agents
from src.agents.prompt_generator_agent import PromptGeneratorAgent
from src.agents.trading_agent import TradingAgent

# Generate custom trading analysis prompt
prompt_agent = PromptGeneratorAgent()
trading_prompt = prompt_agent.generate_prompt(
    purpose="Analyze token for trading opportunity",
    category="trading"
)

# Use in trading agent
# (Modify trading agent to accept custom prompts)
```

## 🛠️ Development

### Project Structure

```
prompt_generator_agent.py        # Main agent (745 lines)
prompt_cli.py                    # CLI interface (450 lines)
prompt_dashboard.py              # Web dashboard (650 lines)
test_prompt_generator.py         # Test suite (400 lines)
```

### Adding New Templates

```python
# In prompt_generator_agent.py, add to create_template_library()
templates["your_category"] = [
    {
        "name": "your_template",
        "template": """Your prompt with {variables}""",
        "description": "What it does",
        "variables": ["list", "of", "variables"]
    }
]
```

### Extending Model Support

```python
# Add new model provider in model_factory.py
# Then update model_providers list in prompt_generator_agent.py
self.model_providers = ['anthropic', 'openai', 'deepseek', 'groq', 'gemini', 'your_model']
```

### Custom Optimization Rules

```python
# Modify optimize_prompt() in prompt_generator_agent.py
# Add custom optimization logic based on your needs
```

## 🧪 Testing

### Run All Tests

```bash
# Full test suite
python tests/test_prompt_generator.py

# With verbose output
python -m pytest tests/test_prompt_generator.py -v

# Specific test class
python -m pytest tests/test_prompt_generator.py::TestPromptGenerator -v

# Single test
python -m pytest tests/test_prompt_generator.py::TestPromptGenerator::test_03_create_template_library -v
```

### Test Coverage

```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run -m pytest tests/test_prompt_generator.py
coverage report
coverage html
```

### Linting

```bash
# Install pylint
pip install pylint

# Lint code
pylint src/agents/prompt_generator_agent.py
pylint src/scripts/prompt_cli.py
pylint src/scripts/prompt_dashboard.py
```

### Manual Testing

```bash
# Test prompt generation
python -c "from src.agents.prompt_generator_agent import PromptGeneratorAgent; agent = PromptGeneratorAgent(); print(agent.generate_prompt('test purpose'))"

# Test database
python -c "from src.agents.prompt_generator_agent import PromptGeneratorAgent; agent = PromptGeneratorAgent(); print(len(agent.get_all_templates()))"

# Test web dashboard (should start server)
python src/scripts/prompt_dashboard.py
```

## 📊 API Reference

### PromptGeneratorAgent Class

#### `__init__()`
Initialize the prompt generator agent with database and configurations.

#### `generate_prompt(purpose, context=None, category='general', auto_optimize=True)`
Generate a new AI prompt.

**Parameters:**
- `purpose` (str): What the prompt should accomplish
- `context` (dict, optional): Additional context
- `category` (str): Template category
- `auto_optimize` (bool): Whether to auto-optimize

**Returns:** Dict with `prompt_template`, `variables`, `description`

#### `optimize_prompt(prompt, purpose)`
Optimize an existing prompt.

**Parameters:**
- `prompt` (str): The prompt to optimize
- `purpose` (str): What the prompt should do

**Returns:** Dict with `optimized_prompt`, `effectiveness_score`, `improvements`

#### `test_prompt_multi_model(prompt_template, test_data, models=None)`
Test prompt across multiple AI models.

**Parameters:**
- `prompt_template` (str): Prompt with `{variables}`
- `test_data` (dict): Data to fill variables
- `models` (list, optional): List of model providers

**Returns:** Dict with `results` and `analysis`

#### `get_all_templates(category=None)`
Retrieve all prompt templates.

**Parameters:**
- `category` (str, optional): Filter by category

**Returns:** List of template dictionaries

#### `export_templates(output_file=None)`
Export all templates to JSON.

**Parameters:**
- `output_file` (str, optional): Output file path

**Returns:** Export file path

#### `learn_from_usage(prompt_id, success, quality_score=None)`
Update prompt ratings based on usage.

**Parameters:**
- `prompt_id` (int): Template ID
- `success` (bool): Whether usage was successful
- `quality_score` (float, optional): Quality score (0-1)

## 🐛 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'flask'`
**Solution:** Install dependencies: `pip install flask flask-cors`

**Issue:** Database not initializing
**Solution:** Delete `src/data/prompt_generator/prompts.db` and restart

**Issue:** API keys not working
**Solution:** Check `.env` file has correct keys: `ANTHROPIC_KEY`, `OPENAI_KEY`, etc.

**Issue:** Web dashboard not accessible
**Solution:** Check firewall, ensure port 5000 is open, try `http://127.0.0.1:5000`

**Issue:** Model testing fails
**Solution:** Ensure API keys are configured for the models you want to test

**Issue:** PowerShell script won't run
**Solution:** Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell (as Admin)

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

from src.agents.prompt_generator_agent import PromptGeneratorAgent
agent = PromptGeneratorAgent()
```

### Reset Database

```bash
# Delete database
rm src/data/prompt_generator/prompts.db

# Reinitialize
python -c "from src.agents.prompt_generator_agent import PromptGeneratorAgent; PromptGeneratorAgent().create_template_library()"
```

## 📚 Examples

### Example 1: Generate Trading Strategy Prompt

```python
agent = PromptGeneratorAgent()

result = agent.generate_prompt(
    purpose="Generate a mean reversion trading strategy for cryptocurrency",
    context={
        "timeframe": "15-minute candles",
        "indicators": ["RSI", "Bollinger Bands"],
        "risk_level": "moderate"
    },
    category="trading"
)

print(result['prompt_template'])
```

### Example 2: Optimize Research Prompt

```python
original = "Research the topic and write a summary"

optimized = agent.optimize_prompt(
    prompt=original,
    purpose="Academic literature review with citations"
)

print(f"Improvement: {optimized['effectiveness_score']}/100")
for improvement in optimized['improvements']:
    print(f"  • {improvement}")
```

### Example 3: Compare Models

```python
results = agent.test_prompt_multi_model(
    prompt_template="Explain {concept} in simple terms",
    test_data={"concept": "blockchain consensus mechanisms"},
    models=['anthropic', 'openai', 'deepseek', 'groq']
)

for model, result in results['results'].items():
    if result['success']:
        print(f"{model}: {result['latency_ms']}ms")
```

## 🤝 Contributing

1. Follow existing code style (< 800 lines per file)
2. Add tests for new features
3. Update documentation
4. Run linting: `pylint src/agents/prompt_generator_agent.py`
5. Ensure all tests pass: `python tests/test_prompt_generator.py`

## 📄 License

Open source - free for educational and commercial use.

## 🙏 Acknowledgments

Built on the Moon Dev AI Agents framework with support for:
- Anthropic Claude
- OpenAI GPT-4
- DeepSeek
- Groq
- Google Gemini
- Local Ollama models

---

**Need Help?** Open an issue or check the troubleshooting section above.

**Want to Contribute?** PRs welcome! Follow the contributing guidelines.

**Moon Dev AI Agents**: Building the future of AI automation, one agent at a time. 🚀
