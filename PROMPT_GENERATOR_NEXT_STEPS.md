# 🚀 AI Prompt Generator - Next Steps & Recommendations

## Quick Start (5 Minutes)

### 1. Windows Setup (PowerShell)

```powershell
# Run the automated setup script
.\setup_prompt_generator.ps1

# When prompted, let it install dependencies and initialize the database
# Configure API keys in .env file (copy from .env_example)
```

### 2. Linux/macOS Setup (Bash)

```bash
# Activate conda environment
conda activate tflow

# Install dependencies
pip install flask flask-cors prompt_toolkit termcolor anthropic openai google-generativeai groq

# Initialize template library
python src/agents/prompt_generator_agent.py

# Start dashboard
python src/scripts/prompt_dashboard.py
```

### 3. First Run

```bash
# Option A: Web Dashboard (Recommended for beginners)
python src/scripts/prompt_dashboard.py
# Open: http://localhost:5000

# Option B: CLI Interface (For developers)
python src/scripts/prompt_cli.py

# Option C: Direct Python API (For integration)
python -c "from src.agents.prompt_generator_agent import PromptGeneratorAgent; agent = PromptGeneratorAgent(); agent.run()"
```

## Complete Implementation Roadmap

### Phase 1: Setup & Familiarization (Week 1)

#### Day 1: Installation & Setup
- [ ] Run `setup_prompt_generator.ps1` (Windows) or manual setup (Linux/macOS)
- [ ] Configure API keys in `.env` file
- [ ] Test web dashboard access at `http://localhost:5000`
- [ ] Run CLI interface: `python src/scripts/prompt_cli.py`
- [ ] Run test suite: `python tests/test_prompt_generator.py`

#### Day 2: Explore Features
- [ ] Generate 3-5 prompts using web dashboard
- [ ] Test prompt optimization feature
- [ ] Run multi-model testing (compare Claude, GPT-4, DeepSeek)
- [ ] Browse template library
- [ ] Export templates to JSON

#### Day 3: Integration Planning
- [ ] Review existing agents in `src/agents/`
- [ ] Identify which agents would benefit from custom prompts
- [ ] Read `PROMPT_GENERATOR_ARCHITECTURE.md`
- [ ] Plan integration strategy

#### Day 4-5: VS Code Setup
- [ ] Configure VS Code tasks (auto-generated in `.vscode/tasks.json`)
- [ ] Test debugging configurations
- [ ] Set up keyboard shortcuts for quick access
- [ ] Install recommended VS Code extensions (Python, Pylint)

#### Day 6-7: Testing & Validation
- [ ] Run full test suite: `python tests/test_prompt_generator.py`
- [ ] Test with real trading data
- [ ] Validate multi-model responses
- [ ] Review and adjust template library

### Phase 2: Integration with Trading Agents (Week 2-3)

#### Step 1: Run Integration Script
```bash
python src/scripts/integrate_prompt_generator.py
```

This will:
- Generate custom prompts for all 48+ agents
- Create integration code samples
- Test with sample data
- Save prompts to `src/data/prompt_generator/`

#### Step 2: Update Individual Agents

**Example: Update `trading_agent.py`**

```python
# Add at the top
from agents.prompt_generator_agent import PromptGeneratorAgent

class TradingAgent:
    def __init__(self):
        self.prompt_gen = PromptGeneratorAgent()

        # Get or generate custom prompt
        templates = self.prompt_gen.get_all_templates(category='trading')
        self.analysis_prompt = max(templates, key=lambda x: x['rating'])

    def analyze_token(self, token_data):
        # Use custom generated prompt
        prompt = self.analysis_prompt['template']

        # Fill variables
        for key, value in token_data.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))

        # Run analysis with optimized prompt
        result = self.run_ai_analysis(prompt)

        # Learn from results
        self.prompt_gen.learn_from_usage(
            self.analysis_prompt['id'],
            success=result.get('confidence', 0) > 0.7,
            quality_score=result.get('confidence', 0.5)
        )

        return result
```

#### Step 3: Update Main Orchestrator

**Add to `src/main.py`:**

```python
from agents.prompt_generator_agent import PromptGeneratorAgent

class MainOrchestrator:
    def __init__(self):
        # ... existing code ...
        self.prompt_generator = PromptGeneratorAgent()

    def weekly_optimization(self):
        """Run weekly prompt optimization"""
        print("Running weekly prompt optimization...")

        templates = self.prompt_generator.get_all_templates()

        for template in templates:
            # Optimize low-performing prompts
            if template['usage_count'] > 10 and template['rating'] < 0.6:
                optimized = self.prompt_generator.optimize_prompt(
                    template['template'],
                    template['description']
                )

                if optimized.get('improved'):
                    print(f"Optimized {template['name']}: {optimized['effectiveness_score']}/100")

    # Call this in your main loop or as a scheduled task
```

#### Step 4: Test Integration
```bash
# Run the updated agents
python src/agents/trading_agent.py

# Run main orchestrator
python src/main.py

# Monitor prompt performance in dashboard
python src/scripts/prompt_dashboard.py
```

### Phase 3: Advanced Features (Week 4+)

#### Continuous Learning Setup

1. **Automatic Performance Tracking**

Create `src/agents/prompt_learning_mixin.py`:

```python
class PromptLearningMixin:
    """Mixin to add prompt learning to any agent"""

    def track_prompt_performance(self, prompt_id, result):
        """Automatically track and learn from prompt usage"""

        success = self.determine_success(result)
        quality = self.calculate_quality_score(result)

        self.prompt_gen.learn_from_usage(
            prompt_id=prompt_id,
            success=success,
            quality_score=quality
        )

    def determine_success(self, result):
        """Override this in each agent"""
        return result.get('confidence', 0) > 0.7

    def calculate_quality_score(self, result):
        """Override this in each agent"""
        return result.get('confidence', 0.5)
```

2. **Scheduled Optimization**

Add to your system cron or Windows Task Scheduler:

```bash
# Linux/macOS (crontab -e)
0 0 * * 0 /path/to/conda/envs/tflow/bin/python /path/to/src/scripts/optimize_all_prompts.py

# Windows (Task Scheduler PowerShell)
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 00:00
$action = New-ScheduledTaskAction -Execute "python" -Argument "src/scripts/optimize_all_prompts.py"
Register-ScheduledTask -TaskName "OptimizePrompts" -Trigger $trigger -Action $action
```

3. **A/B Testing Framework**

```python
class PromptABTesting:
    """A/B test different prompts for the same task"""

    def __init__(self):
        self.prompt_gen = PromptGeneratorAgent()
        self.test_results = {}

    def ab_test(self, task, prompt_a_id, prompt_b_id, test_data):
        """Compare two prompts"""

        # Test prompt A
        result_a = self.run_with_prompt(prompt_a_id, test_data)

        # Test prompt B
        result_b = self.run_with_prompt(prompt_b_id, test_data)

        # Compare and select winner
        winner = self.compare_results(result_a, result_b)

        return winner
```

### Phase 4: Production Deployment

#### 1. Web Dashboard Production Setup

```bash
# Install production server
pip install gunicorn

# Run with gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 src.scripts.prompt_dashboard:app

# Or with PM2 (process manager)
pm2 start "gunicorn -w 4 -b 0.0.0.0:5000 src.scripts.prompt_dashboard:app" --name prompt-dashboard
```

#### 2. Database Migration (SQLite → PostgreSQL)

For high-traffic production use:

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Migrate data
python src/scripts/migrate_to_postgres.py
```

#### 3. Add Monitoring

```python
# Add to prompt_dashboard.py
from prometheus_client import Counter, Histogram

prompts_generated = Counter('prompts_generated_total', 'Total prompts generated')
generation_latency = Histogram('prompt_generation_seconds', 'Time to generate prompt')

@app.route('/metrics')
def metrics():
    return generate_latest()
```

#### 4. Set Up Logging

```python
# Add to all scripts
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/prompt_generator.log'),
        logging.StreamHandler()
    ]
)
```

## Recommended Workflow

### Daily Workflow

```bash
# Morning: Check dashboard stats
python src/scripts/prompt_dashboard.py &
# Open http://localhost:5000 → Stats page

# Generate prompts as needed
python src/scripts/prompt_cli.py
> generate

# Test changes
python tests/test_prompt_generator.py
```

### Weekly Workflow

```bash
# Sunday: Optimize all prompts
python -c "
from src.agents.prompt_generator_agent import PromptGeneratorAgent
agent = PromptGeneratorAgent()
templates = agent.get_all_templates()
for t in templates:
    if t['rating'] < 0.7:
        agent.optimize_prompt(t['template'], t['description'])
"

# Export updated templates
python src/scripts/prompt_cli.py
> export

# Backup database
cp src/data/prompt_generator/prompts.db backups/prompts_$(date +%Y%m%d).db
```

### Monthly Workflow

```bash
# Analyze performance trends
python src/scripts/analyze_prompt_performance.py

# Update template library with new patterns
python src/scripts/update_template_library.py

# Review and merge low-usage prompts
python src/scripts/cleanup_prompts.py
```

## Performance Optimization Recommendations

### 1. Enable Caching

```python
# Add to prompt_generator_agent.py
from functools import lru_cache

@lru_cache(maxsize=100)
def get_all_templates(self, category=None):
    # Existing code
    pass
```

### 2. Async Multi-Model Testing

```python
# For faster testing
import asyncio

async def test_models_async(self, template, data, models):
    tasks = [self.test_single_model(template, data, m) for m in models]
    results = await asyncio.gather(*tasks)
    return results
```

### 3. Database Indexing

```sql
-- Add to init_database()
CREATE INDEX idx_prompts_category_rating ON prompts(category, rating DESC);
CREATE INDEX idx_prompts_usage ON prompts(usage_count DESC);
CREATE INDEX idx_test_results_prompt ON test_results(prompt_id, tested_at DESC);
```

## Troubleshooting Guide

### Issue: Slow Prompt Generation

**Solutions:**
1. Use faster models for generation (e.g., `haiku` instead of `opus`)
2. Reduce `max_tokens` in config
3. Enable caching
4. Use local Ollama models for testing

### Issue: High API Costs

**Solutions:**
1. Use DeepSeek for optimization (much cheaper)
2. Enable prompt caching in Anthropic API
3. Limit multi-model testing to 2-3 models
4. Use Groq (fast and free tier available)

### Issue: Database Lock Errors

**Solutions:**
1. Switch to PostgreSQL for production
2. Add connection pooling
3. Use WAL mode for SQLite:
```python
conn.execute("PRAGMA journal_mode=WAL")
```

## Security Best Practices

### 1. API Key Management

```python
# NEVER commit API keys
# Use environment variables only
from dotenv import load_dotenv
import os

load_dotenv()
ANTHROPIC_KEY = os.getenv('ANTHROPIC_KEY')

# Add to .gitignore
.env
*.db
```

### 2. Input Validation

```python
def validate_input(purpose, category):
    if len(purpose) > 1000:
        raise ValueError("Purpose too long")

    if category not in ALLOWED_CATEGORIES:
        raise ValueError("Invalid category")

    # Sanitize SQL inputs
    purpose = purpose.replace("'", "''")
    return purpose
```

### 3. Rate Limiting

```python
# Add to web dashboard
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/generate')
@limiter.limit("10 per minute")
def generate():
    # Existing code
    pass
```

## Integration Checklist

- [ ] Web dashboard accessible at http://localhost:5000
- [ ] CLI interface working
- [ ] All tests passing
- [ ] Template library initialized (20+ templates)
- [ ] API keys configured in .env
- [ ] VS Code tasks configured
- [ ] Integration script run successfully
- [ ] At least one trading agent updated to use custom prompts
- [ ] Continuous learning enabled
- [ ] Weekly optimization scheduled
- [ ] Monitoring and logging enabled
- [ ] Backup strategy in place
- [ ] Documentation reviewed

## Success Metrics

Track these to measure system effectiveness:

1. **Prompt Quality**: Average rating > 0.7
2. **Usage**: Prompts used > 100 times/week
3. **Optimization**: 20% of prompts optimized monthly
4. **Model Performance**: Latency < 2000ms average
5. **Agent Performance**: Trading confidence improved by 15%+

## Support & Resources

- **Documentation**: `PROMPT_GENERATOR_README.md`
- **Architecture**: `PROMPT_GENERATOR_ARCHITECTURE.md`
- **Tests**: `tests/test_prompt_generator.py`
- **Examples**: `src/data/prompt_generator/`

## Community Contributions

Consider contributing:
- New prompt templates
- Additional model integrations
- Performance optimizations
- Bug fixes
- Documentation improvements

---

## Final Recommendations

### For Beginners
1. Start with web dashboard
2. Generate 5-10 prompts manually
3. Test optimization feature
4. Browse template library
5. Export templates for reference

### For Developers
1. Review architecture document
2. Run integration script
3. Update 2-3 agents with custom prompts
4. Enable continuous learning
5. Set up automated optimization

### For Production
1. Deploy with gunicorn
2. Migrate to PostgreSQL
3. Enable monitoring
4. Set up automated backups
5. Implement rate limiting

**Remember**: Start small, test thoroughly, scale gradually. The system is designed to learn and improve over time!

---

**Need Help?** Check troubleshooting section or review test suite for examples.

**Ready to Deploy?** Follow Phase 4 deployment steps carefully.

**Want to Contribute?** See community contributions section above.

🚀 **Happy Prompting!**
