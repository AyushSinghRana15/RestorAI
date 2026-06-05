import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export async function uploadImage(file) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/upload', form)
  return data
}

export async function restoreImage(jobId, options = {}) {
  const { data } = await api.post(`/restore/${jobId}`, options)
  return data
}

export async function downloadImage(jobId) {
  const { data } = await api.get(`/download/${jobId}`, { responseType: 'blob' })
  return data
}

export async function getStatus(jobId) {
  const { data } = await api.get(`/status/${jobId}`)
  return data
}
