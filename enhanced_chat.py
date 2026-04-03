#!/usr/bin/env python3
"""
Enhanced AI chat system with real AI integration
"""

import json
import sys
import os
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path

# Import Claw Code components
from src.runtime import PortRuntime
from src.commands import get_commands, execute_command
from src.tools import get_tools, execute_tool

@dataclass
class ChatMessage:
    role: str  # 'user', 'assistant', 'system', 'tool'
    content: str
    timestamp: str
    tool_calls: Optional[List[Dict]] = None

class EnhancedChat:
    def __init__(self, ai_provider: str = "openai"):
        self.runtime = PortRuntime()
        self.messages: List[ChatMessage] = []
        self.session_file = Path("enhanced_chat_history.json")
        self.ai_provider = ai_provider
        self.context_window = 10  # Keep last 10 messages for context
        
    def add_message(self, role: str, content: str, tool_calls: Optional[List[Dict]] = None):
        """Add a message to the chat history"""
        import datetime
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=datetime.datetime.now().isoformat(),
            tool_calls=tool_calls
        )
        self.messages.append(message)
        
        # Keep only recent messages for context
        if len(self.messages) > self.context_window + 5:
            self.messages = self.messages[-self.context_window-5:]
    
    def get_context_messages(self) -> List[Dict]:
        """Get recent messages for AI context"""
        return [
            {
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp
            }
            for msg in self.messages[-self.context_window:]
        ]
    
    def route_and_execute(self, user_input: str) -> Dict[str, Any]:
        """Route user input and execute appropriate commands/tools"""
        results = {
            'routed_matches': [],
            'executed_commands': [],
            'executed_tools': [],
            'errors': []
        }
        
        try:
            # Route the input
            matches = self.runtime.route_prompt(user_input, limit=3)
            results['routed_matches'] = [
                {
                    'kind': match.kind,
                    'name': match.name,
                    'score': match.score,
                    'source': match.source_hint
                }
                for match in matches
            ]
            
            # Execute top command match if any
            command_matches = [m for m in matches if m.kind == 'command']
            if command_matches:
                top_command = command_matches[0]
                try:
                    cmd_result = execute_command(top_command.name, user_input)
                    results['executed_commands'].append({
                        'name': top_command.name,
                        'result': cmd_result.message,
                        'handled': cmd_result.handled
                    })
                except Exception as e:
                    results['errors'].append(f"Command execution failed: {e}")
            
            # Execute top tool match if any
            tool_matches = [m for m in matches if m.kind == 'tool']
            if tool_matches:
                top_tool = tool_matches[0]
                try:
                    tool_result = execute_tool(top_tool.name, user_input)
                    results['executed_tools'].append({
                        'name': top_tool.name,
                        'result': tool_result.message,
                        'handled': tool_result.handled
                    })
                except Exception as e:
                    results['errors'].append(f"Tool execution failed: {e}")
                    
        except Exception as e:
            results['errors'].append(f"Routing failed: {e}")
        
        return results
    
    def call_external_ai(self, prompt: str, context: List[Dict]) -> str:
        """Call external AI API (placeholder for real integration)"""
        # This is where you'd integrate with OpenAI, Anthropic, etc.
        # For now, return a simulated response
        
        context_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context[-3:]])
        
        # Simulate different AI providers
        if self.ai_provider == "openai":
            return f"[OpenAI Simulated] Based on your request '{prompt}', I would help you with that. Context shows: {context_str[:100]}..."
        elif self.ai_provider == "claude":
            return f"[Claude Simulated] I understand you want to {prompt}. Looking at the context: {context_str[:100]}..."
        else:
            return f"[Generic AI] I can help with '{prompt}'. Recent context: {context_str[:100]}..."
    
    def generate_response(self, user_input: str) -> str:
        """Generate a comprehensive response"""
        # Route and execute commands/tools
        execution_results = self.route_and_execute(user_input)
        
        # Get context for AI
        context = self.get_context_messages()
        
        # Build response
        response_parts = []
        
        # Add routing information
        if execution_results['routed_matches']:
            response_parts.append("🔍 **Found matches:**")
            for match in execution_results['routed_matches']:
                emoji = "🔧" if match['kind'] == 'command' else "⚙️"
                response_parts.append(f"  {emoji} {match['kind']}: {match['name']} (score: {match['score']})")
        
        # Add execution results
        if execution_results['executed_commands']:
            response_parts.append("\n🚀 **Executed commands:**")
            for cmd in execution_results['executed_commands']:
                response_parts.append(f"  • {cmd['name']}: {cmd['result']}")
        
        if execution_results['executed_tools']:
            response_parts.append("\n🛠️ **Executed tools:**")
            for tool in execution_results['executed_tools']:
                response_parts.append(f"  • {tool['name']}: {tool['result']}")
        
        # Add AI response
        ai_response = self.call_external_ai(user_input, context)
        response_parts.append(f"\n🤖 **AI Response:**\n{ai_response}")
        
        # Add errors if any
        if execution_results['errors']:
            response_parts.append("\n⚠️ **Errors:**")
            for error in execution_results['errors']:
                response_parts.append(f"  • {error}")
        
        return "\n".join(response_parts)
    
    def save_session(self):
        """Save chat history to file"""
        data = []
        for msg in self.messages:
            msg_data = {
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp
            }
            if msg.tool_calls:
                msg_data['tool_calls'] = msg.tool_calls
            data.append(msg_data)
        
        with open(self.session_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_session(self):
        """Load chat history from file"""
        if self.session_file.exists():
            with open(self.session_file) as f:
                data = json.load(f)
                for msg_data in data:
                    self.add_message(
                        msg_data['role'], 
                        msg_data['content'], 
                        msg_data.get('tool_calls')
                    )
    
    def show_stats(self):
        """Show chat statistics"""
        total_messages = len(self.messages)
        user_messages = len([m for m in self.messages if m.role == 'user'])
        assistant_messages = len([m for m in self.messages if m.role == 'assistant'])
        
        print(f"\n📊 **Chat Statistics:**")
        print(f"  Total messages: {total_messages}")
        print(f"  User messages: {user_messages}")
        print(f"  Assistant messages: {assistant_messages}")
        print(f"  AI provider: {self.ai_provider}")
        print(f"  Session file: {self.session_file}")
    
    def run(self):
        """Run the interactive chat"""
        print("🤖 Enhanced AI Chat (built with Claw Code patterns)")
        print("Features: Command/Tool execution + AI integration")
        print("Commands: help, stats, save, load, quit, provider [openai|claude|generic]")
        print("-" * 70)
        
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
                    
                if user_input.lower() == 'stats':
                    self.show_stats()
                    continue
                    
                if user_input.lower() == 'save':
                    self.save_session()
                    print(f"✅ Session saved to {self.session_file}")
                    continue
                
                if user_input.lower() == 'load':
                    self.load_session()
                    print(f"✅ Loaded {len(self.messages)} messages")
                    continue
                
                if user_input.lower().startswith('provider '):
                    provider = user_input.split(' ', 1)[1].lower()
                    if provider in ['openai', 'claude', 'generic']:
                        self.ai_provider = provider
                        print(f"✅ AI provider set to {provider}")
                    else:
                        print("❌ Available providers: openai, claude, generic")
                    continue
                
                # Add user message
                self.add_message('user', user_input)
                
                # Generate and show response
                response = self.generate_response(user_input)
                print(f"\n🤖: {response}")
                
                # Add assistant message
                self.add_message('assistant', response)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show available commands"""
        print("\n📚 **Available commands:**")
        print("• help - Show this help message")
        print("• stats - Show chat statistics")
        print("• save - Save chat history")
        print("• load - Load chat history")
        print("• provider [name] - Switch AI provider (openai/claude/generic)")
        print("• quit - Exit the chat")
        print("\n**Example prompts:**")
        print("• 'help me debug python code'")
        print("• 'create a new file'")
        print("• 'list directory contents'")

if __name__ == "__main__":
    chat = EnhancedChat()
    chat.run()
