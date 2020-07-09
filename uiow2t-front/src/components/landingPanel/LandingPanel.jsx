import React, { useState, useEffect } from 'react'
import { Button, Form, Input, } from 'reactstrap'
import './LandingPanel.css'; // Tell webpack that Button.js uses these styles
import { useHistory } from 'react-router-dom';
import socketIOClient from "socket.io-client";

const ENDPOINT = "http://localhost:8080";

function LandingPanel() {
  const [nick, setNick] = useState('')
  const [response, setResponse] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const history = useHistory();

  // useEffect(() => {
  //   const socket = socketIOClient(ENDPOINT);
  //   socket.on("login_reply", data => {
  //     setResponse(data);
  //     console.log("LOGIN RESPONSE", data)
  //   });
  // }, []);

  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    if (submitted) {
      socket.emit('login', { 'nick': nick })
    }
    socket.on("login_reply", data => {
      setResponse(data);
      console.log("LOGIN RESPONSE", data)
      if (String(data.message) === 'login ok') history.push('/room')
      else console.log('error')
    });
  }, [submitted, nick, history]);


  return (
    <div style={{ position: 'absolute', width: '100%', height: '100%' }}>
      <Form className="usernameForm" style={{ top: '74%' }}>

        <Input id="nickInput" placeholder="Nickname" onChange={(e) => setNick(e.target.value)} />
      </Form>
      <Button className="joinButton" color="red" onClick={evt => {
        evt.preventDefault()
        setSubmitted(true)
      }}>
        <div style={{ color: 'rgba(255,255,255,0.75)' }}>Join the game</div></Button>
    </div>

  )
}
export default LandingPanel
