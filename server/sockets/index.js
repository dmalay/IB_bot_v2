import { Server } from 'socket.io'

import socketAuthMiddleware from '../middleware/socketAuth'

import userHandlers from '../handlers/userHandlers'

let io

const SocketIO = (server) => {
  io = new Server(server)

  io.use((socket, next) => {
    socketAuthMiddleware(socket, next)
  })

  io.on('connection', (socket) => {
    userHandlers(io, socket)

    socket.on('disconnect', () => {
      console.log(`socket: ${socket} disconnected`)
    })
  })
}

export const emitMessage = (event, message) => io.emit(event, message)

export default SocketIO
