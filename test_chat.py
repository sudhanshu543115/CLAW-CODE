#!/usr/bin/env python3
"""
Test the chat system functionality
"""

from enhanced_chat import EnhancedChat

def test_chat():
    """Test the chat system with a sample conversation"""
    print("🧪 Testing AI Chat System")
    print("=" * 50)
    
    # Create chat instance
    chat = EnhancedChat()
    
    # Test prompts
    test_prompts = [
        "help me debug python code",
        "create a new file",
        "list directory contents"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n📝 Test {i}: {prompt}")
        print("-" * 30)
        
        # Add user message
        chat.add_message('user', prompt)
        
        # Generate response
        response = chat.generate_response(prompt)
        
        # Show response (truncated for readability)
        lines = response.split('\n')
        for line in lines[:10]:  # Show first 10 lines
            print(line)
        if len(lines) > 10:
            print("... (truncated)")
        
        # Add assistant message
        chat.add_message('assistant', response)
    
    # Show stats
    print(f"\n📊 Final Stats:")
    print(f"Total messages: {len(chat.messages)}")
    print(f"AI provider: {chat.ai_provider}")
    
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    test_chat()
