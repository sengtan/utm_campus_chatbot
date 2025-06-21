#!/usr/bin/env python3
"""
Setup script for UTM Campus Assistant with self-hosted DeepSeek LLM
"""

import os
import subprocess
import sys
import requests
import time

def check_deepseek_connection(url, model):
    """Test connection to DeepSeek API"""
    try:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except:
        return False

def setup_environment():
    """Set up environment variables"""
    env_vars = {
        'DEEPSEEK_API_URL': 'http://localhost:11434/v1/chat/completions',
        'DEEPSEEK_MODEL': 'deepseek-r1:7b',
        'SESSION_SECRET': 'your-secret-key-change-this',
        'DATABASE_URL': 'postgresql://postgres:password@localhost:5432/utm_campus'
    }
    
    print("Setting up environment variables...")
    for key, default_value in env_vars.items():
        current_value = os.environ.get(key)
        if not current_value:
            os.environ[key] = default_value
            print(f"✓ {key} = {default_value}")
        else:
            print(f"✓ {key} already set")

def check_ollama():
    """Check if Ollama is running and has DeepSeek model"""
    try:
        # Check if Ollama is running
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            deepseek_models = [m for m in models if 'deepseek' in m.get('name', '').lower()]
            
            if deepseek_models:
                print("✓ Ollama is running with DeepSeek model")
                return True
            else:
                print("⚠ Ollama is running but DeepSeek model not found")
                print("Run: ollama pull deepseek-r1:7b")
                return False
        else:
            print("⚠ Ollama API not responding")
            return False
    except:
        print("⚠ Ollama not running. Please start with: ollama serve")
        return False

def test_chatbot():
    """Test the chatbot functionality"""
    url = os.environ.get('DEEPSEEK_API_URL')
    model = os.environ.get('DEEPSEEK_MODEL')
    
    print(f"\nTesting DeepSeek connection...")
    print(f"URL: {url}")
    print(f"Model: {model}")
    
    if check_deepseek_connection(url, model):
        print("✓ DeepSeek API connection successful")
        return True
    else:
        print("✗ DeepSeek API connection failed")
        return False

def main():
    print("UTM Campus Assistant - DeepSeek Setup")
    print("=" * 40)
    
    # Set up environment
    setup_environment()
    
    # Check Ollama
    print("\nChecking Ollama status...")
    ollama_ok = check_ollama()
    
    # Test API connection
    if ollama_ok:
        api_ok = test_chatbot()
        if api_ok:
            print("\n✓ Setup complete! Your DeepSeek integration is ready.")
            print("\nTo start the application:")
            print("1. python main.py")
            print("2. In another terminal: ngrok http 5000")
        else:
            print("\n⚠ Setup incomplete. Please check DeepSeek configuration.")
    else:
        print("\n⚠ Please install and start Ollama with DeepSeek model first.")
        print("\nQuick setup:")
        print("1. curl -fsSL https://ollama.ai/install.sh | sh")
        print("2. ollama serve")
        print("3. ollama pull deepseek-r1:7b")
        print("4. python setup_deepseek.py")

if __name__ == "__main__":
    main()