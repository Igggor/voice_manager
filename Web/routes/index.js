let express = require('express')
let router = express.Router()
const {where} = require("sequelize")
const seq = require('../dbmodels')

/* GET home page. */
router.get('/', async (req, res, next) => {
  const logList = await seq.Logs.findAll({raw: true, where: {raspberry_id: 1}}).then(function(logs) {
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
  res.render('index', { title: 'Главная', logList })
})

/* GET help page. */
router.get('/help', (req, res, next) => {
  res.render('help', { title: 'Помощь' })
})

module.exports = router
