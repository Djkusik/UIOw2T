import React, { useState, useEffect } from 'react'
import styled from 'styled-components'
import UnitTile from './UnitTile';
import socketIOClient from "socket.io-client";

const ENDPOINT = "http://localhost:8080";

const PanelBackground = styled.div`
  height: 10px;
  width: 10px;
  background-color: black;
  width: 1180px;
  height: 140px;
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
  justify-items:center;
  justify-content: center;
  align-items: center;
  display: flex;
  z-index: 10;
`

export default function UnitStorePanel() {
  const [currentUnits, setCurrentUnits] = useState([])
  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    socket.emit('units_from_shop')
    console.log('EMIT 1')
    socket.on('units_from_shop_reply', data => {
      console.log("units", data)
      setCurrentUnits(data)
    })
  }, [currentUnits]);

  // useEffect(() => {
  // const socket = socketIOClient(ENDPOINT);
  // socket.emit('units_from_shop')
  // console.log('EMIT 2')
  // socket.on('units_from_shop_reply', data => {
  //   console.log("units", data)
  //   this.setCurrentUnits(data)
  // })
  // }, [currentUnits]);

  return (
    <PanelBackground>
      <UnitTile />
      <UnitTile />
      <UnitTile />
      <UnitTile />
      <UnitTile />
      <UnitTile />
    </PanelBackground>

  )
}