# My AI Chat System

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
