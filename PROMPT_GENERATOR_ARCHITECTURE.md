# 🏗️ AI Prompt Generator - System Architecture

## Overview

The Ultimate AI Prompt Generator is a comprehensive system designed for autonomous prompt engineering, multi-model testing, and continuous learning. This document outlines the complete architecture, data flows, and integration points.

## System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACES                              │
├──────────────┬────────────────┬──────────────┬──────────────────┤
│  Web Dashboard │   CLI Tool    │   VS Code   │  Python API      │
│   (Flask)     │  (Interactive)│  (Tasks)    │  (Direct)        │
└──────┬────────┴───────┬────────┴──────┬──────┴─────────┬────────┘
       │                 │                │                │
       └─────────────────┴────────────────┴────────────────┘
                              │
                              ▼
       ┌──────────────────────────────────────────────────┐
       │      PROMPT GENERATOR AGENT (Core Engine)        │
       ├──────────────────────────────────────────────────┤
       │  • Prompt Generation                             │
       │  • Prompt Optimization                           │
       │  • Multi-Model Testing                           │
       │  • Template Management                           │
       │  • Self-Learning System                          │
       └───────┬──────────────────────────────────┬───────┘
               │                                  │
       ┌───────▼────────┐                ┌───────▼────────┐
       │ Model Factory  │                │   Database     │
       │  (Abstraction) │                │   (SQLite)     │
       ├────────────────┤                ├────────────────┤
       │ • Anthropic    │                │ • prompts      │
       │ • OpenAI       │                │ • test_results │
       │ • DeepSeek     │                │ • knowledge_base│
       │ • Groq         │                │ • optimizations│
       │ • Gemini       │                └────────────────┘
       │ • Ollama       │
       └────────────────┘
               │
               ▼
       ┌──────────────────┐
       │  AI Model APIs   │
       └──────────────────┘
```

## Data Flow Architecture

### 1. Prompt Generation Flow

```
User Request
    │
    ▼
Purpose + Context + Category
    │
    ▼
AI Generation System
    │   (using ModelFactory)
    │
    ▼
Raw Prompt Template
    │
    ▼
Auto-Optimization (optional)
    │   (AI-powered refinement)
    │
    ▼
Variable Extraction
    │
    ▼
Database Storage
    │   (versioned)
    │
    ▼
Return to User
```

### 2. Multi-Model Testing Flow

```
Prompt Template + Test Data
    │
    ▼
Variable Substitution
    │
    ▼
┌────────────────────────────────┐
│  Parallel Model Testing        │
├─────────┬─────────┬────────────┤
│ Claude  │ GPT-4   │ DeepSeek   │
│ (API)   │ (API)   │ (API)      │
└────┬────┴────┬────┴─────┬──────┘
     │         │          │
     ▼         ▼          ▼
  Result    Result     Result
     │         │          │
     └─────────┴──────────┘
              │
              ▼
     Results Aggregation
              │
              ▼
     Performance Analysis
     • Latency comparison
     • Response quality
     • Cost estimation
     • Model recommendation
              │
              ▼
     Store in test_results table
              │
              ▼
     Return Analysis to User
```

### 3. Self-Learning Flow

```
Prompt Usage Event
    │
    ▼
Record Usage Metrics
• Success/Failure
• Quality Score
• Latency
• User Feedback
    │
    ▼
Update Prompt Statistics
• usage_count++
• rating adjustment
• effectiveness score
    │
    ▼
Knowledge Base Update
• Store successful patterns
• Identify optimization opportunities
• Update recommendations
    │
    ▼
Automatic Prompt Improvement
• Trigger re-optimization
• Update template library
• Archive old versions
```

## Database Schema

### Table: `prompts`
```sql
CREATE TABLE prompts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    template TEXT NOT NULL,
    description TEXT,
    variables TEXT,              -- JSON array
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    version INTEGER,
    rating REAL,                 -- 0.0 - 1.0
    usage_count INTEGER
);

-- Indexes
CREATE INDEX idx_category ON prompts(category);
CREATE INDEX idx_rating ON prompts(rating DESC);
CREATE INDEX idx_usage ON prompts(usage_count DESC);
```

### Table: `test_results`
```sql
CREATE TABLE test_results (
    id INTEGER PRIMARY KEY,
    prompt_id INTEGER,
    model_provider TEXT,
    model_name TEXT,
    input_data TEXT,             -- JSON
    output TEXT,
    latency_ms INTEGER,
    token_count INTEGER,
    cost_usd REAL,
    quality_score REAL,
    tested_at TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES prompts(id)
);

-- Indexes
CREATE INDEX idx_prompt_test ON test_results(prompt_id);
CREATE INDEX idx_model ON test_results(model_provider);
```

### Table: `knowledge_base`
```sql
CREATE TABLE knowledge_base (
    id INTEGER PRIMARY KEY,
    topic TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT,
    relevance_score REAL,
    created_at TIMESTAMP
);

-- Full-text search index
CREATE VIRTUAL TABLE knowledge_fts USING fts5(topic, content);
```

### Table: `optimizations`
```sql
CREATE TABLE optimizations (
    id INTEGER PRIMARY KEY,
    prompt_id INTEGER,
    original_template TEXT,
    optimized_template TEXT,
    improvement_score REAL,
    optimization_type TEXT,      -- 'clarity', 'efficiency', 'specificity'
    created_at TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES prompts(id)
);
```

## API Architecture

### REST API Endpoints (Flask Dashboard)

```
GET  /                          → Dashboard HTML
GET  /api/templates             → Get all templates
GET  /api/templates/:category   → Get category templates
POST /api/generate              → Generate new prompt
POST /api/optimize              → Optimize prompt
POST /api/test                  → Multi-model test
GET  /api/stats                 → Get statistics
GET  /api/export                → Export templates (JSON)
POST /api/learn                 → Record usage feedback
```

### Python API

```python
# Core Agent API
agent = PromptGeneratorAgent()

# Generation
result = agent.generate_prompt(purpose, context, category, auto_optimize)

# Optimization
optimized = agent.optimize_prompt(prompt, purpose)

# Testing
results = agent.test_prompt_multi_model(template, data, models)

# Management
templates = agent.get_all_templates(category)
agent.learn_from_usage(prompt_id, success, quality_score)
export_path = agent.export_templates(output_file)
```

## Integration Architecture

### 1. Moon Dev Trading Agents Integration

```python
# agents/trading_agent.py (Modified)
from agents.prompt_generator_agent import PromptGeneratorAgent

class TradingAgent:
    def __init__(self):
        self.prompt_gen = PromptGeneratorAgent()

    def analyze_market(self, token_data):
        # Generate custom analysis prompt
        prompt = self.prompt_gen.generate_prompt(
            purpose=f"Analyze {token_data['symbol']} for trading",
            category="trading",
            context={"risk_level": "moderate"}
        )

        # Use generated prompt for analysis
        analysis = self.run_analysis(prompt['prompt_template'], token_data)

        # Learn from results
        self.prompt_gen.learn_from_usage(
            prompt['prompt_id'],
            success=analysis['confidence'] > 0.7,
            quality_score=analysis['confidence']
        )

        return analysis
```

### 2. VS Code Extension Points

```json
// .vscode/tasks.json
{
  "tasks": [
    {
      "label": "Generate Prompt for Current File",
      "type": "shell",
      "command": "python",
      "args": [
        "src/scripts/prompt_cli.py",
        "--generate",
        "Code review for ${file}"
      ]
    },
    {
      "label": "Optimize Documentation Prompts",
      "type": "shell",
      "command": "python",
      "args": [
        "-c",
        "from src.agents.prompt_generator_agent import *; optimize_all_docs()"
      ]
    }
  ]
}
```

### 3. GitHub Actions Integration

```yaml
# .github/workflows/prompt-optimization.yml
name: Optimize Prompts
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  optimize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Optimize all prompts
        run: |
          python -c "
          from src.agents.prompt_generator_agent import PromptGeneratorAgent
          agent = PromptGeneratorAgent()
          # Optimize low-performing prompts
          templates = agent.get_all_templates()
          for t in templates:
              if t['rating'] < 0.6:
                  agent.optimize_prompt(t['template'], t['description'])
          "
```

## Performance Optimization

### 1. Caching Strategy

```python
# Implement LRU cache for frequent operations
from functools import lru_cache

class PromptGeneratorAgent:
    @lru_cache(maxsize=100)
    def get_template_by_name(self, name):
        """Cache frequently accessed templates"""
        pass

    @lru_cache(maxsize=50)
    def _analyze_test_results(self, results_hash):
        """Cache result analysis"""
        pass
```

### 2. Async Multi-Model Testing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def test_prompt_async(self, template, data, models):
    """Async version for faster parallel testing"""
    with ThreadPoolExecutor(max_workers=len(models)) as executor:
        futures = [
            executor.submit(self._test_single_model, template, data, model)
            for model in models
        ]
        results = await asyncio.gather(*futures)
    return results
```

### 3. Database Optimization

```sql
-- Materialized view for statistics
CREATE VIEW prompt_stats AS
SELECT
    category,
    COUNT(*) as count,
    AVG(rating) as avg_rating,
    SUM(usage_count) as total_usage
FROM prompts
GROUP BY category;

-- Prepared statements for common queries
PREPARE get_top_prompts AS
SELECT * FROM prompts
WHERE category = $1
ORDER BY rating DESC, usage_count DESC
LIMIT 10;
```

## Security Architecture

### 1. API Key Management

```python
# Use environment variables only
import os
from dotenv import load_load_dotenv

load_dotenv()

ANTHROPIC_KEY = os.getenv('ANTHROPIC_KEY')  # Never hardcode
OPENAI_KEY = os.getenv('OPENAI_KEY')
```

### 2. Input Validation

```python
def validate_prompt_input(purpose, category):
    """Validate user inputs"""
    if not purpose or len(purpose) < 5:
        raise ValueError("Purpose must be at least 5 characters")

    if category not in ALLOWED_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")

    # Sanitize SQL inputs
    purpose = purpose.replace("'", "''")

    return purpose, category
```

### 3. Rate Limiting

```python
from functools import wraps
import time

def rate_limit(max_calls=10, period=60):
    """Rate limiting decorator"""
    calls = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - period]

            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")

            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## Scalability Considerations

### Horizontal Scaling

```
┌─────────────┐
│ Load Balancer│
└──────┬───────┘
       │
  ┌────┴────┬────────┬────────┐
  │         │        │        │
┌─▼──┐   ┌──▼─┐   ┌──▼─┐   ┌──▼─┐
│App1│   │App2│   │App3│   │App4│
└─┬──┘   └──┬─┘   └──┬─┘   └──┬─┘
  │         │        │        │
  └────┬────┴────────┴────────┘
       │
  ┌────▼────────┐
  │   Database  │
  │  (SQLite →  │
  │  PostgreSQL)│
  └─────────────┘
```

### Vertical Scaling

- **Database**: SQLite → PostgreSQL for concurrent writes
- **Caching**: Add Redis for template caching
- **Queue**: Add Celery for async model testing
- **Storage**: Move to S3 for template exports

## Monitoring & Analytics

### Key Metrics

```python
# Track in real-time
metrics = {
    'prompts_generated_total': Counter(),
    'prompts_optimized_total': Counter(),
    'model_tests_total': Counter(label='model'),
    'avg_prompt_rating': Gauge(),
    'avg_generation_latency_ms': Histogram(),
    'active_templates': Gauge(),
}
```

### Logging Strategy

```python
import logging

# Structured logging
logger = logging.getLogger('prompt_generator')
logger.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log to file and console
file_handler = logging.FileHandler('logs/prompt_generator.log')
console_handler = logging.StreamHandler()

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
```

## Deployment Architecture

### Local Development

```bash
# Development mode (auto-reload)
python src/scripts/prompt_dashboard.py
# → Flask debug mode on localhost:5000
```

### Production Deployment

```bash
# Use production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.scripts.prompt_dashboard:app

# With nginx reverse proxy
# nginx.conf:
# location / {
#     proxy_pass http://localhost:5000;
# }
```

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY .env .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.scripts.prompt_dashboard:app"]
```

## Future Enhancements

### Phase 1 (Current)
✅ Prompt generation
✅ Multi-model testing
✅ Template library
✅ Web dashboard
✅ CLI interface

### Phase 2 (Planned)
- [ ] Async model testing
- [ ] Advanced analytics dashboard
- [ ] Prompt versioning with git
- [ ] A/B testing framework
- [ ] Custom model fine-tuning

### Phase 3 (Future)
- [ ] Distributed testing
- [ ] Real-time collaboration
- [ ] Prompt marketplace
- [ ] Advanced ML-based optimization
- [ ] Multi-language support

## Conclusion

This architecture provides a scalable, maintainable foundation for AI prompt engineering with:
- Clear separation of concerns
- Multiple interface options
- Self-learning capabilities
- Production-ready deployment
- Extensive integration points

Built with flexibility and extensibility in mind to grow with your needs.

---

**Architecture Version**: 1.0.0
**Last Updated**: 2025-01-08
**Maintainer**: Moon Dev AI Agents Team
