let express = require('express')
let router = express.Router()
const {where} = require("sequelize")
const seq = require('../dbmodels')

router.get('/', async (req, res, next) => {
  console.log(req.body.table)
  let data = {}
  if (seq.hasOwnProperty(req.body.table)) {
    try {
      data = await seq[req.body.table].findAll({
        where: JSON.parse(req.body.params)
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
      data = await seq[req.body.table].create(JSON.parse(req.body.params))
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
      data = await seq[req.body.table].update(JSON.parse(req.body.changes),{
        where: JSON.parse(req.body.params)
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
  console.log(req.body.table)
  let data = {}
  if (seq.hasOwnProperty(req.body.table)) {
    try {
      data = await seq[req.body.table].destroy({
        where: JSON.parse(req.body.params)
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

  console.log(req.body)
})

module.exports = router
