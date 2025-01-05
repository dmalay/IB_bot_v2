import { combineReducers } from 'redux'
import { connectRouter } from 'connected-react-router'
import analytics from './analytics.reducer'

const createRootReducer = (history) => {
  return combineReducers({
    router: connectRouter(history),
    analytics,
  })
}

export default createRootReducer
