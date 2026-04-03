#!/usr/bin/env python3
"""
Web-based AI chat interface using Flask and Claw Code patterns
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import json
import uuid
from datetime import datetime
from pathlib import Path

# Import Claw Code components
from src.runtime import PortRuntime
from src.commands import execute_command
from src.tools import execute_tool
from real_file_tools import enhance_chat_with_file_ops

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

class WebChatSession:
    def __init__(self):
        self.runtime = PortRuntime()
        self.messages = []
        self.session_id = str(uuid.uuid4())
        # Add real file operations
        self.file_handler, self.file_ops = enhance_chat_with_file_ops()
        
    def add_message(self, role: str, content: str):
        """Add a message to the chat"""
        message = {
            'id': str(uuid.uuid4()),
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        self.messages.append(message)
        return message
    
    def process_message(self, user_input: str) -> dict:
        """Process user message and generate response"""
        # Add user message
        user_msg = self.add_message('user', user_input)
        
        response_parts = []
        
        # First try real file operations
        file_result = self.file_handler(user_input)
        if file_result.get('success', False):
            response_parts.append(f"🎯 **File Operation:** {file_result['message']}")
            
            # If it was a list operation, show the files
            if 'files' in file_result:
                response_parts.append("\n📁 **Files found:**")
                for file_info in file_result['files'][:10]:  # Show first 10
                    response_parts.append(f"  • {file_info['name']} ({file_info['size']} bytes)")
            
            # If it was a read operation, show content preview
            if 'content' in file_result:
                content = file_result['content']
                preview = content[:200] + "..." if len(content) > 200 else content
                response_parts.append(f"\n📖 **Content preview:**\n```\n{preview}\n```")
        else:
            # Fall back to Claw Code routing
            try:
                matches = self.runtime.route_prompt(user_input, limit=3)
                
                if matches:
                    response_parts.append("🔍 **Found matches:**")
                    for match in matches:
                        emoji = "🔧" if match.kind == 'command' else "⚙️"
                        response_parts.append(f"  {emoji} {match.name} ({match.source_hint})")
                    
                    # Execute top match
                    top_match = matches[0]
                    try:
                        if top_match.kind == 'command':
                            result = execute_command(top_match.name, user_input)
                            response_parts.append(f"\n🚀 **Command result:** {result.message}")
                        else:
                            result = execute_tool(top_match.name, user_input)
                            response_parts.append(f"\n🛠️ **Tool result:** {result.message}")
                    except Exception as e:
                        response_parts.append(f"\n❌ **Execution error:** {e}")
                else:
                    response_parts.append("🤔 **No specific commands/tools found. Using general AI response.**")
                    response_parts.append(f"I understand you want to: {user_input}")
                    response_parts.append("This would be handled by a general AI assistant.")
                    
            except Exception as e:
                response_parts.append(f"❌ **Error processing request:** {e}")
        
        response_text = "\n".join(response_parts)
        
        # Add assistant message
        assistant_msg = self.add_message('assistant', response_text)
        
        return {
            'user_message': user_msg,
            'assistant_message': assistant_msg,
            'session_id': self.session_id
        }

# Store active sessions
active_sessions = {}

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for chat messages"""
    data = request.get_json()
    user_input = data.get('message', '')
    session_id = data.get('session_id', '')
    
    # Get or create session
    if session_id not in active_sessions:
        active_sessions[session_id] = WebChatSession()
    
    chat_session = active_sessions[session_id]
    
    # Process message
    result = chat_session.process_message(user_input)
    
    return jsonify(result)

@app.route('/api/sessions', methods=['GET'])
def api_sessions():
    """List active sessions"""
    return jsonify({
        'sessions': list(active_sessions.keys()),
        'count': len(active_sessions)
    })

@app.route('/api/session/<session_id>/messages', methods=['GET'])
def api_session_messages(session_id):
    """Get messages for a specific session"""
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify({
        'messages': active_sessions[session_id].messages,
        'session_id': session_id
    })

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    emit('status', {'msg': 'Connected to chat server'})

@socketio.on('message')
def handle_message(data):
    """Handle WebSocket message"""
    user_input = data.get('message', '')
    session_id = data.get('session_id', '')
    
    # Get or create session
    if session_id not in active_sessions:
        active_sessions[session_id] = WebChatSession()
    
    chat_session = active_sessions[session_id]
    
    # Process message
    result = chat_session.process_message(user_input)
    
    # Emit response
    emit('response', result)

if __name__ == '__main__':
    print("🌐 Starting Web Chat Server...")
    print("Open http://localhost:5000 in your browser")
    print("Built with Claw Code architecture patterns")
    
    # Create templates directory and HTML file
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chat - Claw Code Architecture</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 10px 10px 0 0; }
        .chat-window { height: 400px; overflow-y: auto; padding: 20px; border-bottom: 1px solid #eee; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; max-width: 80%%; }
        .user { background: #3498db; color: white; margin-left: auto; text-align: right; }
        .assistant { background: #2ecc71; color: white; }
        .input-area { padding: 20px; display: flex; gap: 10px; }
        .input-area input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .input-area button { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .input-area button:hover { background: #2980b9; }
        .status { padding: 10px; background: #ecf0f1; text-align: center; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Chat - Claw Code Architecture</h1>
            <p>Powered by Claw Code command/tool routing patterns</p>
        </div>
        
        <div class="chat-window" id="chatWindow">
            <div class="message assistant">
                👋 Welcome! I'm an AI assistant built using Claw Code architecture patterns. I can route your requests to appropriate commands and tools. Try asking me to help with code, files, or debugging!
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
        
        <div class="status" id="status">Connected</div>
    </div>

    <script>
        const socket = io();
        let sessionId = Math.random().toString(36).substr(2, 9);
        
        socket.on('connect', function() {
            updateStatus('Connected');
        });
        
        socket.on('response', function(data) {
            addMessage('assistant', data.assistant_message.content);
        });
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message) {
                addMessage('user', message);
                socket.emit('message', {message: message, session_id: sessionId});
                input.value = '';
            }
        }
        
        function addMessage(role, content) {
            const chatWindow = document.getElementById('chatWindow');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            messageDiv.innerHTML = content.replace(/\\n/g, '<br>');
            chatWindow.appendChild(messageDiv);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function updateStatus(message) {
            document.getElementById('status').textContent = message;
        }
    </script>
</body>
</html>'''
    
    with open(templates_dir / 'chat.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
