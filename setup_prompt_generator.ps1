# Ultimate AI Prompt Generator - Windows Setup Script
# PowerShell installation and configuration script

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  AI PROMPT GENERATOR - SETUP" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Warning: Not running as Administrator. Some features may require elevation." -ForegroundColor Yellow
    Write-Host ""
}

# Check Python installation
Write-Host "[1/8] Checking Python installation..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found! Please install Python 3.8+ from python.org" -ForegroundColor Red
    exit 1
}

# Check Anaconda/Conda
Write-Host "[2/8] Checking Conda installation..." -ForegroundColor Green
try {
    $condaVersion = conda --version 2>&1
    Write-Host "  ✓ Found: $condaVersion" -ForegroundColor Green

    # Activate tflow environment
    Write-Host "  Activating 'tflow' environment..." -ForegroundColor Yellow
    conda activate tflow 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Environment 'tflow' activated" -ForegroundColor Green
    } else {
        Write-Host "  ! Creating 'tflow' environment..." -ForegroundColor Yellow
        conda create -n tflow python=3.10 -y
        conda activate tflow
    }
} catch {
    Write-Host "  ! Conda not found. Using system Python..." -ForegroundColor Yellow
}

# Install required packages
Write-Host "[3/8] Installing required Python packages..." -ForegroundColor Green
$packages = @(
    "flask",
    "flask-cors",
    "prompt_toolkit",
    "termcolor",
    "anthropic",
    "openai",
    "google-generativeai",
    "groq",
    "requests",
    "pandas",
    "numpy"
)

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -ForegroundColor Yellow
    pip install $package --quiet
}

# Update requirements.txt
Write-Host "  Updating requirements.txt..." -ForegroundColor Yellow
pip freeze > requirements.txt
Write-Host "  ✓ Packages installed" -ForegroundColor Green

# Create data directories
Write-Host "[4/8] Creating data directories..." -ForegroundColor Green
$dataDir = "src\data\prompt_generator"
if (-not (Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
    Write-Host "  ✓ Created $dataDir" -ForegroundColor Green
} else {
    Write-Host "  ✓ Directory already exists" -ForegroundColor Green
}

# Initialize database
Write-Host "[5/8] Initializing prompt database..." -ForegroundColor Green
python -c "from src.agents.prompt_generator_agent import PromptGeneratorAgent; agent = PromptGeneratorAgent(); agent.create_template_library(); print('  ✓ Database initialized')"

# Check for .env file
Write-Host "[6/8] Checking environment configuration..." -ForegroundColor Green
if (-not (Test-Path ".env")) {
    Write-Host "  ! .env file not found" -ForegroundColor Yellow
    Write-Host "  Creating .env from template..." -ForegroundColor Yellow

    if (Test-Path ".env_example") {
        Copy-Item ".env_example" ".env"
        Write-Host "  ✓ Created .env file - Please configure your API keys!" -ForegroundColor Green
    } else {
        Write-Host "  ✗ .env_example not found" -ForegroundColor Red
    }
} else {
    Write-Host "  ✓ .env file exists" -ForegroundColor Green
}

# Create VS Code integration
Write-Host "[7/8] Setting up VS Code integration..." -ForegroundColor Green
$vscodeDir = ".vscode"
if (-not (Test-Path $vscodeDir)) {
    New-Item -ItemType Directory -Path $vscodeDir -Force | Out-Null
}

# Create VS Code tasks
$tasksJson = @"
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Start Prompt Generator Dashboard",
            "type": "shell",
            "command": "python",
            "args": ["src/scripts/prompt_dashboard.py"],
            "problemMatcher": [],
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Start Prompt Generator CLI",
            "type": "shell",
            "command": "python",
            "args": ["src/scripts/prompt_cli.py"],
            "problemMatcher": [],
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Run Prompt Generator Agent",
            "type": "shell",
            "command": "python",
            "args": ["src/agents/prompt_generator_agent.py"],
            "problemMatcher": []
        },
        {
            "label": "Initialize Template Library",
            "type": "shell",
            "command": "python",
            "args": ["src/scripts/prompt_cli.py", "--init-library"],
            "problemMatcher": []
        },
        {
            "label": "Run All Tests",
            "type": "shell",
            "command": "python",
            "args": ["-m", "pytest", "tests/", "-v"],
            "problemMatcher": []
        },
        {
            "label": "Lint Code (pylint)",
            "type": "shell",
            "command": "pylint",
            "args": ["src/agents/prompt_generator_agent.py", "src/scripts/prompt_cli.py"],
            "problemMatcher": []
        }
    ]
}
"@

$tasksJson | Out-File -FilePath "$vscodeDir\tasks.json" -Encoding UTF8
Write-Host "  ✓ VS Code tasks configured" -ForegroundColor Green

# Create launch.json for debugging
$launchJson = @"
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Prompt Generator: Dashboard",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/scripts/prompt_dashboard.py",
            "console": "integratedTerminal"
        },
        {
            "name": "Prompt Generator: CLI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/scripts/prompt_cli.py",
            "console": "integratedTerminal"
        },
        {
            "name": "Prompt Generator: Agent",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/agents/prompt_generator_agent.py",
            "console": "integratedTerminal"
        }
    ]
}
"@

$launchJson | Out-File -FilePath "$vscodeDir\launch.json" -Encoding UTF8
Write-Host "  ✓ VS Code debug configurations created" -ForegroundColor Green

# Test installation
Write-Host "[8/8] Running installation test..." -ForegroundColor Green
try {
    python -c "from src.agents.prompt_generator_agent import PromptGeneratorAgent; print('  ✓ Import test passed')" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Installation test passed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Installation test failed" -ForegroundColor Red
    }
} catch {
    Write-Host "  ✗ Import test failed: $_" -ForegroundColor Red
}

# Summary
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  SETUP COMPLETE!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Configure your API keys in .env file" -ForegroundColor White
Write-Host "  2. Start the web dashboard:" -ForegroundColor White
Write-Host "     python src/scripts/prompt_dashboard.py" -ForegroundColor Green
Write-Host "  3. Or use the CLI:" -ForegroundColor White
Write-Host "     python src/scripts/prompt_cli.py" -ForegroundColor Green
Write-Host "  4. Or run standalone agent:" -ForegroundColor White
Write-Host "     python src/agents/prompt_generator_agent.py" -ForegroundColor Green
Write-Host ""
Write-Host "VS Code Integration:" -ForegroundColor Yellow
Write-Host "  - Press Ctrl+Shift+P -> 'Tasks: Run Task'" -ForegroundColor White
Write-Host "  - Select 'Start Prompt Generator Dashboard'" -ForegroundColor White
Write-Host ""
Write-Host "Access dashboard at: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""

# Optionally start dashboard
$startDashboard = Read-Host "Start dashboard now? (y/n)"
if ($startDashboard -eq 'y') {
    Write-Host ""
    Write-Host "Starting dashboard..." -ForegroundColor Green
    python src/scripts/prompt_dashboard.py
}
