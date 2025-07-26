import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMsg, setInputMsg] = useState('');
  const [conversationId, setConversationId] = useState(null);

  const handleSend = async () => {
    if (!inputMsg.trim()) return;

    const newUserMessage = { sender: 'user', message: inputMsg };
    setMessages([...messages, newUserMessage]);

    try {
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: inputMsg,
        conversation_id: conversationId
      });

      const aiMessage = {
        sender: 'ai',
        message: response.data.reply,
      };

      setConversationId(response.data.conversation_id); // retain session
      setMessages(prev => [...prev, aiMessage]);
      setInputMsg('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="app-container">
      <h1 className="title">Conversational AI Chat</h1>
      <ChatWindow messages={messages} />
      <div className="input-area">
        <input
          type="text"
          value={inputMsg}
          onChange={(e) => setInputMsg(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default App;
