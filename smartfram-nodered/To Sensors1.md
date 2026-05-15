let p = msg.payload || {};
let ts = p.timestamp || null;

let mTemp = (p.temp_c !== undefined) ? { payload: Number(p.temp_c), timestamp: ts } : null;

return [mTemp];