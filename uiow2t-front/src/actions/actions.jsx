export const SET_CURRENT_POSITION = 'SET_CURRENT_POSITION'

export function setCurrentPosition(newPosition) {
    return {
        type: SET_CURRENT_POSITION,
        newPosition: newPosition
    };
}