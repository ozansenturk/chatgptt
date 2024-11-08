// File: src/components/Chat.js
import React, { useState, useEffect, useRef } from 'react';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const ws = useRef(null);
    
    useEffect(() => {
        ws.current = new WebSocket(
            process.env.NODE_ENV === 'development'
              ? 'ws://localhost:8000/ws/chat'    // Local development
              : 'ws://localhost:8000/ws/chat'      // Docker
          );
        // ws.current = new WebSocket('ws://backend:8000/ws/chat');
        
        ws.current.onmessage = (event) => {
            setMessages((prev) => [...prev, event.data]);
        };

        ws.current.onclose = () => {
            console.log("WebSocket closed.");
        };

        return () => {
            ws.current.close();
        };
    }, []);

    const sendMessage = () => {
        if (input.trim()) {
            ws.current.send(input);
            setInput('');
        }
    };

    return (
        <div style={{ maxWidth: '500px', margin: 'auto', padding: '1rem' }}>
            <div style={{ height: '400px', overflowY: 'scroll', border: '1px solid gray', marginBottom: '1rem' }}>
                {messages.map((msg, index) => (
                    <div key={index}>{msg}</div>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Type a message..."
                style={{ width: '80%' }}
            />
            <button onClick={sendMessage} style={{ width: '20%' }}>Send</button>
        </div>
    );
};

export default Chat;
