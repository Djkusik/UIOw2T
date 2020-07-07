import React, { useState } from 'react'
import { Button, Form, Input, } from 'reactstrap'
import './LandingPanel.css'; // Tell webpack that Button.js uses these styles
import axios from 'axios';
import { useHistory } from 'react-router-dom';

async function joinGame(nick, evt, history) {
  evt.preventDefault()
  const response = await axios.post(`<type in your host>/add_player`, { nick })
  if (response && response.statusCode === 200) history.push('<type in room address>')
  else history.push('/')
}

function LandingPanel() {
  const [nick, setNick] = useState('')
  const history = useHistory();

  return (
    <div style={{ position: 'absolute', width: '100%', height: '100%' }}>
      <Form className="usernameForm" style={{ top: '74%' }}>

        <Input id="nickInput" placeholder="Nickname" onChange={(e) => setNick(e.target.value)} />
      </Form>
      <Button className="joinButton" color="red" onClick={evt => joinGame(nick, evt, history)}>
        <div style={{ color: 'rgba(255,255,255,0.75)' }}>Join the game</div></Button>
    </div>

  )
}
export default LandingPanel
