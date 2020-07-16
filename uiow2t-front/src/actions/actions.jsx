export const SET_CURRENT_POSITION = "SET_CURRENT_POSITION";

export function setCurrentPosition(newPosition) {
  return {
    type: SET_CURRENT_POSITION,
    newPosition: newPosition
  };
}

export const SET_SOCKET = "SET_SOCKET";

export function setSocket(newSocket) {
  return {
    type: SET_SOCKET,
    socket: newSocket
  };
}

export const SET_OWNED_UNIT = "SET_OWNED_UNIT";

export function setOwnedUnit(newUnit) {
  return {
    type: SET_OWNED_UNIT,
    unit: newUnit
  };
}

export const SET_OWNED_UNITS = "SET_OWNED_UNITS";

export function setOwnedUnits(units) {
  return {
    type: SET_OWNED_UNITS,
    units: units
  };
}

export const SET_CURRENT_GOLD = "SET_CURRENT_GOLD";

export function setCurrentGold(newGold) {
  return {
    type: SET_CURRENT_GOLD,
    gold: newGold
  };
}

export const UPDATE_UNITS_POSITIONS = "UPDATE_UNITS_POSITIONS";

export function setUnitsPositions(newPositions) {
  return {
    type: UPDATE_UNITS_POSITIONS,
    unitsPositions: newPositions
  };
}
