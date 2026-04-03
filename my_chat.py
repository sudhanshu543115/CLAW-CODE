#!/usr/bin/env python3
"""
Simple AI chat system built using Claw Code architecture patterns
"""

import json
import sys
from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path

# Import Claw Code components
from src.runtime import PortRuntime
from src.commands import get_commands
from src.tools import get_tools
from src.models import PortingModule

@dataclass
class ChatMessage:
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str

class SimpleChat:
    def __init__(self):
        self.runtime = PortRuntime()
        self.messages: List[ChatMessage] = []
        self.session_file = Path("chat_history.json")
        
    def add_message(self, role: str, content: str):
        """Add a message to the chat history"""
        import datetime
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=datetime.datetime.now().isoformat()
        )
        self.messages.append(message)
        
    def route_user_input(self, user_input: str) -> List[str]:
        """Route user input to appropriate commands/tools"""
        matches = self.runtime.route_prompt(user_input, limit=5)
        
        responses = []
        for match in matches:
            if match.kind == 'command':
                responses.append(f"🔧 Command: {match.name} ({match.source_hint})")
            elif match.kind == 'tool':
                responses.append(f"⚙️ Tool: {match.name} ({match.source_hint})")
                
        return responses
    
    def simulate_response(self, user_input: str) -> str:
        """Generate a simulated response based on routed matches"""
        matches = self.route_user_input(user_input)
        
        if not matches:
            return "I'm not sure how to handle that. Try asking about code, debugging, or file operations."
        
        response = f"I found {len(matches)} ways to help:\n\n"
        for match in matches:
            response += f"• {match}\n"
            
        response += f"\nLet me simulate what would happen with the first match..."
        
        # Simulate a bootstrap session
        session = self.runtime.bootstrap_session(user_input, limit=3)
        response += f"\n\nSession result: {session.turn_result.output[:200]}..."
        
        return response
    
    def save_session(self):
        """Save chat history to file"""
        data = [
            {
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp
            }
            for msg in self.messages
        ]
        
        with open(self.session_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_session(self):
        """Load chat history from file"""
        if self.session_file.exists():
            with open(self.session_file) as f:
                data = json.load(f)
                for msg_data in data:
                    self.add_message(msg_data['role'], msg_data['content'])
    
    def run(self):
        """Run the interactive chat"""
        print("🤖 Simple AI Chat (built with Claw Code patterns)")
        print("Type 'quit' to exit, 'help' for commands, 'save' to save session")
        print("-" * 50)
        
        self.load_session()
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() == 'quit':
                    print("Goodbye! 👋")
                    break
                    
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                    
                if user_input.lower() == 'save':
                    self.save_session()
                    print(f"Session saved to {self.session_file}")
                    continue
                
                if user_input.lower() == 'load':
                    self.load_session()
                    print(f"Loaded {len(self.messages)} messages from {self.session_file}")
                    continue
                
                # Add user message
                self.add_message('user', user_input)
                
                # Generate and show response
                response = self.simulate_response(user_input)
                print(f"\n🤖: {response}")
                
                # Add assistant message
                self.add_message('assistant', response)
                
            except KeyboardInterrupt:
                print("\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def show_help(self):
        """Show available commands"""
        print("\n📚 Available commands:")
        print("• help - Show this help message")
        print("• save - Save chat history")
        print("• load - Load chat history")
        print("• quit - Exit the chat")
        print("• Any other text will be processed by the AI")

if __name__ == "__main__":
    chat = SimpleChat()
    chat.run()
