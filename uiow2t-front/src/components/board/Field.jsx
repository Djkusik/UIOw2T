import React from "react";
import styled from "styled-components";
import { connect, useSelector } from "react-redux";
import { TileTypes } from "../dragTypes/TileTypes";
import { useDrop } from "react-dnd";
import store from "../../store/store";

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

function Field({ index, children, dispatch, setCurrentPositions }) {
  const [{ isOver }, drop] = useDrop({
    accept: TileTypes.BENCH_TILE,
    drop: (props, monitor) => {
      console.log("DROPPED ", monitor.getItem().unit);
      setCurrentPosition([x, y], monitor.getItem().unit);
      console.log("OWNED ", ownedUnits);
      let results = ownedUnits;
      for (let i = 0; i < results.length; i++) {
        if (results[i].id === monitor.getItem().unit.id) {
          results.splice(i, 1);
          console.log("OWNED ", results);
          dispatch({ type: "SET_OWNED_UNITS", units: results });
        }
      }
      return monitor.getItem();
    },
    collect: monitor => ({
      isOver: !!monitor.isOver()
    })
  });

  const unitsPositions = useSelector(
    state => state.unitsPositionsReducer.unitsPositions
  );

  const ownedUnits = useSelector(state => state.ownedUnitsReducer.ownedUnits);

  const removeUnit = () => {
    const result = unitsPositions;
    if (
      result &&
      result[index] &&
      result[index].unit &&
      result[index].unit.id === unitsPositions[index].unit.id
    ) {
      dispatch({ type: "SET_OWNED_UNIT", unit: result[index].unit });
      result[index] = {};
      dispatch({ type: "UPDATE_UNITS_POSITIONS", unitsPositions: result });
      setCurrentPositions(result);
    }
  };

  const setCurrentPosition = (newPosition, unit) => {
    const result = unitsPositions;
    if (!result[index]) result[index] = { position: newPosition, unit: unit };
    setCurrentPositions(result);
    dispatch({ type: "UPDATE_UNITS_POSITIONS", unitsPositions: result });
  };

  const isRight = (index - 9) % 10 === 0;
  const isBottom = index >= 50;
  const x = index % 10;
  const y = Math.floor(index / 6);

  if (isRight && isBottom)
    return (
      <FrameBottomRight ref={drop} onClick={removeUnit()}>
        {children}
      </FrameBottomRight>
    );
  else if (isRight)
    return (
      <FrameRight ref={drop} onClick={removeUnit()}>
        {children}
      </FrameRight>
    );
  else if (isBottom)
    return (
      <FrameBottom ref={drop} onClick={removeUnit()}>
        {children}
      </FrameBottom>
    );
  else
    return (
      <Frame ref={drop} onClick={removeUnit()}>
        {children}
      </Frame>
    );
}

export default connect(mapStateToProps)(Field);
