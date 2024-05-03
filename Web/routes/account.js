let express = require('express')
let router = express.Router()
let crypto = require('crypto')
const {where} = require("sequelize")
const seq = require('../dbmodels')

function generateRandomString(length) {
  let result = ''
  let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let charactersLength = characters.length
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength))
  }
  return result
}

function generateCrypto() {
  return crypto.randomBytes(32).toString('base64');
}

router.get('/', async (req, res, next) => {
  if (await seq.Sessions.findByPk(req.cookies.sessionId) != null) {
    next()
  }
  else {
    res.redirect('/account/login')
  }
}, async (req, res) => {
  let h = req.headers
  const userData = (await seq.Users.findByPk((await seq.Sessions.findByPk(req.cookies.sessionId)).user_id)).dataValues
  res.render('account', {page: 'account', title: "Аккаунт", isAccount: true, userData})
})

router.post('/', async (req, res, next) => {
  if (req.body.operationType === 'exit') {
    await seq.Sessions.destroy({
      where: {
        id: req.cookies.sessionId
      }
    })
    res.clearCookie('sessionId')
    res.end()
  }
})

router.get('/login', (req, res) => {
  res.render('login', {page: 'login', title: "Вход", isSignInUp: true})
})

router.post('/login', async (req, res) => {
  console.log(req.body)
  const user = (await seq.Users.findAll({where: { email: req.body.email }}))[0]
  if(user !== undefined && req.body.password === user.password) {
    let sessionIdString = generateCrypto()
    while (await seq.Sessions.findByPk(sessionIdString) !== null) {
      sessionIdString = generateCrypto()
    }
    await seq.Sessions.create({id: sessionIdString, user_id: user.id})
    res.cookie('sessionId', sessionIdString, { httpOnly: true })
    res.send({ correct : true })
  }
  else {
    res.send({ correct : false })
  }
})

router.get('/signup', (req, res) => {
  res.render('signup', {page: 'signup', title: "Регистрация", isSignInUp: true})
})

router.post('/signup', async function (req, res) {
  console.log(req.body)
  const [user, created] = await seq.Users.findOrCreate({
    where: {email: req.body.userData.email},
    defaults: req.body.userData
  })
  if (created) {
    let sessionIdString = generateCrypto()
    while (await seq.Sessions.findByPk(sessionIdString) !== null) {
      sessionIdString = generateCrypto()
    }
    await seq.Sessions.create({id: sessionIdString, user_id: user.id})
    res.cookie('sessionId', sessionIdString, { httpOnly: true })
    res.sendStatus(200)
  }
  else {
    res.sendStatus(400)
  }
})

module.exports = router;