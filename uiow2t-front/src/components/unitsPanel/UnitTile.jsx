import React, { useState } from "react";
import styled from "styled-components";
import { connect } from "react-redux";
import { useSelector } from "react-redux";

const TileBackground = styled.div`
  background-color: white;
  align-self: flex-end;
  height: 115px;
  width: 180px;
  display: inline-block;
  margin: 10px 7.5px 15px 7.5px;
  justify-content: center;
  align-items: center;
`;

const TileText = styled.p`
  margin-left: 10px;
`;

const mapStateToProps = function(state) {
  return {
    ownedUnits: state.ownedUnits
  };
};

function buyUnit(dispatch, currentGold, unit, visible, setVisibile) {
  if (visible && currentGold > unit.price) {
    dispatch({ type: "SET_OWNED_UNITS", unit });
    const newGoldState = currentGold - unit.price;
    dispatch({ type: "SET_CURRENT_GOLD", newGoldState });
    setVisibile(false);
  }
}

function UnitTile({ unit, dispatch }) {
  const [visible, setVisibile] = useState(true);
  const currentGold = useSelector(state => state.goldReducer.currentGold);

  return (
    <TileBackground
      onClick={e => {
        e.preventDefault;
        buyUnit(dispatch, currentGold, unit, visible, setVisibile);
      }}
    >
      <TileText>{visible && unit.name}</TileText>
      <TileText>{visible && unit.price}</TileText>
    </TileBackground>
  );
}
export default connect(mapStateToProps)(UnitTile);
