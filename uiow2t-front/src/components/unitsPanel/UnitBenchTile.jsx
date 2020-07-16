import React from "react";
import styled from "styled-components";
import { useDrag, DragSource } from "react-dnd";
import { TileTypes } from "../dragTypes/TileTypes";
function collect(connect, monitor) {
  return {
    // Call this function inside render()
    // to let React DnD handle the drag events:
    connectDragSource: connect.dragSource(),
    // You can ask the monitor about the current drag state:
    isDragging: monitor.isDragging()
  };
}
const BenchTileSource = {
  beginDrag(props) {
    // Return the data describing the dragged item
    return {
      unit: props.unit
    };
  },
  endDrag(props, monitor) {
    console.log("KILL ME ", monitor.getItem());
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
    item: { type: TileTypes.BENCH_TILE, unit: unit },
    collect: monitor => ({
      isDragging: !!monitor.isDragging()
    })
  });

  return unit ? (
    <TileBackground ref={drag}>{unit.name}</TileBackground>
  ) : (
    <TileBackground />
  );
}
export default DragSource(
  TileTypes.BENCH_TILE,
  BenchTileSource,
  collect
)(UnitBenchTile);
