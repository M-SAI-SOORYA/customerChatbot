import React from 'react';

const MessageBubble = ({ sender, message }) => {
  const isUser = sender === 'user';
  return (
    <div className={`message-bubble ${isUser ? 'user' : 'ai'}`}>
      <p>{message}</p>
    </div>
  );
};

export default MessageBubble;
