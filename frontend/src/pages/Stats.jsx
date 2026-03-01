import React, { useState, useEffect } from 'react'
import { getStats } from '../utils/api'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
export default function Stats() {
  const [stats, setStats] = useState(null)
  useEffect(() => { getStats().then(r=>setStats(r.data)).catch(()=>{}) }, [])
  if (!stats) return <div style={{ padding:40, color:'#64748b' }}>Loading...</div>
  const winsData = Object.entries(stats.wins_by_agent||{}).map(([name,count])=>({name,count}))
  const cards = [['Total Debates',stats.total_debates,'#4ade80'],['Complete',stats.complete_debates,'#22d3ee'],['Arguments',stats.total_arguments,'#a78bfa'],['Avg Score',stats.avg_argument_score?(stats.avg_argument_score*100).toFixed(0)+'%':'N/A','#facc15']]
  return (
    <div style={{ maxWidth:900, margin:'0 auto', padding:'32px 24px' }}>
      <h1 style={{ fontSize:24, marginBottom:24 }}>📊 Stats</h1>
      <div style={{ display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:16, marginBottom:32 }}>
        {cards.map(([l,v,c])=><div key={l} style={{ background:'#12121a', border:'1px solid #2a2a40', borderRadius:10, padding:20 }}><div style={{ fontSize:28, fontFamily:'Space Mono,monospace', color:c, marginBottom:4 }}>{v}</div><div style={{ fontSize:12, color:'#64748b' }}>{l}</div></div>)}
      </div>
      {winsData.length>0&&<div style={{ background:'#12121a', border:'1px solid #2a2a40', borderRadius:10, padding:24 }}>
        <h2 style={{ fontSize:16, marginBottom:20 }}>🏆 Wins by Agent</h2>
        <ResponsiveContainer width="100%" height={200}><BarChart data={winsData}><XAxis dataKey="name" stroke="#64748b" fontSize={12}/><YAxis stroke="#64748b" fontSize={12}/><Tooltip contentStyle={{ background:'#1a1a28', border:'1px solid #2a2a40', borderRadius:8 }}/><Bar dataKey="count" radius={[4,4,0,0]}>{winsData.map((_,i)=><Cell key={i} fill={i%2===0?'#4ade80':'#f472b6'}/>)}</Bar></BarChart></ResponsiveContainer>
      </div>}
    </div>
  )
}
