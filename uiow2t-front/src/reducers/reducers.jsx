import { SET_CURRENT_POSITION } from '../actions/actions'

const initialPosition = {
    currentPosition: []
}

function positionReducer(state = initialPosition, action) {
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
export default positionReducer;