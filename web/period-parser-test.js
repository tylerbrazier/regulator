#!/usr/bin/env node
'use strict'

const parser = require('./period-parser')
const assert = require('assert')

let m = 1000 * 60,
    h = 1000 * 60 * 60,
    d = 1000 * 60 * 60 * 24,
    w = 1000 * 60 * 60 * 24 * 7,
    start, end

start = new Date(0)
end = new Date(70*m)
assert(!parser.isWithin(start, end, '10m'))
assert(!parser.isWithin(start, end, '69.9m'))
assert(parser.isWithin(start, end, '70m'))
assert(parser.isWithin(start, end, '71m'))
assert(!parser.isWithin(start, end, '1h'))
assert(parser.isWithin(start, end, '2h'))

end = new Date(1.5*h)
assert(parser.isWithin(start, end, '1.5h'))
assert(parser.isWithin(start, end, '2h'))
assert(!parser.isWithin(start, end, '1.4h'))
assert(parser.isWithin(start, end, '90m'))
assert(!parser.isWithin(start, end, '89m'))
assert(parser.isWithin(start, end, '1d'))
assert(parser.isWithin(start, end, '1w'))

end = new Date(2*d)
assert(!parser.isWithin(start, end, '1d'))
assert(parser.isWithin(start, end, '2d'))
assert(parser.isWithin(start, end, '48h'))
assert(!parser.isWithin(start, end, '47h'))
assert(parser.isWithin(start, end, '1w'))

end = new Date(1*w).getTime()
assert(!parser.isWithin(start, end, '1d'))
assert(!parser.isWithin(start, end, '6.9d'))
assert(parser.isWithin(start, end, '7d'))
assert(parser.isWithin(start, end, '8d'))

// test default period of 1d
end = new Date(1*d).getTime()
assert(parser.isWithin(start, end, undefined))
end = new Date(23*h).getTime()
assert(parser.isWithin(start, end, undefined))
end = new Date(25*h).getTime()
assert(!parser.isWithin(start, end, undefined))

// failure cases
assert.throws(() => parser.isWithin(start, end, '10'))
assert.throws(() => parser.isWithin(start, end, 'd'))
assert.throws(() => parser.isWithin(start, end, 'w8'))
assert.throws(() => parser.isWithin(start, end, '3hm'))
assert.throws(() => parser.isWithin(start, end, '0'))
assert.throws(() => parser.isWithin(start, end, '-1'))
assert.throws(() => parser.isWithin(start, end, '-24w'))
