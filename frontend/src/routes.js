import React from "react";
import { Route } from "react-router-dom";
import Hoc from './hoc/hoc';
import Chat from "./containers/Chat";
import Sidepanel from "./containers/Sidepanel";
import MainCompo from "./containers/MainCompo";
const BaseRouter = () => (
  <Hoc>
    <Route exact path="/:chatID/" component={Chat} />
    {/* <Route exact path="/:chatID/" component={Sidepanel} /> */}
  </Hoc>
);

export default BaseRouter;
