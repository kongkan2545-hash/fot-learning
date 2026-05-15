let p = msg.payload || {};
let ts = p.timestamp || null;

let mLux  = (p.lux !== undefined) ? { payload: Number(p.lux), timestamp: ts } : null;

return [mLux];