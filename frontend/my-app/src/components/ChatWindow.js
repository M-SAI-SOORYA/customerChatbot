import React from 'react';
import MessageBubble from './MessageBubble';

const ChatWindow = ({ messages }) => {
  return (
    <div className="chat-window">
      {messages.map((msg, index) => (
        <MessageBubble key={index} sender={msg.sender} message={msg.message} />
      ))}
    </div>
  );
};

export default ChatWindow;
