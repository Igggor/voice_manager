let express = require('express')
let router = express.Router()
// const {where} = require("sequelize")
// const seq = require('../dbmodels')
// const {joinSQLFragments} = require("sequelize/lib/utils/join-sql-fragments");

function generateRandomString(length) {
  let result = ''
  let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let charactersLength = characters.length
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength))
  }
  return result
}

router.get('/', (req, res, next) => {
  console.log('Cookie: ', req.cookies.sessionId)
  if (req.cookies.sessionId === 'qwerty123') {
    next()
  }
  else {
    res.redirect('/account/login')
  }
}, (req, res) => {
  let h = req.headers
  res.render('account', {page: 'account', title: "Аккаунт"})
})

router.get('/login', (req, res) => {
  res.render('login', {page: 'login', title: "Вход", isSignInUp: true})
})
router.post('/login', (req, res) => {
  console.log(req.body)
  if(req.body.operationType === 'login' && req.body.password === '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4') {
    let sessionIdString = generateRandomString(128)

    res.send({ correct : true, sessionId : sessionIdString })
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
  // const [user, created] = await seq.Users.findOrCreate({
  //   where: {username: req.body.username},
  //   defaults: {password: req.body.password}
  // })
  if (created) {
    res.sendStatus(200)
  }
  else {
    res.sendStatus(400)
  }
})

module.exports = router;