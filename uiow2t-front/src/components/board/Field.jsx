import React from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux';


const mapStateToProps = function (state) {
    return {
        currentPosition: state.currentPosition,
    }
}

const Frame = styled.div`
    width: 95.5px;
    height: 60px;
    background-color: rgba(0,0,255,0.7);
    margin-right: 5px;
    margin-bottom: 5px;
`
const FrameRight = styled.div`
    width: 95.5px;
    height: 60px;
    background-color: rgba(0,0,255,0.7);
    margin-bottom: 5px;
`
const FrameBottom = styled.div`
    width: 95.5px;
    height: 60px;
    background-color: rgba(0,0,255,0.7);
    margin-right: 5px;
    margin-bottom: 0px;
`
const FrameBottomRight = styled.div`
    width: 95.5px;
    height: 60px;
    background-color: rgba(0,0,255,0.7);
    margin-right: 0px;
    margin-bottom: 0px;
`

function Field({ index, children, dispatch }) {
    const setCurrentPosition = (newPosition) => dispatch({ type: 'SET_CURRENT_POSITION', newPosition })

    const isRight = (index - 9) % 10 === 0
    const isBottom = (index) >= 50
    const x = index % 10
    const y = Math.floor(index / 6)

    if (isRight && isBottom) return <FrameBottomRight onClick={() => setCurrentPosition([x, y])}>{children}</FrameBottomRight>
    else if (isRight) return <FrameRight onClick={() => setCurrentPosition([x, y])}>{children}</FrameRight>
    else if (isBottom) return <FrameBottom onClick={() => setCurrentPosition([x, y])}>{children}</FrameBottom>
    else return <Frame onClick={() => setCurrentPosition([x, y])}>{children}</Frame>
}

export default connect(mapStateToProps)(Field)