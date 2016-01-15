#!/usr/bin/env node
'use strict'

// Host a little web server that can be queried for statistics of the
// temperature log for any given period and generate plots using plot.ly.

const usage = 'Usage: node index.js log plotly-username plotly-api-key'

if (process.argv.length !== 5) {
  console.error(usage)
  process.exit(1)
}

const log = process.argv[2]
const plotlyUser = process.argv[3]
const plotlyKey = process.argv[4]

const express = require('express')
const serveIndex = require('serve-index')
const logger = require('./logger')
const stats = require('./stats')
const plotly = require('./plotly')
const logReader = require('./log-reader')
const app = express()
const port = 8080
const logsDir = __dirname+'/../logs'

app.set('views', __dirname+'/views')
app.set('view engine', 'ejs')

app.use( (req, res, next) => {
  logger.out(req.method, req)
  next()
})

app.use('/logs', serveIndex(logsDir, {view: 'details'}))
app.use('/logs', express.static(logsDir))

app.get('/stats', (req, res, next) => {
  logReader.read(log, req.query.period, (err, x, y) => {
    if (err)
      return next(err)

    let s = stats(y)
    let data = {
      start: x[0],
      end: x.slice(-1).pop(),
      min: s.min,
      max: s.max,
      average: s.average,
      points: x.length,
      plot: null,
    }

    if (req.query.plot === 'true')
      plotly.plot(plotlyUser, plotlyKey, x, y, (err, json) => {
        if (err)
          return next(err)
        else if (json.error)
          return next(new Error(json.error))
        else {
          data.plot = json.url
          res.render('stats', data)
        }
      })
    else
      res.render('stats', data)
  })
})

// log and render errors
app.use( (err, req, res, next) => {
  logger.err(err.message, req)
  res.render('error', {message: err.message})
})

app.listen(port, () => logger.out(`Listening on ${port}`) )

