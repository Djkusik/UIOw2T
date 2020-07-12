import { createStore } from 'redux';
import positionReducer from './../reducers/reducers';
const store = createStore(positionReducer);
export default store;