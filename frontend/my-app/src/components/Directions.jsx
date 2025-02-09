import { ContainerFilled } from '@ant-design/icons';
import React from 'react';
import styled from 'styled-components';
import SearchBar from './SearchBar';

const Container = styled.div`
    position: absolute;
    top: 30px;
    width: 420px;
    background-color: white;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 100;
`;

const Destination = styled.div`
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    font-size: 16px;
    color: #333;
`;

const Hr = styled.hr`
  border: 0;
  border-top: 1px solid #ddd;
  margin: 10px 0;
`;

const RouteOption = styled.div`
  padding: 5px;
  margin-bottom: 10px; 
  color: #333;
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

const formatDuration = (duration) => {
  if (!duration) return 'N/A';
  const seconds = parseInt(duration.replace('s', ''), 10);
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes} min ${remainingSeconds} sec`;
};

const formatDistance = (distanceMeters) => {
  if (!distanceMeters) return 'N/A';
  return `${(distanceMeters / 1000).toFixed(1)} km`;
};

const Directions = ({ routeData }) => {
  return (
    <Container>
      {routeData.length === 2 ? (
        <div>
          <RouteOption>
            <h3>Route 1</h3>
            <p>{`${formatDuration(routeData[0].legs[0]?.duration)}`}</p>
            <p>{`${formatDistance(routeData[0].legs[0]?.distanceMeters)}`}</p>
          </RouteOption>
          
          <Hr />

          <RouteOption>
            <h3>Route 2</h3>
            <p>{`${formatDuration(routeData[1].legs[0]?.duration)}`}</p>
            <p>{`${formatDistance(routeData[1].legs[0]?.distanceMeters)}`}</p>
          </RouteOption>
        </div>
      ) : (
        <p>No routes found.</p>
      )}
    </Container>
  );
};

export default Directions;