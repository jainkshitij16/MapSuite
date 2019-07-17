/* eslint-disable quote-props */
const express = require('express')
const bodyParser = require('body-parser')
const port = 3000

const app = express()

// parse requests of content-type -mapsuite/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }))

// parse requests of content-type -mapsuite/json
app.use(bodyParser.json())

const dbConfig = require('./config/database.js')
const mongoose = require('mongoose')

mongoose.Promise = global.Promise

mongoose.connect(dbConfig.url, {
  useNewUrlParser: true
}).then(() => {
  console.log('Successfully connected to the database')
}).catch(err => {
  console.log('Could not connect to the database, ending connection now', err)
  process.exit()
})

// defining a simple route
app.get('', (req, res) => {
  res.json({ 'Message': 'Welcome to MapSuite, we are currenly building the product for you' })
})

app.listen(port, () => {
  console.log('Server is listening on port ' + port)
})
