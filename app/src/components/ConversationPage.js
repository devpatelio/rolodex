import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

const ConversationPage = () => {
  const [conversation, setConversation] = useState('');
  const { name, file } = useParams();

  useEffect(() => {
    fetch(`/logs/${file}`)
      .then(response => response.text())
      .then(data => setConversation(data))
      .catch(error => console.error('Error fetching conversation:', error));
  }, [file]);

  return (
    <div className="conversation-page">
      <Link to={`/profile/${name}`} className="back-link">← Back to {name}'s Profile</Link>
      <h2>Conversation</h2>
      <pre>{conversation}</pre>
    </div>
  );
};

export default ConversationPage;