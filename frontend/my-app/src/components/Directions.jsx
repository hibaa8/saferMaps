import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  position: absolute;
  top: 30px;
  width: 420px;
  background-color: white;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 100;
`;

const Hr = styled.hr`
  border: 0;
  border-top: 1px solid #ddd;
  margin: 10px 0;
`;

const RouteOption = styled.div`
  padding: 5px;
  margin-bottom: 10px;
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 1px;

  h3 {
    font-size: 18px;
    margin: 0 0 5px 0;
  }

  p {
    font-size: 14px;
    margin: 0;
  }
`;

const Directions = ({ origin, destination }) => {
  const [routes, setRoutes] = useState([]);
  const [summaries, setSummaries] = useState([]);

  useEffect(() => {
    if (origin && destination) {
      // First, fetch the routes based on origin and destination
      fetch('http://127.0.0.1:5000/get_routes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ origin, destination }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            console.error('Backend error:', data.error);
          } else if (data.routes) {
            console.log('Routes received:', data.routes);
            // Select the first two routes
            const selectedRoutes = data.routes.slice(0, 2);
            setRoutes(selectedRoutes);

            // Now call the summarization API with the selected routes.
            // Adjust the JSON body if your API expects a specific key.
            fetch('http://127.0.0.1:5000/summarize_routes', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(selectedRoutes),
            })
              .then((res) => res.json())
              .then((summaryData) => {
                if (summaryData.error) {
                  console.error('Error summarizing routes:', summaryData.error);
                } else if (summaryData.summaries) {
                  // The returned summaries string is assumed to look like:
                  // "Here are the routes summarized in 10-word blurbs:\n\n1. Take M60-SBS bus to Broadway/W 120 St.\n2. Take M60-SBS bus to Broadway/W 120 St again.\n..."
                  // We extract only the first two summary lines.
                  const lines = summaryData.summaries
                    .split('\n')
                    .map((line) => line.trim())
                    .filter((line) => line !== '');

                  let route1Summary = '';
                  let route2Summary = '';
                  for (let i = 0; i < lines.length; i++) {
                    if (lines[i].startsWith('1.') && !route1Summary) {
                      route1Summary = lines[i];
                    } else if (lines[i].startsWith('2.') && !route2Summary) {
                      route2Summary = lines[i];
                    }
                    if (route1Summary && route2Summary) break;
                  }
                  setSummaries([route1Summary, route2Summary]);
                }
              })
              .catch((error) =>
                console.error('Error fetching summary:', error)
              );
          }
        })
        .catch((error) => console.error('Error fetching routes:', error));
    }
  }, [origin, destination]);

  return (
    <Container>
      {routes.length > 0 ? (
        <div>
          <RouteOption style={{ color: '#8B0000' }}>
            <h3>Route 1</h3>
            <p>{summaries[0] || 'Loading summary...'}</p>
            <p>Duration: {routes[0].legs[0]?.duration || 'N/A'}</p>
            <p>Distance: {routes[0].legs[0]?.distanceMeters || 'N/A'}</p>
          </RouteOption>

          <Hr />

          <RouteOption style={{ color: '#FF7F7F' }}>
            <h3>Route 2</h3>
            <p>{summaries[1] || 'Loading summary...'}</p>
            <p>Duration: {routes[1].legs[0]?.duration || 'N/A'}</p>
            <p>Distance: {routes[1].legs[0]?.distanceMeters || 'N/A'}</p>
          </RouteOption>
        </div>
      ) : (
        <p>Loading routes...</p>
      )}
    </Container>
  );
};

export default Directions;
