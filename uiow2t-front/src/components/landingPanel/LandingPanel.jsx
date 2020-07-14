import React, { useState, useEffect } from "react";
import { Button, Form, Input } from "reactstrap";
import "./LandingPanel.css"; // Tell webpack that Button.js uses these styles
import { useHistory } from "react-router-dom";
import socketIOClient from "socket.io-client";
import { connect } from "react-redux";

const mapStateToProps = function(state) {
  return {
    socket: state.socket
  };
};

const ENDPOINT = "http://localhost:8080";

function LandingPanel({ dispatch }) {
  const [nick, setNick] = useState("");
  const history = useHistory();
  const socket = socketIOClient(ENDPOINT);

  useEffect(() => {
    socket.on("login_reply", data => {
      console.log("LOGIN RESPONSE", data);
      if (String(data.message) === "login ok") history.push("/room");
      else console.log("error");
    });
  }, [nick, history]);

  return (
    <div style={{ position: "absolute", width: "100%", height: "100%" }}>
      <Form className="usernameForm" style={{ top: "74%" }}>
        <Input
          id="nickInput"
          placeholder="Nickname"
          onChange={e => setNick(e.target.value)}
        />
      </Form>
      <Button
        className="joinButton"
        color="red"
        onClick={evt => {
          evt.preventDefault();
          dispatch({ type: "SET_SOCKET", socket });
          socket.emit("login", { nick: nick });
        }}
      >
        <div style={{ color: "rgba(255,255,255,0.75)" }}>Join the game</div>
      </Button>
    </div>
  );
}
export default connect(mapStateToProps)(LandingPanel);
