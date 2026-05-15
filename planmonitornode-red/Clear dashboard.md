// ---------- CHECK EMPTY PAYLOAD ----------
let isEmptyObject =
    typeof msg.payload === "object" &&
    !Array.isArray(msg.payload) &&
    Object.keys(msg.payload).length === 0;

let isEmptyArray =
    Array.isArray(msg.payload) &&
    msg.payload.length === 0;

if (isEmptyObject || isEmptyArray) {

    // ----- RESET MODE -----
    let normalOff = { payload: false };
    let alertOff = { payload: false };
    let alarmOff = { payload: false };
    let textClear = { payload: "" };

    return [null, normalOff, alertOff, alarmOff, textClear];
}
