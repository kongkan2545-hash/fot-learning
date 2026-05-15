let p = msg.payload || {};
let ts = p.timestamp || null;
let mVPD  = (p.vpd_kpa !== undefined) ? { payload: Number(p.vpd_kpa), timestamp: ts } : null;

return [mVPD];