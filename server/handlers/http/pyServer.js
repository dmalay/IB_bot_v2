import axios from 'axios'

const predictUrl = 'http://localhost:5000/predict'

export const predictRequest = async (dataset) => {
  try {
    const { data } = await axios.post(predictUrl, dataset)
    return data.prediction
  } catch (e) {
    console.error(`Error: ${e.message}`, e)
    return { error: e.response.status, message: e.response.statusText }
  }
}

export const doSmth = () => {}
