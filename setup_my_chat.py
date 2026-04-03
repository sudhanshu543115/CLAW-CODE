#!/usr/bin/env python3
"""
Setup script for building your own AI chat system using Claw Code patterns
"""

import subprocess
import sys
from pathlib import Path

def install_requirements():
    """Install required packages"""
    requirements = [
        'flask',
        'flask-socketio',
        'requests',
        'python-dotenv'
    ]
    
    print("📦 Installing required packages...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def create_env_file():
    """Create environment file for API keys"""
    env_content = """# AI Chat Environment Variables
# Add your API keys here

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Other settings
DEBUG=True
FLASK_ENV=development
"""
    
    env_file = Path('.env')
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file - add your API keys there!")
    else:
        print("ℹ️ .env file already exists")
    
    return env_file

def create_readme():
    """Create README for the chat system"""
    readme_content = """# My AI Chat System

Built using Claw Code architecture patterns, this chat system demonstrates how to create an AI assistant with command/tool routing.

## Features

- 🔍 **Command/Tool Routing**: Routes user requests to appropriate handlers
- ⚙️ **Real Execution**: Executes actual commands and tools from the Claw Code system
- 🤖 **AI Integration**: Placeholder for real AI API integration
- 💬 **Multiple Interfaces**: CLI, enhanced CLI, and web interface
- 💾 **Session Management**: Save and load chat history

## Quick Start

1. **Install dependencies:**
   ```bash
   python setup_my_chat.py
   ```

2. **Set up API keys:**
   Edit the `.env` file and add your API keys

3. **Run the chat:**

   **Simple CLI:**
   ```bash
   python my_chat.py
   ```

   **Enhanced CLI:**
   ```bash
   python enhanced_chat.py
   ```

   **Web Interface:**
   ```bash
   python web_chat.py
   ```
   Then open http://localhost:5000

## Architecture

This system is built using Claw Code patterns:

- **Runtime**: Manages session state and routing
- **Commands**: Handle specific user requests
- **Tools**: Execute specific operations
- **Query Engine**: Routes prompts to appropriate handlers

## Example Usage

Try these prompts:
- "help me debug python code"
- "create a new file"
- "list directory contents"
- "show system information"

## Customization

### Adding Your Own Commands

1. Create a new command function
2. Register it in the command registry
3. The routing system will automatically find it

### Adding AI Integration

Replace the simulated AI responses in `enhanced_chat.py` with real API calls:

```python
def call_openai(self, prompt, context):
    import openai
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        # ... other parameters
    )
    return response.choices[0].message.content
```

## Next Steps

1. Add real AI API integration
2. Create custom commands/tools
3. Add file system operations
4. Implement memory/context management
5. Add user authentication
6. Deploy to production

## Built With

- **Claw Code Architecture**: Command/tool routing patterns
- **Flask**: Web interface
- **Socket.IO**: Real-time communication
- **Python**: Core implementation

---

This is a demonstration of how to build AI systems using proven architecture patterns from Claw Code.
"""
    
    with open('README_MyChat.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Created README_MyChat.md")

def main():
    """Main setup function"""
    print("🚀 Setting up your AI Chat System")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        return
    
    # Create environment file
    env_file = create_env_file()
    
    # Create README
    create_readme()
    
    print("\n✅ Setup complete!")
    print("\n📋 Next steps:")
    print(f"1. Edit {env_file} and add your API keys")
    print("2. Run one of the chat interfaces:")
    print("   - python my_chat.py (simple)")
    print("   - python enhanced_chat.py (enhanced)")
    print("   - python web_chat.py (web interface)")
    print("3. Check README_MyChat.md for more details")

if __name__ == "__main__":
    main()
