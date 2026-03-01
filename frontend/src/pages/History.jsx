import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { listDebates, deleteDebate } from '../utils/api'
const SC = { complete:'#4ade80', running:'#facc15', pending:'#94a3b8', failed:'#f472b6' }
export default function History() {
  const [debates, setDebates] = useState([])
  useEffect(() => { listDebates().then(r=>setDebates(r.data)).catch(()=>{}) }, [])
  const del = async (id) => { await deleteDebate(id); setDebates(d=>d.filter(x=>x.id!==id)) }
  return (
    <div style={{ maxWidth:900, margin:'0 auto', padding:'32px 24px' }}>
      <h1 style={{ fontSize:24, marginBottom:24 }}>📜 Debate History</h1>
      {debates.map(d=>(
        <div key={d.id} style={{ background:'#12121a', border:'1px solid #2a2a40', borderRadius:10, padding:'16px 20px', marginBottom:10, display:'flex', justifyContent:'space-between', alignItems:'center' }}>
          <div><div style={{ fontSize:14, marginBottom:6 }}>{d.topic}</div>
            <div style={{ display:'flex', gap:12, fontSize:12, color:'#64748b' }}>
              <span style={{ color:SC[d.status], fontFamily:'Space Mono,monospace' }}>{d.status}</span>
              <span>{d.rounds} rounds</span><span style={{ color:'#4ade80' }}>{d.agent_pro}</span><span>vs</span><span style={{ color:'#f472b6' }}>{d.agent_con}</span>
              {d.winner&&d.winner!=='draw'&&<span style={{ color:'#facc15' }}>🏆 {d.winner}</span>}
            </div></div>
          <div style={{ display:'flex', gap:8 }}>
            <Link to={`/debate/${d.id}`} style={{ background:'#1a1a28', border:'1px solid #2a2a40', color:'#94a3b8', padding:'6px 12px', borderRadius:6, textDecoration:'none', fontSize:12 }}>View</Link>
            <button onClick={()=>del(d.id)} style={{ background:'#1a1a28', border:'1px solid #2a2a40', color:'#f472b6', padding:'6px 12px', borderRadius:6, cursor:'pointer', fontSize:12 }}>Delete</button>
          </div>
        </div>
      ))}
      {debates.length===0&&<div style={{ textAlign:'center', color:'#64748b', padding:60 }}>No debates yet. <Link to="/" style={{ color:'#4ade80' }}>Start one →</Link></div>}
    </div>
  )
}
