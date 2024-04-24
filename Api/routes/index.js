let express = require('express')
let router = express.Router()
const {where} = require("sequelize")
const seq = require('../dbmodels')

router.get('/', async (req, res, next) => {
  console.log(req.query)
  let data = {}
  if (seq.hasOwnProperty(req.query.table)) {
    try {
      let table = req.query.table
      delete req.query.table
      data = await seq[table].findAll({
        where: req.query
      })
    }
    catch (e) {
      data = {error: e}
    }
  }
  else {
    data = {error: 'table not found'}
  }
  res.json(data)
})

router.post('/', async (req, res, next) => {
  console.log(req.body)
  let data = {}
  if (seq.hasOwnProperty(req.body.table)) {
    try {
      data = await seq[req.body.table].create(req.body.params)
    }
    catch (e) {
      data = {error: e}
    }
  }
  else {
    data = {error: 'table not found'}
  }
  res.json(data)
})

router.put('/', async (req, res, next) => {
  console.log(req.body)
  let data = {}
  if (seq.hasOwnProperty(req.body.table)) {
    try {
      data = await seq[req.body.table].update(req.body.changes,{
        where: req.body.params
      })
    }
    catch (e) {
      data = {error: e}
    }
  }
  else {
    data = {error: 'table not found'}
  }
  res.json(data)
})

router.delete('/', async (req, res, next) => {
  console.log(req.query)
  let data = {}
  if (seq.hasOwnProperty(req.query.table)) {
    try {
      let table = req.query.table
      delete req.query.table
      data = await seq[table].destroy({
        where: req.query
      })
    }
    catch (e) {
      data = {error: e}
    }
  }
  else {
    data = {error: 'table not found'}
  }
  res.json(data)
})

module.exports = router
