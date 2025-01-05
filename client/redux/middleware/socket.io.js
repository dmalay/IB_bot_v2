import io from 'socket.io-client'

import * as analyticsTypes from '../types/analytics.types'

const token = localStorage.getItem('token')

function socketMiddleware() {
  return (store) => {
    const socket = io({ auth: { token } })
    socket.on('IO', (data) => {
      const { event, payload } = data
      console.log('IO on', event)
      if (analyticsTypes[event] === event) {
        store.dispatch({ type: event, payload })
      }
    })

    return (next) => (action) => {
      if (typeof action === 'function') {
        return next(action)
      }
      const {
        event, emit, payload, leave
      } = action
      if (!event) {
        return next(action)
      }
      if (leave) {
        socket.removeListener(event)
      }
      if (emit) {
        console.log('emit:', event, payload)
        return socket.emit(event, payload)
      }
      return next(action)
    }
  }
}

export default socketMiddleware

/* * * * *  redux middleware.  * * * * *

Dispatch specific redux actions anytime those events
are broadcasted to store from the socket.io server.
socket connection is created only once on the store loading.
* * *
client --> server
to emit directly from dispatch any dispatch call should have
the following format ->
        dispatch({
          event: 'UPDATE_STATUS',
          emit: true,
          payload: your_data
        })
* * *
server --> client
to emit from server the emit call should have the following format ->
        io.emit('IO', { event: 'UPDATE_STATUS', payload: your_data })

 * * * * * * * * * * * * * * * * * * */
