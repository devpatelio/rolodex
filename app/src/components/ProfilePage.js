import React from 'react';
import { useParams, Link } from 'react-router-dom';

const ProfilePage = ({ profiles }) => {
    const { name } = useParams();
    const profile = profiles.find(p => p.name === name);

    if (!profile) {
        return <div>Profile not found</div>;
    }

    return (
        <div className="profile-page">
            <Link to="/" className="back-link">← Back</Link>
            <div className="profile-content">
                <img src={profile.image} alt={profile.name} className="profile-large-image" />
                <div className="profile-details">
                    <h2>{profile.name}</h2>
                    <p><strong>Relationship:</strong> {profile.relationship}</p>
                    <p><strong>Likes:</strong> {profile.likes}</p>
                    {profile.logs && (
                        <div className="conversation-logs">
                            {profile.logs.map((log, index) => (
                                <div key={index} className="log-button">
                                    <Link to={`/conversation/${profile.name}/${log.file}`}>
                                        Conversation from {log.date}
                                    </Link>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;