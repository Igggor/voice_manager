let express = require('express')
let router = express.Router()
const {where} = require("sequelize")
const seq = require('../dbmodels')

router.get('/:table', async (req, res, next) => {
  console.log(req.query)
  if (process.env.API_KEY === undefined || req.query.key !== process.env.API_KEY) {
    res.json({error: 'Error API Key'})
    return 0
  }
  let data = {}
  delete req.query.key
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
  if (process.env.API_KEY === undefined || req.query.key !== process.env.API_KEY) {
    res.json({error: 'Error API Key'})
    return 0
  }
  let data = {}
  delete req.query.key
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
  if (process.env.API_KEY === undefined || req.query.key !== process.env.API_KEY) {
    res.json({error: 'Error API Key'})
    return 0
  }
  let data = {}
  delete req.query.key
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
  if (process.env.API_KEY === undefined || req.query.key !== process.env.API_KEY) {
    res.json({error: 'Error API Key'})
    return 0
  }
  let data = {}
  delete req.query.key
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
