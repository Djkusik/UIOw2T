import React from "react";
import styled from "styled-components";
import { connect } from "react-redux";
import { TileTypes } from "../dragTypes/TileTypes";
import { useDrop } from "react-dnd";

const mapStateToProps = function(state) {
  return {
    currentPosition: state.currentPosition,
    unitsPositions: state.unitsPositions
  };
};

const Frame = styled.div`
  width: 95.5px;
  height: 60px;
  background-color: rgba(0, 0, 255, 0.7);
  margin-right: 5px;
  margin-bottom: 5px;
`;
const FrameRight = styled.div`
  width: 95.5px;
  height: 60px;
  background-color: rgba(0, 0, 255, 0.7);
  margin-bottom: 5px;
`;
const FrameBottom = styled.div`
  width: 95.5px;
  height: 60px;
  background-color: rgba(0, 0, 255, 0.7);
  margin-right: 5px;
  margin-bottom: 0px;
`;
const FrameBottomRight = styled.div`
  width: 95.5px;
  height: 60px;
  background-color: rgba(0, 0, 255, 0.7);
  margin-right: 0px;
  margin-bottom: 0px;
`;

function Field({ index, children, dispatch }) {
  const unitsPositions = useSelector(
    state => state.unitsPositionsReducer.unitsPositions
  );

  const [{ isOver }, drop] = useDrop({
    accept: TileTypes.BENCH_TILE,
    drop: monitor => setCurrentPosition([x, y], monitor.getItem()),
    collect: monitor => ({
      isOver: !!monitor.isOver()
      item: monitor.item
    })
  });

  const setCurrentPosition = (newPosition, unit) => {
    if (!unitsPositions[index].unit) {
      const result = unitsPositions;
      result[index] = { position: newPosition, unit: unit };
      dispatch({ type: "UPDATE_UNITS_POSITIONS", result });
    }
  };

  const isRight = (index - 9) % 10 === 0;
  const isBottom = index >= 50;
  const x = index % 10;
  const y = Math.floor(index / 6);

  if (isRight && isBottom)
    return <FrameBottomRight ref={drop}>{children}</FrameBottomRight>;
  else if (isRight) return <FrameRight ref={drop}>{children}</FrameRight>;
  else if (isBottom) return <FrameBottom ref={drop}>{children}</FrameBottom>;
  else return <Frame ref={drop}>{children}</Frame>;
}

export default connect(mapStateToProps)(Field);
