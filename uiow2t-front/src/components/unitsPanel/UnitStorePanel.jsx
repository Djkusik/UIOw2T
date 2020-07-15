import React, { useState, useEffect } from "react";
import styled from "styled-components";
import UnitTile from "./UnitTile";
import { useSelector } from "react-redux";
import { connect } from "react-redux";
import { setCurrentGold } from "../../actions/actions";

const mapStateToProps = function(state) {
  return {
    currentGold: state.currentGold
  };
};

const PanelBackground = styled.div`
  background-color: black;
  width: 1280px;
  height: 140px;
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
  justify-items: center;
  justify-content: center;
  align-items: center;
  display: flex;
  z-index: 10;
`;

const SidePanel = styled.div`
  background-color: black;
  width: 100px;
  height: 140px;
  border-top-left-radius: 20px;
  justify-items: center;
  justify-content: center;
  align-items: center;
  display: inline-block;
  z-index: 10;
  margin-left: 7.5px;
  margin-right: 7.5px;
`;
/*
function buyUnit(dispatch, currentGold, unit) {
  if (currentGold > unit.price) {
    dispatch({ type: "SET_OWNED_UNITS", unit });
    const newGoldState = currentGold - unit.price;
    dispatch({ type: "SET_CURRENT_GOLD", newGoldState });
    setVisibile(false);
  }
}

 */

function UnitStorePanel({ dispatch }) {
  const [currentUnits, setCurrentUnits] = useState([]);
  const [currentGoldState, setCurrentGoldState] = useState(0);
  const socket = useSelector(state => state.socketReducer.socket);
  const currentGold = useSelector(state => state.goldReducer.currentGold);

  useEffect(() => {
    socket.emit("units_from_shop");
    socket.emit("get_gold");
    socket.on("units_from_shop_reply", data => {
      console.log("units ", data);
      setCurrentUnits(data);
    });
    socket.on("get_gold_reply", data => {
      console.log("gold ", data);
      dispatch({ type: "SET_CURRENT_GOLD", data });
      setCurrentGoldState(data);
    });
  }, []);

  const updateMoney = value => {
    setCurrentGoldState(value);
  };
  return (
    <>
      <PanelBackground>
        <SidePanel>
          <div
            style={{
              fontSize: "20px",
              color: "white",
              padding: "10px 0 0 10px"
            }}
          >
            {currentGoldState}
          </div>
        </SidePanel>

        {currentUnits &&
          currentUnits.map(unit => (
            <UnitTile
              update={updateMoney}
              unit={unit}
              currentGold={currentGoldState}
            />
          ))}
      </PanelBackground>
    </>
  );
}

export default connect(mapStateToProps)(UnitStorePanel);
