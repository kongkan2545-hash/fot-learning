let p = msg.payload || {};
let label = p.y_label_pred || p.y_label || "unknown";

let normalMsg = { payload: label === "normal" };
let alertMsg  = { payload: label === "alert" };
let alarmMsg  = { payload: label === "alarm" };

return [normalMsg, alertMsg, alarmMsg];