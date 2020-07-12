import React, { useState, useEffect } from 'react'
import styled from 'styled-components'
import CharacterIndicator from './CharacterIndicator';
import Field from './Field';
import { useSelector } from 'react-redux'

const ENDPOINT = "http://localhost:8080";

const BoardBackground = styled.div`
  height: 385px;
  width: 1000px;
  align-self: flex-end;
  margin-right: 0;
  display: flex;
  bottom: 50px;
  flex-wrap: wrap;
`
function renderSquare(i, currentPosition) {
    const x = i % 10
    const y = Math.floor(i / 6)
    if (currentPosition) {
        const isKnightHere = currentPosition[0] === x && currentPosition[1] === y
        const piece = isKnightHere ? <CharacterIndicator /> : null
        return <Field key={i} index={i}>{piece}</Field>
    }
    else return <Field key={i} index={i}></Field>
}


export default function Board({ positionOccupied }) {
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
    const currentPosition = useSelector(state => state.currentPosition)

    const fields = []
    for (let i = 0; i < 60; i++) {
        fields.push(renderSquare(i, currentPosition))
    }
    return (
        // <div style={{ display: 'flex', justifyContent: 'center' }}>
        <BoardBackground>
            {fields}
        </BoardBackground>
        // </div >
    )
}