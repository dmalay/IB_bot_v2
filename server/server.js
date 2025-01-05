import express from 'express'
import cors from 'cors'
import path from 'path'
import http from 'http'
import passport from 'passport'
import { spawn } from 'child_process'

import options from './config'
import router from './router'
import jwtStrategy from './services/passport'
import mongooseService from './services/mongoose'
import SocketIO from './sockets'

const app = express()

const PORT = options.port

mongooseService.connect()

const middleware = [
  cors(),
  express.urlencoded({ limit: '50mb', extended: true, parameterLimit: 50000 }),
  express.json({ limit: '50mb', extended: true }),
  router,
]

passport.use('jwt', jwtStrategy)

middleware.forEach((it) => app.use(it))

if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.resolve('build')))
  app.get('*', (req, res) => {
    res.sendFile(path.resolve('build', 'index.html'))
  })
}

const server = http.createServer(app)

SocketIO(server)

server.listen(PORT, (error) => {
  if (error) throw error
  console.log(`listening on port:${PORT}`)
})

const pythonServer = spawn('python3', ['python-scripts/api_server.py']);

pythonServer.stdout.on('data', (data) => {
  console.log(`Python Server: ${data}`);
});

pythonServer.stderr.on('data', (data) => {
  console.error(`Python Error: ${data}`);
});

pythonServer.on('close', (code) => {
  console.log(`Python server process exited with code ${code}`);
});
