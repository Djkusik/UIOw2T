import React from "react";
import styled from "styled-components";

const TileBackground = styled.div`
  background-color: white;
  align-self: flex-end;
  height: 80px;
  width: 80px;
  display: inline-block;
  margin: 0px 4px 5px 4px;
`;

export default function UnitBenchTile({ unit }) {
  return unit ? (
    <TileBackground>{unit.name}</TileBackground>
  ) : (
    <TileBackground />
  );
}
