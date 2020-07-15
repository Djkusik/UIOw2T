import {
  SET_CURRENT_POSITION,
  SET_SOCKET,
  SET_OWNED_UNITS,
  SET_CURRENT_GOLD,
  UPDATE_UNITS_POSITIONS
} from "../actions/actions";
import { combineReducers } from "../../../../../Library/Caches/typescript/3.6/node_modules/redux";

const initialPosition = {
  currentPosition: []
};

const initialSocket = {
  socket: undefined
};

const initialOwnedUnits = {
  ownedUnits: []
};

const initialOwnedGold = {
  currentGold: 0
};

const initialUnitsPositions = {
  unitsPositions: []
};
export function positionReducer(state = initialPosition, action) {
  switch (action.type) {
    case SET_CURRENT_POSITION:
      return {
        ...state,
        currentPosition: action.newPosition
      };
    default:
      return state;
  }
}

export function socketReducer(state = initialSocket, action) {
  switch (action.type) {
    case SET_SOCKET:
      return {
        ...state,
        socket: action.socket
      };
    default:
      return state;
  }
}

export function ownedUnitsReducer(state = initialOwnedUnits, action) {
  switch (action.type) {
    case SET_OWNED_UNITS:
      return {
        ...state,
        ownedUnits: [...state.ownedUnits, action.unit]
      };
    default:
      return state;
  }
}

export function goldReducer(state = initialOwnedGold, action) {
  switch (action.type) {
    case SET_CURRENT_GOLD:
      return {
        ...state,
        currentGold: action.currentGold
      };
    default:
      return state;
  }
}

export function unitsPositionsReducer(state = initialUnitsPositions, action) {
  switch (action.type) {
    case UPDATE_UNITS_POSITIONS: {
      return {
        ...state,
        unitsPositions: action.unitsPositions
      };
    }
    default:
      return state;
  }
}

const combinedReducer = combineReducers({
  positionReducer: positionReducer,
  socketReducer: socketReducer,
  ownedUnitsReducer: ownedUnitsReducer,
  goldReducer: goldReducer,
  unitsPositionsReducer: unitsPositionsReducer
});

export default combinedReducer;
