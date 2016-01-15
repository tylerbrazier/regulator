'use strict'

// Make an api call to plot.ly to generate a plot with with data points from
// arrays x and y. The callback will be passed the json response from plot.ly.

const https = require('https')
const querystring = require('querystring')

// x and y are arrays, callback(err, json)
exports.plot = (user, apiKey, x, y, callback) => {
  let body = ''
  const postData = querystring.stringify({
    un: user,
    key: apiKey,
    platform: 'node',
    origin: 'plot',
    args: JSON.stringify([x, y]),
    kwargs: JSON.stringify({
      filename: 'temperature',
      fileopt: 'overwrite',
      style: { type: 'line' },
      layout: { title: 'Temperature' },
      world_readable: true
    })
  })

  https.request({
    host: 'plot.ly',
    port: 443,
    method: 'POST',
    path: '/clientresp',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    }
  }, res => {
    if (res.statusCode !== 200)
      return callback(new Error(`Got ${res.statusCode} from plot.ly`))
    res.on('error', callback)
    res.on('data', chunk => body += chunk )
    res.on('end', () => callback(null, JSON.parse(body)))
  }).end(postData)
}

