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
  return (
    <Container>

      <div>
        <RouteOption>
          <h3>Route 1</h3>
          <p>Duration: N/A</p>
          <p>Distance: N/A</p>
        </RouteOption>
        
        <Hr />

        <RouteOption>
          <h3>Route 2</h3>
          <p>Duration: N/A</p>
          <p>Distance: N/A</p>
        </RouteOption>
      </div>
    </Container>
  );
};

export default Directions;