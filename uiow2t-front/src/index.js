import React from "react";
import reactDOM from "react-dom";

import "bootstrap/dist/css/bootstrap.min.css";
import "./index.css";
import App from "./app/App";
import * as serviceWorker from "./serviceWorker";
import { Provider } from "react-redux";
import store from "./store/store";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

reactDOM.render(
  <Provider store={store}>
    <DndProvider backend={HTML5Backend}>
      <App />
    </DndProvider>
  </Provider>,
  document.getElementById("root")
);
serviceWorker.unregister();
