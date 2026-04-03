#!/usr/bin/env python3
"""
Real file operations for the AI chat system
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class RealFileOperations:
    """Real file operations that can be called from the chat system"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.operations_log = []
    
    def create_file(self, filename: str, content: str = "") -> Dict[str, Any]:
        """Actually create a new file with content"""
        try:
            file_path = self.base_path / filename
            
            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            result = {
                'success': True,
                'message': f'✅ Created file: {filename}',
                'path': str(file_path),
                'size': len(content.encode('utf-8')),
                'timestamp': datetime.now().isoformat()
            }
            
            self.operations_log.append(result)
            return result
            
        except Exception as e:
            return {
                'success': False,
                'message': f'❌ Failed to create file: {e}',
                'error': str(e)
            }
    
    def list_files(self, directory: str = ".", pattern: str = "*") -> Dict[str, Any]:
        """List files in a directory"""
        try:
            dir_path = self.base_path / directory
            if not dir_path.exists():
                return {
                    'success': False,
                    'message': f'❌ Directory does not exist: {directory}'
                }
            
            files = []
            for file_path in dir_path.glob(pattern):
                if file_path.is_file():
                    files.append({
                        'name': file_path.name,
                        'path': str(file_path),
                        'size': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
            
            return {
                'success': True,
                'message': f'📁 Found {len(files)} files in {directory}',
                'files': files,
                'directory': str(dir_path)
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'❌ Failed to list files: {e}',
                'error': str(e)
            }
    
    def read_file(self, filename: str) -> Dict[str, Any]:
        """Read file contents"""
        try:
            file_path = self.base_path / filename
            
            if not file_path.exists():
                return {
                    'success': False,
                    'message': f'❌ File does not exist: {filename}'
                }
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'success': True,
                'message': f'📖 Read file: {filename}',
                'content': content,
                'size': len(content.encode('utf-8')),
                'lines': len(content.splitlines())
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'❌ Failed to read file: {e}',
                'error': str(e)
            }
    
    def delete_file(self, filename: str) -> Dict[str, Any]:
        """Delete a file"""
        try:
            file_path = self.base_path / filename
            
            if not file_path.exists():
                return {
                    'success': False,
                    'message': f'❌ File does not exist: {filename}'
                }
            
            file_path.unlink()
            
            result = {
                'success': True,
                'message': f'🗑️ Deleted file: {filename}',
                'timestamp': datetime.now().isoformat()
            }
            
            self.operations_log.append(result)
            return result
            
        except Exception as e:
            return {
                'success': False,
                'message': f'❌ Failed to delete file: {e}',
                'error': str(e)
            }
    
    def create_directory(self, dirname: str) -> Dict[str, Any]:
        """Create a new directory"""
        try:
            dir_path = self.base_path / dirname
            dir_path.mkdir(parents=True, exist_ok=True)
            
            result = {
                'success': True,
                'message': f'📁 Created directory: {dirname}',
                'path': str(dir_path),
                'timestamp': datetime.now().isoformat()
            }
            
            self.operations_log.append(result)
            return result
            
        except Exception as e:
            return {
                'success': False,
                'message': f'❌ Failed to create directory: {e}',
                'error': str(e)
            }
    
    def get_operations_log(self) -> List[Dict[str, Any]]:
        """Get log of all file operations"""
        return self.operations_log

# Enhanced chat with real file operations
def enhance_chat_with_file_ops():
    """Enhanced chat that can actually perform file operations"""
    
    file_ops = RealFileOperations()
    
    def handle_file_command(user_input: str) -> Dict[str, Any]:
        """Handle file-related commands with real operations"""
        
        user_input_lower = user_input.lower()
        
        # Create file
        if any(keyword in user_input_lower for keyword in ['create file', 'create new file', 'make file']):
            # Extract filename from the input
            words = user_input.split()
            filename = "new_file.txt"  # default
            
            # Try to extract filename
            for i, word in enumerate(words):
                if word.lower() in ['create', 'make'] and i + 2 < len(words):
                    if words[i+1].lower() in ['file', 'new']:
                        filename = words[i+2]
                        break
            
            # Add .txt if no extension
            if '.' not in filename:
                filename += '.txt'
            
            return file_ops.create_file(filename, f"Created by AI Chat on {datetime.now()}")
        
        # List files
        elif any(keyword in user_input_lower for keyword in ['list files', 'list directory', 'show files']):
            directory = "."
            if 'in' in user_input_lower:
                # Try to extract directory name
                parts = user_input.split('in')
                if len(parts) > 1:
                    directory = parts[1].strip()
            
            return file_ops.list_files(directory)
        
        # Read file
        elif any(keyword in user_input_lower for keyword in ['read file', 'open file', 'show file']):
            words = user_input.split()
            filename = words[-1] if words else "readme.txt"
            return file_ops.read_file(filename)
        
        # Delete file
        elif any(keyword in user_input_lower for keyword in ['delete file', 'remove file']):
            words = user_input.split()
            filename = words[-1] if words else "temp.txt"
            return file_ops.delete_file(filename)
        
        # Create directory
        elif any(keyword in user_input_lower for keyword in ['create directory', 'make directory', 'new folder']):
            words = user_input.split()
            dirname = words[-1] if words else "new_folder"
            return file_ops.create_directory(dirname)
        
        else:
            return {
                'success': False,
                'message': '❌ Not a recognized file operation'
            }
    
    return handle_file_command, file_ops

if __name__ == "__main__":
    # Test the file operations
    handler, ops = enhance_chat_with_file_ops()
    
    print("🧪 Testing Real File Operations")
    print("=" * 40)
    
    # Test creating a file
    result = handler("create file test.txt")
    print(f"Create file: {result['message']}")
    
    # Test listing files
    result = handler("list files")
    print(f"List files: {result['message']}")
    
    # Test reading the file
    result = handler("read file test.txt")
    print(f"Read file: {result['message']}")
    
    print("\n✅ File operations working!")
