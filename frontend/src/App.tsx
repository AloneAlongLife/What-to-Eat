import React from "react";

import "./App.scss"

import LoginBox from "./ts/login-box";
import TopBar from "./ts/top-bar";

type propsType = Readonly<{}>;
type stateType = Readonly<{
  showLogin: boolean
}>;

export default class App extends React.Component<propsType> {
  state: stateType;
  switchLogin: (state: boolean) => void;
  constructor(props: propsType) {
    super(props);

    this.state = {
      showLogin: true,
    };

    this.switchLogin = (state) => {
      this.setState({
        showLogin: state,
      });
    };
    this.switchLogin = this.switchLogin.bind(this);
  }

  render(): React.ReactNode {
    return (
      <div id="app">
        <LoginBox
          show={this.state.showLogin}
          switchLogin={this.switchLogin}
        />
        <TopBar />
      </div>
    )
  }
}
