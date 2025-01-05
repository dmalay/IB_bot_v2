import * as ioTypes from '../types/io.types'
import { loginController } from '../controllers/authController'

export default (io, socket) => {
  const updateStatus = async (params) => {
    try {
      const response = await loginController(params)
      io.emit('IO', { event: ioTypes.UPDATE_STATUS, payload: response })
    } catch (e) {
      console.log('updateStatus ERR', e)
    }
  }

  // * * *  queries from client, processed with controllers
  socket.on(ioTypes.UPDATE_STATUS, async (payload) => updateStatus(payload))
}
