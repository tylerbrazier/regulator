'use strict'

// Parses the given log file, and builds up arrays x and y which are timestamps
// and degrees (in celsius) respectively, starting at a point that is <period>
// from now (e.g. 1h ago. see period-parser.js).

const fs = require('fs')
const readline = require('readline')
const periodParser = require('./period-parser')

// callback(err, x, y)
exports.read = (log, period, callback) => {
  let x=[], y=[], now=Date.now(), split, date, within, err

  let readstream = fs.createReadStream(log, {encoding:'utf8'})
  let reader = readline.createInterface({ input: readstream })

  readstream.on('error', e => callback(err = e))

  reader.on('line', line => {
    if (err)
      return // no sense in continuing

    // line has the format: timestamp[tab]degrees_c[tab]degrees_f
    split = line.split('\t')
    date = new Date(split[0])
    date.setMinutes(date.getMinutes() + date.getTimezoneOffset())

    if (isNaN(date))
      return err = new Error(`Error parsing date from ${log}`)

    try {
      within = within || periodParser.isWithin(date, now, period)
    } catch (e) {
      return err = e
    }

    if (within) {
      // http://help.plot.ly/date-format-and-time-series/
      x.push(split[0].replace(/T/, ' '))
      y.push(split[1])
    }
  })

  reader.on('close', () => {
    if (err)
      callback(err)
    else if (y.length == 0)
      callback(new Error(`No data for period ${period || periodParser.DEFAULT}`))
    else
      callback(null, x, y)
  })

}
