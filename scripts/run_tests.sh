#!/bin/bash

# Test runner script for Open Mineral project

echo "🧪 Running Open Mineral Test Suite"
echo "=================================="

# Change to Django project directory
cd bc

# Set test environment
export DJANGO_SETTINGS_MODULE=bc.settings_test

# Run different test suites
echo ""
echo "📋 Running Unit Tests..."
python -m pytest ../tests/test_models/ -v --tb=short

echo ""
echo "🌐 Running API Tests..."
python -m pytest ../tests/test_views/ -v --tb=short

echo ""
echo "🔄 Running Integration Tests..."
python -m pytest ../tests/test_integration/ -v --tb=short

echo ""
echo "📊 Running All Tests with Coverage..."
python -m pytest ../tests/ -v --cov=. --cov-report=html --cov-report=term-missing

echo ""
echo "✅ Test Suite Complete!"
echo "Coverage report available at: htmlcov/index.html"
