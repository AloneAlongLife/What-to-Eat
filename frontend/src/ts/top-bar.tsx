import React from "react";

import "../scss/top-bar.scss";

import { rem2Pixel, classFromList } from "../utils";

type propsType = Readonly<{}>;
type stateType = Readonly<{
    transparent: boolean
}>;

export default class TopBar extends React.Component {
    state: stateType;
    onScroll: () => void;
    constructor(props: propsType) {
        super(props);
        this.state = {
            transparent: false,
        };

        this.onScroll = (): void => {
            let transparent = window.scrollY > rem2Pixel(4);
            if (transparent !== this.state.transparent) {
                this.setState({
                    transparent: transparent,
                });
            }
        };
        this.onScroll = this.onScroll.bind(this);
    }

    componentDidMount(): void {
        document.addEventListener("scroll", this.onScroll);
    }

    componentWillUnmount(): void {
        document.removeEventListener("scroll", this.onScroll);
    }

    render(): React.ReactNode {
        let className: string = classFromList([
            this.state.transparent ? "transparent" : null,
        ]);
        return (
            <div id="top-bar" className={className}>

            </div>
        );
    }
}
