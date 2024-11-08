// File: src/App.js
import React from 'react';
import './App.css';
import Chat from './components/Chat';

function App() {
    return (
        <div className="App chat-container">
            <h1>Ask me anything</h1>
            <Chat />
        </div>
    );
}

export default App;
