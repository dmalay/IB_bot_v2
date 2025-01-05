import * as analyticsTypes from '../types/analytics.types'

const initialState = {
  status: {},
  token: '',
}

const analytics = (state = initialState, action) => {
  switch (action.type) {
    // NEW v1
    case analyticsTypes.UPDATE_STATUS: {
      const oldStatus = state.status
      const newStatus = action.payload
      return {
        ...state,
        status: { ...oldStatus, ...newStatus }
      }
    }

    default:
      return state
  }
}

export default analytics
