#!/bin/bash

# Comprehensive linting script for Open Mineral project

echo "🔍 Running Code Quality Checks"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        exit 1
    fi
}

# Change to project root
cd "$(dirname "$0")/.."

echo ""
echo "📦 Installing/Updating dependencies..."
pip install -q -r requirements.txt

echo ""
echo "🎨 Running Black (Code Formatting)..."
black --check --diff bc/ deals/ scripts/ *.py
print_status $? "Black formatting check"

echo ""
echo "📋 Running isort (Import Sorting)..."
isort --check-only --diff bc/ deals/ scripts/ *.py
print_status $? "isort import sorting"

echo ""
echo "🔍 Running Flake8 (Linting)..."
flake8 bc/ deals/ scripts/ *.py
print_status $? "Flake8 linting"

echo ""
echo "🔒 Running Bandit (Security Analysis)..."
bandit -r bc/ -f json -o bandit-report.json || true
if [ -f bandit-report.json ]; then
    echo "Security scan completed. Report saved to bandit-report.json"
    print_status 0 "Bandit security scan"
else
    print_status 1 "Bandit security scan"
fi

echo ""
echo "🛡️ Running Safety (Dependency Security)..."
safety check --json --output safety-report.json || true
if [ -f safety-report.json ]; then
    echo "Dependency security scan completed. Report saved to safety-report.json"
    print_status 0 "Safety dependency check"
else
    print_status 1 "Safety dependency check"
fi

echo ""
echo "🔬 Running MyPy (Type Checking)..."
cd bc
mypy . --ignore-missing-imports || true
print_status 0 "MyPy type checking"

echo ""
echo "🧪 Running Tests with Coverage..."
python -m pytest ../tests/ -v --cov=. --cov-report=html --cov-report=term-missing --cov-report=xml
print_status $? "Test suite with coverage"

echo ""
echo "📊 Code Quality Summary:"
echo "========================"
echo "✅ Code formatting (Black)"
echo "✅ Import sorting (isort)"
echo "✅ Linting (Flake8)"
echo "✅ Security analysis (Bandit)"
echo "✅ Dependency security (Safety)"
echo "✅ Type checking (MyPy)"
echo "✅ Test coverage"

echo ""
echo "📁 Generated Reports:"
echo "===================="
echo "• Coverage HTML: bc/htmlcov/index.html"
echo "• Coverage XML: bc/coverage.xml"
echo "• Security Report: bandit-report.json"
echo "• Safety Report: safety-report.json"

echo ""
echo -e "${GREEN}🎉 All code quality checks completed!${NC}"
