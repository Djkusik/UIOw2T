import React, { useEffect, useState } from "react";
import styled from "styled-components";
import AwaitModal from "./../../components/awaitModal/AwaitModal";
import UnitStorePanel from "./../../components/unitsPanel/UnitStorePanel";
import UnitBenchPanel from "./../../components/unitsPanel/UnitBenchPanel";
import Board from "./../../components/board/Board";
import socketIOClient from "socket.io-client";
import { useSelector } from "react-redux";

const ENDPOINT = "http://localhost:8080";

const Background = styled.div`
  position: absolute;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  top: 0px;
  right: 0px;
  bottom: 0px;
  left: 0px;
  background-color: #91f546;
`;

export default function GameScreen() {
  const [playersList, setPlayersList] = useState([]);
  const socket = useSelector(state => state.socketReducer.socket);
  function handlePlayersWaiting(data) {
    setPlayersList(data.players_waiting);
    console.log(playersList);
  }
  useEffect(() => {
    socket.emit("players_waiting");
    console.log("EMIT");
    socket.on("players_waiting_reply", data => {
      handlePlayersWaiting(data);
    });
  }, []);

  return (
    <Background>
      <AwaitModal playersWaiting={playersList.length} />
      <div
        style={{
          alignSelf: "center",
          paddingBottom: "10%",
          justifyContent: "center",
          position: "absolute"
        }}
      >
        <Board />
      </div>
      <div style={{ alignSelf: "flex-end", justifyContent: "center" }}>
        <UnitBenchPanel />
        <UnitStorePanel socket={socket} />
      </div>
    </Background>
  );
}
