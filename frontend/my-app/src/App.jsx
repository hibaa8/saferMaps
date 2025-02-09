import './App.css';
import React, { useState } from 'react';
import BgMap from './components/BgMap';
import SearchBar from './components/SearchBar';
import Directions from './components/Directions';
import logo from './assets/logo.png';
import BgMapJS from './components/BgMapJS';

function App() {

  const [location, setLocation] = useState(null);

  return (
    <div>
      <Directions />
      <BgMap />
      <SearchBar />
      
      <img
        src={logo}  // Use the path of the image
        alt="Top Right Logo"
        style={{
          position: 'absolute',
          top: '20px',
          right: '20px',
          width: '200px',
          height: 'auto',
        }}
      />

    </div>
  )
}

export default App;