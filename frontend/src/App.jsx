import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Nav from './components/Nav'
import Arena from './pages/Arena'
import History from './pages/History'
import Stats from './pages/Stats'
import Scorer from './pages/Scorer'
import DebateView from './pages/DebateView'
export default function App() {
  return (<><Nav /><Routes><Route path="/" element={<Arena />} /><Route path="/history" element={<History />} /><Route path="/debate/:id" element={<DebateView />} /><Route path="/scorer" element={<Scorer />} /><Route path="/stats" element={<Stats />} /></Routes></>)
}
