import './App.css';
import React, { useState } from 'react';
import BgMap from './components/BgMap';
import SearchBar from './components/SearchBar';
import Directions from './components/Directions';
import logo from './assets/logo.png';

function App() {

  const [origin, setOrigin] = useState(null);

  // Called when a user selects a place in the fixed SearchBar
  const handleOriginSelect = (place) => {
    setOrigin(place);
  };

  return (
    <div>
      {/* Fixed SearchBar for the origin */}
      <SearchBar fixed={true} onPlaceSelected={handleOriginSelect} />

      {/* Render Directions only if an origin has been selected */}
      {origin && <Directions origin={origin} />}

      {/* Background map component can use the selected origin */}
      <BgMap location={origin} />
      
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