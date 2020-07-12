import React from 'react'
import reactDOM from 'react-dom'

import 'bootstrap/dist/css/bootstrap.min.css'
import './index.css'
import App from './app/App'
import * as serviceWorker from './serviceWorker'
import {
    Provider
} from 'react-redux'
import store from './store/store';

reactDOM.render(<
    Provider store={
        store
    } >
    <App />
</Provider>, document.getElementById('root'))
serviceWorker.unregister()