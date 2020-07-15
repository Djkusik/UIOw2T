import React, { useState } from "react";
import styled from "styled-components";
import { useDrag, DragSource } from "react-dnd";
import { TileTypes } from "../dragTypes/TileTypes";

const BenchTileSource = {
  beginDrag(props) {
    // Return the data describing the dragged item
    const item = { unit: props.unit };
    return item;
  }
};

const TileBackground = styled.div`
  background-color: white;
  align-self: flex-end;
  height: 80px;
  width: 80px;
  display: inline-block;
  margin: 0px 4px 5px 4px;
  cursor: "move";
`;

function UnitBenchTile({ unit }) {
  const [{ isDragging }, drag] = useDrag({
    item: { type: TileTypes.BENCH_TILE },
    collect: monitor => ({
      isDragging: !!monitor.isDragging()
    })
  });
  const [unitOccupying, setUnitOccupying] = useState(unit);
  return unit ? (
    <TileBackground ref={drag}>{unit.name}</TileBackground>
  ) : (
    <TileBackground />
  );
}

export default BenchTileSource(
  TileTypes.BENCH_TILE,
  BenchTileSource
)(UnitBenchTile);
