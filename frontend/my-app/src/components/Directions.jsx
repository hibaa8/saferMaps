import { ContainerFilled } from '@ant-design/icons';
import React, { useState } from 'react';
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

const Button = styled.button`
  position: absolute;
  top: 10px;
  right: -80px;
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;

  &:hover {
    background-color: #0056b3;
  }
`;

const Modal = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  z-index: 200;
  width: 300px;
  text-align: center;
`;

const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 199;
`;

const Directions = ({ routeData, get_closest_camera }) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [cameraData, setCameraData] = useState(null);

  const handleButtonClick = async () => {
    const data = await get_closest_camera();
    setCameraData(data);
    setModalOpen(true);
  };

  return (
    <>
      <Container>
        {routeData.length === 2 ? (
          <div>
            <RouteOption>
              <h3>Route 1</h3>
              <p>{routeData[0].legs[0]?.duration || 'N/A'}</p>
              <p>{routeData[0].legs[0]?.distanceMeters || 'N/A'}</p>
            </RouteOption>

            <Hr />

            <RouteOption>
              <h3>Route 2</h3>
              <p>{routeData[1].legs[0]?.duration || 'N/A'}</p>
              <p>{routeData[1].legs[0]?.distanceMeters || 'N/A'}</p>
            </RouteOption>
          </div>
        ) : (
          <p>No routes found.</p>
        )}

        <Button onClick={handleButtonClick}>Show Camera</Button>
      </Container>

      {modalOpen && (
        <>
          <Overlay onClick={() => setModalOpen(false)} />
          <Modal>
            <h3>Closest Camera</h3>
            {cameraData ? (
              <>
                <p>{cameraData.description}</p>
                <img src={cameraData.url} alt="Traffic Camera" style={{ width: '100%' }} />
              </>
            ) : (
              <p>Loading...</p>
            )}
            <button onClick={() => setModalOpen(false)}>Close</button>
          </Modal>
        </>
      )}
    </>
  );
};

export default Directions;
