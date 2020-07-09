import React from 'react'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import HomeScreen from '../screens/HomeScreen/HomeScreen'
import GameScreen from '../screens/GameScreen/GameScreen'
import './App.css'
import AwaitModal from './../components/awaitModal/AwaitModal';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact={true} path="/" component={HomeScreen} />
        <Route exact={true} path="/room" component={GameScreen} />
      </Switch>
    </Router>
  )
}

export default App
