let p = msg.payload || {};
let ts = p.timestamp || null;

let mHum  = (p.humidity_pct !== undefined) ? { payload: Number(p.humidity_pct), timestamp: ts } : null;

return [ mHum];