import jwt from 'jsonwebtoken'

import options from '../config'
import User from '../models/user.model'
import registerValidation from '../validators/registerValidator'

const generateToken = (user) => {
  const payload = { _id: user._id }
  const token = jwt.sign(payload, options.jwtSecret, { expiresIn: '365d' })
  return token
}

export const loginController = async (req, res) => {
  try {
    const { login, password } = req.body
    const user = await User.findAndValidateUser({ login, password })
    user.password = ''
    console.log(`user logged in: ${user.username}`)
    const token = generateToken(user)
    return res.status(200).json({
      message: 'User Successfully Logged In',
      user,
      token,
    })
  } catch (err) {
    return res.status(500).json({ message: err.message })
  }
}

export const tokenController = async (req, res) => {
  try {
    // const login = 'testMain'
    // const user = await User.findThisUser({ login })

    const bearerToken = req.headers.authorization.replace('Bearer ', '')
    const jwtUser = jwt.verify(bearerToken, options.jwtSecret)
    const user = await User.findById(jwtUser._id)
    user.password = ''
    const token = generateToken(user)
    console.log(`user ${user.username} logged in with current token`)
    return res
      .status(200)
      .json({ message: 'User Successfully Logged In', user, token })
  } catch (err) {
    return res.status(500).json({ message: err.message })
  }
}

export const registerController = async (req, res) => {
  try {
    const { username, email, password } = req.body
    const { error } = registerValidation({ username, email, password })
    console.log(error)
    if (error) {
      return res.status(400).send(error.details[0].message)
    }
    const doesUserExist = await User.exists({
      // eslint-disable-next-line object-shorthand
      username: username, email: email,
    })
    if (doesUserExist) {
      return res.status(400).send({ message: 'This User Already Exists' })
    }
    const user = new User({ username, email, password })
    await user.save()
    user.password = ''
    const token = generateToken(user)
    console.log(`new user registered: ${user.username}`)
    return res.status(200).json({
      message: 'User Successfully Registered',
      user,
      token,
    })
  } catch (err) {
    return res.status(500).json({ message: err.message })
  }
}
