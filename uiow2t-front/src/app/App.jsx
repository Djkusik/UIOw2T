import React from 'react'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import HomeScreen from '../screens/HomeScreen/HomeScreen'
import './App.css'

function App() {
  return (
    <Router>
      <Switch>
        <Route exact={true} path="/" component={HomeScreen} />
      </Switch>
    </Router>
  )
}

export default App
