import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';
import ProfilePage from './components/ProfilePage';
import ConversationPage from './components/ConversationPage';

const profiles = [
  {
    name: 'Dev Patel',
    image: '/images/dev_patel.png',
    relationship: 'Friend',
    likes: 'Long walks on the beach, startups, eating chocolate cake and strawberries',
    logs: [
      { date: 'August 3, 3:17pm', file: 'pg1.txt' },
      { date: 'August 1, 9:40pm', file: 'pg2.txt' }
    ]
  },
  {
    name: 'Richa Pandya',
    image: '/images/richa_pandya.png',
    relationship: 'Friend',
    likes: 'Wearables, Taco Bell, ordering things from Amazon'
  },
  {
    name: 'Bobak Tavangar',
    image: '/images/bobak_tavangar.jpg',
    relationship: 'Colleague',
    likes: 'Innovative projects, space exploration, reading science fiction'
  },
  {
    name: 'Raj Nakarja',
    image: '/images/raj_nakarja.jpg',
    relationship: 'Father',
    likes: 'Yoga, meditation, healthy cooking, traveling to exotic places'
  },
  {
    name: 'Ben Heald',
    image: '/images/ben_heald.jpg',
    relationship: 'Business Partner',
    likes: 'Strategic planning, outdoor adventures, craft beer tasting'
  },
];

function ProfileBox({ name, image, isPink }) {
  return (
    <div className={`profile-box ${isPink ? 'pink' : 'green'}`}>
      {image && <img src={image} alt={name} className="profile-image" />}
      <span>{name}</span>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="container">
        <header>
          <h1>ROLODEX</h1>
          <div className="header-line"></div>
        </header>
        <Routes>
          <Route path="/" element={
            <>
              <h2>My Profiles</h2>
              <div className="profiles-grid">
                <div className="pink-boxes">
                  <ProfileBox name="Add New Profile" isPink={true} />
                  <ProfileBox name="Unnamed Profiles" isPink={true} />
                </div>
                {profiles.map((profile, index) => (
                  <Link key={index} to={`/profile/${profile.name}`} className="profile-link">
                    <ProfileBox name={profile.name} image={profile.image} isPink={false} />
                  </Link>
                ))}
              </div>
            </>
          } />
          <Route path="/profile/:name" element={<ProfilePage profiles={profiles} />} />
          <Route path="/conversation/:name/:file" element={<ConversationPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;