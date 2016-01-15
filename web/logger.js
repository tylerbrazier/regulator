'use strict'

// Log messages and request info to stdout or stderr with a timestamp

exports.out = function(msg, req) {
  console.log(`${timestamp()}\t${msg}${reqToString(req)}`)
}

exports.err = function(msg, req) {
  console.error(`${timestamp()}\t${msg}${reqToString(req)}`)
}

function reqToString(req) {
  return req ? `\tfrom ${req.hostname} to ${req.originalUrl}` : ''
}

function timestamp() {
  let date = new Date(),
      yr = date.getFullYear(),
      mo = pad(date.getMonth()+1), // getMonth is zero indexed
      dy = pad(date.getDate()),
      hr = pad(date.getHours()),
      mi = pad(date.getMinutes()),
      se = pad(date.getSeconds())
  return `${yr}-${mo}-${dy}T${hr}:${mi}:${se}`
}

function pad(i) {
  return i < 10 ? '0'+i : i.toString()
}
