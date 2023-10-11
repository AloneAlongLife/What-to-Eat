export function rem2Pixel(rem: number): number {
    return rem * parseFloat(getComputedStyle(document.documentElement).fontSize);
}

export function classFromList(classes: Array<string|null>): string {
    return classes.filter(x => typeof x === "string").join(" ");
}
