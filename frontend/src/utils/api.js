import axios from 'axios'
const api = axios.create({ baseURL: '/api' })
export const createDebate = (p) => api.post('/debates/', p)
export const listDebates = (skip=0, limit=20) => api.get('/debates/', { params: { skip, limit } })
export const getDebate = (id) => api.get(`/debates/${id}`)
export const deleteDebate = (id) => api.delete(`/debates/${id}`)
export const getStats = () => api.get('/debates/stats/summary')
export const scoreArgument = (p) => api.post('/debates/score', p)
export default api
