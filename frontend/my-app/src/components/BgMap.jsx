import React from 'react';

const apiKey = import.meta.env.VITE_GOOGLE_API_KEY;

const BgMap = () => {
  return (
    <div>
        <iframe
            src={`https://www.google.com/maps/embed/v1/view?key=${apiKey}&center=40.7128,-74.0060&zoom=12&maptype=roadmap`}
            allowFullScreen
            className="map-iframe"
        ></iframe>
    </div>
  );
};

export default BgMap;