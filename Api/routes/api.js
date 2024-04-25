let express = require('express')
let router = express.Router()
const {where} = require("sequelize")
const seq = require('../dbmodels')

router.get('/:table', async (req, res, next) => {
  console.log(req.query)
  let data = {}
  try {
    data = await seq[req.params.table].findAll({
      where: req.query
    })
  }
  catch (e) {
    data = {error: e}
  }
  res.json(data)
})

router.post('/:table', async (req, res, next) => {
  console.log(req.body)
  let data = {}
  try {
    data = await seq[req.params.table].create(req.body.params)
  }
  catch (e) {
    data = {error: e}
  }
  res.json(data)
})

router.put('/:table', async (req, res, next) => {
  console.log(req.body)
  let data = {}
  try {
    data = await seq[req.params.table].update(req.body.changes,{
      where: req.body.params
    })
  }
  catch (e) {
    data = {error: e}
  }
  res.json(data)
})

router.delete('/:table', async (req, res, next) => {
  console.log(req.query)
  let data = {}
    try {
      data = await seq[req.params.table].destroy({
        where: req.query
      })
    }
    catch (e) {
      data = {error: e}
    }
  res.json(data)
})

module.exports = router
