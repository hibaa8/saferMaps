import React, { useEffect } from 'react';

const BgMapJS = () => {
  useEffect(() => {
    // Dynamically loading the Google Maps JavaScript API
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${import.meta.env.VITE_GOOGLE_API_KEY}&libraries=places`;
    script.async = true;
    script.defer = true;

    document.head.appendChild(script);

    // Cleanup when component is unmounted
    return () => {
      document.head.removeChild(script);
    };
  }, []);

  return (
    <div>
      <div id="google-map" style={{ height: '500px', width: '100%' }}></div>
    </div>
  );
};

export default BgMapJS;