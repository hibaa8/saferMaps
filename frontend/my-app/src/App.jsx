import './App.css';
import React, { useState } from 'react';
import BgMap from './components/BgMap';
import SearchBar from './components/SearchBar';
import Directions from './components/Directions';

function App() {

  const [location, setLocation] = useState(null);

  return (
    <div>
      <Directions />
      <BgMap location={location}/>
      <SearchBar />
      
    </div>
  )
}

export default App;