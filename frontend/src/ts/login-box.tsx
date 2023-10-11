import React, { MouseEventHandler, SyntheticEvent } from "react";

import "../scss/login-box.scss";

import { classFromList } from "../utils";

type propsType = Readonly<{
    show: boolean,
    switchLogin: (state: boolean) => void,
}>;

export default class LoginBox extends React.Component<propsType> {
    clickBackground: (ev: React.MouseEvent<HTMLElement>) => void;
    constructor(props: propsType) {
        super(props);

        this.clickBackground = (ev) => {
            let target: HTMLElement = ev.target as HTMLElement;
            if (target.id === "login-box") {
                this.props.switchLogin(false);
            }
        };
        this.clickBackground = this.clickBackground.bind(this);
    }

    render(): React.ReactNode {
        let className = classFromList([

        ]);
        return (
            <div
                id="login-box"
                onClick={this.clickBackground}
            >
                <div className="box">

                </div>
            </div>
        );
    }
}
