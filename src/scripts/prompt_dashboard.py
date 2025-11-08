#!/usr/bin/env python3
"""
AI Prompt Generator Web Dashboard
Flask-based web interface with real-time updates
"""

import os
import sys
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.prompt_generator_agent import PromptGeneratorAgent

app = Flask(__name__)
CORS(app)

# Initialize agent
agent = PromptGeneratorAgent()

# Ensure template library exists
try:
    templates = agent.get_all_templates()
    if len(templates) == 0:
        print("Initializing template library...")
        agent.create_template_library()
except Exception as e:
    print(f"Creating template library: {e}")
    agent.create_template_library()


@app.route('/')
def index():
    """Main dashboard"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Prompt Generator Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }

        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #666;
            font-size: 1.1em;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        }

        .card h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.5em;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }

        input, textarea, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }

        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }

        textarea {
            min-height: 120px;
            resize: vertical;
            font-family: 'Courier New', monospace;
        }

        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        button:active {
            transform: translateY(0);
        }

        .output {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin-top: 20px;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.6;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #667eea;
            font-size: 16px;
        }

        .loading.active {
            display: block;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }

        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }

        .template-list {
            max-height: 400px;
            overflow-y: auto;
        }

        .template-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: background 0.2s ease;
        }

        .template-item:hover {
            background: #e9ecef;
        }

        .template-name {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }

        .template-desc {
            font-size: 0.9em;
            color: #666;
        }

        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-right: 5px;
            margin-top: 5px;
        }

        .badge-category {
            background: #667eea;
            color: white;
        }

        .badge-rating {
            background: #28a745;
            color: white;
        }

        .success {
            color: #28a745;
            font-weight: bold;
        }

        .error {
            color: #dc3545;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Ultimate AI Prompt Generator</h1>
            <p class="subtitle">Generate, optimize, and test AI prompts across multiple models</p>
        </div>

        <div class="dashboard-grid">
            <!-- Generate Prompt Card -->
            <div class="card">
                <h2>📝 Generate Prompt</h2>
                <div class="form-group">
                    <label>Purpose</label>
                    <textarea id="generatePurpose" placeholder="What should this prompt accomplish?"></textarea>
                </div>
                <div class="form-group">
                    <label>Category</label>
                    <select id="generateCategory">
                        <option value="general">General</option>
                        <option value="trading">Trading</option>
                        <option value="analysis">Analysis</option>
                        <option value="content_creation">Content Creation</option>
                        <option value="automation">Automation</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>
                        <input type="checkbox" id="autoOptimize" checked> Auto-optimize
                    </label>
                </div>
                <button onclick="generatePrompt()">Generate Prompt</button>
                <div class="loading" id="generateLoading">
                    <div class="spinner"></div>
                    Generating prompt...
                </div>
                <div class="output" id="generateOutput" style="display:none;"></div>
            </div>

            <!-- Optimize Prompt Card -->
            <div class="card">
                <h2>🔧 Optimize Prompt</h2>
                <div class="form-group">
                    <label>Existing Prompt</label>
                    <textarea id="optimizePrompt" placeholder="Paste your prompt here..."></textarea>
                </div>
                <div class="form-group">
                    <label>Purpose</label>
                    <input type="text" id="optimizePurpose" placeholder="What does this prompt do?">
                </div>
                <button onclick="optimizePrompt()">Optimize</button>
                <div class="loading" id="optimizeLoading">
                    <div class="spinner"></div>
                    Optimizing prompt...
                </div>
                <div class="output" id="optimizeOutput" style="display:none;"></div>
            </div>

            <!-- Test Prompt Card -->
            <div class="card">
                <h2>🧪 Test Multi-Model</h2>
                <div class="form-group">
                    <label>Prompt Template</label>
                    <textarea id="testPrompt" placeholder="Enter prompt with {variables}"></textarea>
                </div>
                <div class="form-group">
                    <label>Test Data (JSON)</label>
                    <input type="text" id="testData" placeholder='{"variable": "value"}'>
                </div>
                <div class="form-group">
                    <label>Models</label>
                    <select id="testModels" multiple size="5">
                        <option value="anthropic" selected>Anthropic Claude</option>
                        <option value="openai">OpenAI GPT-4</option>
                        <option value="deepseek">DeepSeek</option>
                        <option value="groq">Groq</option>
                        <option value="gemini">Google Gemini</option>
                    </select>
                </div>
                <button onclick="testPrompt()">Run Tests</button>
                <div class="loading" id="testLoading">
                    <div class="spinner"></div>
                    Testing across models...
                </div>
                <div class="output" id="testOutput" style="display:none;"></div>
            </div>

            <!-- Statistics Card -->
            <div class="card">
                <h2>📊 Statistics</h2>
                <button onclick="loadStats()">Refresh Stats</button>
                <div id="statsContainer"></div>
            </div>
        </div>

        <!-- Template Library -->
        <div class="card">
            <h2>📚 Template Library</h2>
            <button onclick="loadTemplates()">Load Templates</button>
            <button onclick="exportTemplates()" style="margin-left: 10px;">Export All</button>
            <div class="template-list" id="templateList"></div>
        </div>
    </div>

    <script>
        const API_BASE = '';

        async function generatePrompt() {
            const purpose = document.getElementById('generatePurpose').value;
            const category = document.getElementById('generateCategory').value;
            const autoOptimize = document.getElementById('autoOptimize').checked;

            if (!purpose) {
                alert('Please enter a purpose');
                return;
            }

            document.getElementById('generateLoading').classList.add('active');
            document.getElementById('generateOutput').style.display = 'none';

            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({purpose, category, auto_optimize: autoOptimize})
                });

                const data = await response.json();

                let output = '';
                if (data.error) {
                    output = `<span class="error">Error: ${data.error}</span>`;
                } else {
                    output = `<span class="success">✓ Prompt Generated!</span>\n\n`;
                    output += `<strong>Template:</strong>\n${data.prompt_template}\n\n`;
                    output += `<strong>Variables:</strong> ${JSON.stringify(data.variables)}\n\n`;
                    output += `<strong>Description:</strong> ${data.description}`;

                    if (data.optimization_notes) {
                        output += `\n\n<strong>Optimizations:</strong>\n`;
                        data.optimization_notes.forEach(note => output += `• ${note}\n`);
                    }
                }

                document.getElementById('generateOutput').innerHTML = output;
                document.getElementById('generateOutput').style.display = 'block';
            } catch (error) {
                document.getElementById('generateOutput').innerHTML =
                    `<span class="error">Error: ${error.message}</span>`;
                document.getElementById('generateOutput').style.display = 'block';
            } finally {
                document.getElementById('generateLoading').classList.remove('active');
            }
        }

        async function optimizePrompt() {
            const prompt = document.getElementById('optimizePrompt').value;
            const purpose = document.getElementById('optimizePurpose').value;

            if (!prompt || !purpose) {
                alert('Please fill in both fields');
                return;
            }

            document.getElementById('optimizeLoading').classList.add('active');
            document.getElementById('optimizeOutput').style.display = 'none';

            try {
                const response = await fetch('/api/optimize', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt, purpose})
                });

                const data = await response.json();

                let output = '';
                if (data.improved) {
                    output = `<span class="success">✓ Prompt Optimized!</span>\n\n`;
                    output += `<strong>Optimized Prompt:</strong>\n${data.optimized_prompt}\n\n`;
                    output += `<strong>Score:</strong> ${data.effectiveness_score}/100\n\n`;
                    output += `<strong>Improvements:</strong>\n`;
                    data.improvements.forEach(imp => output += `• ${imp}\n`);
                    output += `\n<strong>Reasoning:</strong>\n${data.reasoning}`;
                } else {
                    output = '<span class="success">✓ Prompt is already optimal!</span>';
                }

                document.getElementById('optimizeOutput').innerHTML = output;
                document.getElementById('optimizeOutput').style.display = 'block';
            } catch (error) {
                document.getElementById('optimizeOutput').innerHTML =
                    `<span class="error">Error: ${error.message}</span>`;
                document.getElementById('optimizeOutput').style.display = 'block';
            } finally {
                document.getElementById('optimizeLoading').classList.remove('active');
            }
        }

        async function testPrompt() {
            const prompt = document.getElementById('testPrompt').value;
            const testDataStr = document.getElementById('testData').value;
            const modelSelect = document.getElementById('testModels');
            const models = Array.from(modelSelect.selectedOptions).map(opt => opt.value);

            if (!prompt || !testDataStr) {
                alert('Please fill in all fields');
                return;
            }

            let testData;
            try {
                testData = JSON.parse(testDataStr);
            } catch (e) {
                alert('Invalid JSON in test data');
                return;
            }

            document.getElementById('testLoading').classList.add('active');
            document.getElementById('testOutput').style.display = 'none';

            try {
                const response = await fetch('/api/test', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt, test_data: testData, models})
                });

                const data = await response.json();

                let output = '<span class="success">✓ Test Results</span>\n\n';

                for (const [model, result] of Object.entries(data.results)) {
                    if (result.success) {
                        output += `<strong>${model.toUpperCase()}:</strong> ✓\n`;
                        output += `  Latency: ${result.latency_ms.toFixed(0)}ms\n`;
                        output += `  Response: ${result.response.substring(0, 100)}...\n\n`;
                    } else {
                        output += `<strong>${model.toUpperCase()}:</strong> ✗\n`;
                        output += `  Error: ${result.error}\n\n`;
                    }
                }

                const analysis = data.analysis;
                output += `<strong>ANALYSIS:</strong>\n`;
                output += `Fastest: ${analysis.fastest_model} (${analysis.fastest_latency_ms.toFixed(0)}ms)\n`;
                output += `Recommendation: ${analysis.recommendation}`;

                document.getElementById('testOutput').innerHTML = output;
                document.getElementById('testOutput').style.display = 'block';
            } catch (error) {
                document.getElementById('testOutput').innerHTML =
                    `<span class="error">Error: ${error.message}</span>`;
                document.getElementById('testOutput').style.display = 'block';
            } finally {
                document.getElementById('testLoading').classList.remove('active');
            }
        }

        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();

                let html = '<div class="stats-grid">';
                html += `<div class="stat-card"><div class="stat-value">${data.total_templates}</div><div class="stat-label">Total Templates</div></div>`;
                html += `<div class="stat-card"><div class="stat-value">${data.categories}</div><div class="stat-label">Categories</div></div>`;
                html += `<div class="stat-card"><div class="stat-value">${data.avg_rating.toFixed(2)}</div><div class="stat-label">Avg Rating</div></div>`;
                html += '</div>';

                document.getElementById('statsContainer').innerHTML = html;
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }

        async function loadTemplates() {
            try {
                const response = await fetch('/api/templates');
                const templates = await response.json();

                let html = '';
                templates.forEach(t => {
                    html += `<div class="template-item">`;
                    html += `<div class="template-name">${t.name}</div>`;
                    html += `<div class="template-desc">${t.description}</div>`;
                    html += `<span class="badge badge-category">${t.category}</span>`;
                    html += `<span class="badge badge-rating">★ ${t.rating.toFixed(2)}</span>`;
                    html += `</div>`;
                });

                document.getElementById('templateList').innerHTML = html || 'No templates found';
            } catch (error) {
                console.error('Error loading templates:', error);
            }
        }

        async function exportTemplates() {
            window.location.href = '/api/export';
        }

        // Load stats on page load
        window.onload = () => {
            loadStats();
            loadTemplates();
        };
    </script>
</body>
</html>
    """


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint for prompt generation"""
    data = request.json
    result = agent.generate_prompt(
        purpose=data.get('purpose'),
        context=data.get('context'),
        category=data.get('category', 'general'),
        auto_optimize=data.get('auto_optimize', True)
    )
    return jsonify(result)


@app.route('/api/optimize', methods=['POST'])
def api_optimize():
    """API endpoint for prompt optimization"""
    data = request.json
    result = agent.optimize_prompt(
        prompt=data.get('prompt'),
        purpose=data.get('purpose')
    )
    return jsonify(result)


@app.route('/api/test', methods=['POST'])
def api_test():
    """API endpoint for multi-model testing"""
    data = request.json
    result = agent.test_prompt_multi_model(
        prompt_template=data.get('prompt'),
        test_data=data.get('test_data', {}),
        models=data.get('models')
    )
    return jsonify(result)


@app.route('/api/templates')
def api_templates():
    """API endpoint to get all templates"""
    templates = agent.get_all_templates()
    return jsonify(templates)


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    templates = agent.get_all_templates()

    categories = set(t['category'] for t in templates)
    avg_rating = sum(t['rating'] for t in templates) / len(templates) if templates else 0

    return jsonify({
        'total_templates': len(templates),
        'categories': len(categories),
        'avg_rating': avg_rating,
        'total_usage': sum(t['usage_count'] for t in templates)
    })


@app.route('/api/export')
def api_export():
    """API endpoint to export templates"""
    filepath = agent.export_templates()
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    return send_from_directory(directory, filename, as_attachment=True)


def main():
    print("\n" + "="*60)
    print("  🚀 AI PROMPT GENERATOR DASHBOARD")
    print("="*60)
    print("\n  Access the dashboard at: http://localhost:5000")
    print("  Press Ctrl+C to stop the server\n")

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    main()
