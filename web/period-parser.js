'use strict'

// Check if two dates are within a particular period of eachother.
// Periods can be like 2m (2 minutes), 74d (74 days), etc.

const DEFAULT = '1d'
const MILLIES = {
  m: 1000 * 60,               // minute
  h: 1000 * 60 * 60,          // hour
  d: 1000 * 60 * 60 * 24,     // day
  w: 1000 * 60 * 60 * 24 * 7, // week
}

exports.DEFAULT = DEFAULT

exports.isWithin = function(start, end, period) {
  let p = toMillis(period)
  return end - start <= p
}

function toMillis(period) {
  let p = period || DEFAULT
  let n = Number(p.slice(0, p.length-1)) // all but the last character
  let m = p.slice(-1)                    // the last character
  if (!n || n < 0 || !MILLIES[m])
    throw new Error('Invalid period')
  else
    return n * MILLIES[m]
}
