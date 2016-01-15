'use strict'

// Given data that is an array of numbers or stringy numbers
// (e.g. ['3','0.3',-5]) return an object with min, max and average of the data

module.exports = (data) => {
  let min, max, total=0

  data.forEach(d => {
    d = Number(d)
    min = (min === undefined) ? d : (d < min) ? d : min
    max = (max === undefined) ? d : (d > max) ? d : max
    total += d
  })

  return {
    min, max, average: (data.length > 0) ? total/data.length : undefined
  }
}
