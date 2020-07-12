import React, { useState, useEffect } from 'react'
import styled from 'styled-components'
import UnitBenchTile from './UnitBenchTile';
import socketIOClient from "socket.io-client";

const ENDPOINT = "http://localhost:8080";

const PanelBackground = styled.div`
  height: 10px;
  width: 10px;
  align-self: flex-end;
  justify-self: center;
  margin-right: 0;
  width: 695px;
  height: 95px;
  justify-items:center;
  justify-content: center;
  align-items: center;
  display: flex;
  z-index: 10;
`

export default function UnitBenchPanel() {
    // const [currentUnits, setCurrentUnits] = useState([])
    // useEffect(() => {
    //     const socket = socketIOClient(ENDPOINT);
    //     socket.emit('players_waiting')
    //     console.log('EMIT')uNIT
    //     socket.on('players_waiting_reply', data => {
    //         handlePlayersWaiting(data)
    //     })
    // }, []);

    // useEffect(() => {
    //     if (playersList.length) {
    //         console.log('update')
    //         console.log(playersList)
    //     }
    // }, [playersList]);


    return (
        <div style={{ display: 'flex', justifyContent: 'center' }}>
            <PanelBackground>
                <UnitBenchTile />
                <UnitBenchTile />
                <UnitBenchTile />
                <UnitBenchTile />
                <UnitBenchTile />
                <UnitBenchTile />
                <UnitBenchTile />
                <UnitBenchTile />
            </PanelBackground>
        </div >
    )
}