let express = require('express')
let router = express.Router()
const {where} = require("sequelize")
const seq = require('../dbmodels')
const {raw} = require("express");

/* GET home page. */
router.get('/', async (req, res, next) => {
  if (await seq.Sessions.findByPk(req.cookies.sessionId) != null) {
    next()
  }
  else {
    res.redirect('/account/login')
  }
}, async (req, res, next) => {
  const logList = await seq.Logs.findAll({raw: true, where: {raspberry_id: (await seq.Sessions.findByPk(req.cookies.sessionId, {raw: true})).user_id}}).then(function(logs) {
    logs = logs.map(function (log) {
      let times = new Date(log.createdAt)
      let hours = String(times.getHours()).padStart(2, "0")
      let minutes = String(times.getMinutes()).padStart(2, "0")
      let seconds = String(times.getSeconds()).padStart(2, "0")
      log.createdAt = `${hours}:${minutes}:${seconds}`
      return log
    })
    return logs
  })
  const deviceList = await seq.Devices.findAll({raw: true, where: {user_id: (await seq.Sessions.findByPk(req.cookies.sessionId, {raw: true})).user_id}})
  res.render('index', { title: 'Главная', page: 'main', logList, deviceList})
})

/* GET help page. */
router.get('/help', async (req, res, next) => {
  if (await seq.Sessions.findByPk(req.cookies.sessionId) != null) {
    next()
  }
  else {
    res.redirect('/account/login')
  }
}, async (req, res, next) => {
  if ((await seq.Users.findByPk((await seq.Sessions.findByPk(req.cookies.sessionId)).user_id)).role === 'admin') {
    const questionList = await seq.Questions.findAll({raw: true})
    questionList.reverse()
    res.render('help', { title: 'Помощь', page: 'help', admin: true, questionList })
  }
  else {
    res.render('help', { title: 'Помощь', page: 'help', admin: false })
  }
})

router.post('/help', async (req, res) => {
  console.log(req.body)
  await seq.Questions.create({user_id: (await seq.Sessions.findByPk(req.cookies.sessionId)).user_id, theme: req.body.theme, question: req.body.question})
  res.status(201).send()
})

/* GET devices page. */
router.get('/devices', async (req, res, next) => {
  if (await seq.Sessions.findByPk(req.cookies.sessionId) != null) {
    next()
  }
  else {
    res.redirect('/account/login')
  }
}, async (req, res, next) => {
  const deviceList = await seq.Devices.findAll({raw: true, where: {user_id: (await seq.Sessions.findByPk(req.cookies.sessionId, {raw: true})).user_id}})
  res.render('devices', { title: 'Устройства', page: 'devices', deviceList })
})

router.post('/devices', async (req, res, next) => {
  console.log(req.body)
  await seq.Devices.update({
    user_id: (await seq.Sessions.findByPk(req.cookies.sessionId, {raw: true})).user_id,
  }, {
    where: {hash_key: req.body.hashKey},
  })
  res.status(200).send()
})

module.exports = router
