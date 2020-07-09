import React, { useEffect, useState } from 'react'
import styled from 'styled-components'
import AwaitModal from './../../components/awaitModal/AwaitModal';
import socketIOClient from "socket.io-client";

const ENDPOINT = "http://localhost:8080";


const Background = styled.div`
  height: 100vh;
  width: 100vw;
  background-color: red;
`

export default function GameScreen() {
    const [playersList, setPlayersList] = useState([])
    function handlePlayersWaiting(data) {
        setPlayersList(data.players_waiting)
        console.log(playersList)

    }
    useEffect(() => {
        const socket = socketIOClient(ENDPOINT);
        socket.emit('players_waiting')
        console.log('EMIT')
        socket.on('players_waiting_reply', data => {
            handlePlayersWaiting(data)
        })
    }, []);

    useEffect(() => {
        if (playersList.length) {
            console.log('update')
            console.log(playersList)
        }
    }, [playersList]);

    return (
        <Background>
            <AwaitModal playersWaiting={playersList.length} />
        </Background>

    )
}