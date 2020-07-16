import React, { useState, useEffect } from "react";
import styled from "styled-components";
import CharacterIndicator from "./CharacterIndicator";
import Field from "./Field";
import { useSelector } from "react-redux";

const ENDPOINT = "http://localhost:8080";

const BoardBackground = styled.div`
  height: 385px;
  width: 1000px;
  align-self: flex-end;
  margin-right: 0;
  display: flex;
  bottom: 50px;
  flex-wrap: wrap;
`;
function renderSquare(i, unit, setCurrentPositions) {
  const x = i % 10;
  const y = Math.floor(i / 6);
  if (unit) {
    const piece = <CharacterIndicator />;
    return (
      <Field key={i} index={i} setCurrentPositions={setCurrentPositions}>
        {unit.name}
      </Field>
    );
  } else
    return (
      <Field
        key={i}
        index={i}
        setCurrentPositions={setCurrentPositions}
      ></Field>
    );
}

export default function Board() {
  // const currentPosition = useSelector(
  //   state => state.positionReducer.currentPosition
  // );
  const [currentPositions, setCurrentPositions] = useState([]);
  const fields = [];
  for (let i = 0; i < 60; i++) {
    const unit = currentPositions[i];
    fields.push(renderSquare(i, unit, setCurrentPositions));
  }
  return <BoardBackground>{fields}</BoardBackground>;
}
