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

if (typeof p.lux !== 'undefined') {
  msgs.push({ topic: 'lux', payload: p.lux, timestamp: ts });
}

// Return multiple messages on single output
return [msgs];