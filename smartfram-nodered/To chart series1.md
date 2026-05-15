let p = msg.payload || {};
let msgs = [];

// Use timestamp from payload if possible, else now
let ts = Date.now();
if (p.timestamp) {
    let d = new Date(p.timestamp);
    if (!isNaN(d.getTime())) {
        ts = d.getTime();
    }
}

if (typeof p.temp_c !== 'undefined') {
    msgs.push({ topic: 'temp_c', payload: p.temp_c, timestamp: ts });
}
if (typeof p.humidity_pct !== 'undefined') {
    msgs.push({ topic: 'humidity_pct', payload: p.humidity_pct, timestamp: ts });
}
// if (typeof p.lux !== 'undefined') {
//   msgs.push({ topic: 'lux', payload: p.lux, timestamp: ts });
// }
if (typeof p.vpd_kpa !== 'undefined') {
    msgs.push({ topic: 'vpd_kpa', payload: p.vpd_kpa, timestamp: ts });
}

// Return multiple messages on single output
return [msgs];