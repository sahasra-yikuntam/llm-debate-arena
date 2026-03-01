import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getDebate } from '../utils/api'
import ArgumentCard from '../components/ArgumentCard'
export default function DebateView() {
  const { id } = useParams()
  const [debate, setDebate] = useState(null)
  useEffect(() => { getDebate(id).then(r=>setDebate(r.data)).catch(()=>{}) }, [id])
  if (!debate) return <div style={{ padding:40, color:'#64748b' }}>Loading...</div>
  const proArgs = debate.arguments.filter(a=>a.stance==='pro')
  const conArgs = debate.arguments.filter(a=>a.stance==='con')
  return (
    <div style={{ maxWidth:1000, margin:'0 auto', padding:'32px 24px' }}>
      <Link to="/history" style={{ color:'#64748b', textDecoration:'none', fontSize:13, display:'block', marginBottom:24 }}>← Back to History</Link>
      <h1 style={{ fontSize:20, marginBottom:8 }}>{debate.topic}</h1>
      <div style={{ display:'flex', gap:12, fontSize:12, color:'#64748b', marginBottom:28 }}>
        <span>{debate.rounds} rounds</span><span style={{ color:'#4ade80' }}>{debate.agent_pro} (PRO)</span><span>vs</span><span style={{ color:'#f472b6' }}>{debate.agent_con} (CON)</span>
        {debate.winner&&<span style={{ color:'#facc15' }}>🏆 {debate.winner}</span>}
      </div>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20 }}>
        <div><div style={{ fontSize:11, color:'#4ade80', fontFamily:'Space Mono,monospace', marginBottom:12 }}>PRO</div>{proArgs.map(a=><ArgumentCard key={a.id} arg={a}/>)}</div>
        <div><div style={{ fontSize:11, color:'#f472b6', fontFamily:'Space Mono,monospace', marginBottom:12 }}>CON</div>{conArgs.map(a=><ArgumentCard key={a.id} arg={a}/>)}</div>
      </div>
    </div>
  )
}
