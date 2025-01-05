import jwt from 'jsonwebtoken'
import options from '../config'

const socketAuthMiddleware = (socket, next) => {
  const { token } = socket.handshake.auth
  if (!token) {
    const err = new Error('not authorized')
    next(err)
  }
  jwt.verify(token, options.jwtSecret, (err, user) => {
    if (err) {
      next({ error: err })
    }
    socket.user = user
  })
  next()
}

export default socketAuthMiddleware
