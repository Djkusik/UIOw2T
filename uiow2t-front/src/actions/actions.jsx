export const SET_CURRENT_POSITION = 'SET_CURRENT_POSITION'

export function setCurrentPosition(newPosition) {
    return {
        type: SET_CURRENT_POSITION,
        newPosition: newPosition
    };
}

export const SET_SOCKET = 'SET_SOCKET'

export function setSocket(newSocket) {
    return {
        type: SET_SOCKET,
        socket: newSocket
    }
}

export const SET_OWNED_UNITS = 'SET_OWNED_UNITS'

export function setOwnedUnits(newUnit) {
    return {
        type: SET_OWNED_UNITS,
        unit: newUnit
    }
}

export const SET_CURRENT_GOLD = 'SET_CURRENT_GOLD'

export function setCurrentGold(newGold) {
    return {
        type: SET_CURRENT_GOLD,
        gold: newGold
    }
}