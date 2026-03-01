import React, { useState, useEffect, useRef } from 'react'
import { createDebate, getDebate } from '../utils/api'
import ArgumentCard from '../components/ArgumentCard'
const SUGGESTED = ["AI will eliminate more jobs than it creates in the next decade","Social media has done more harm than good to society","Universal basic income should be implemented globally","Nuclear energy is essential for solving climate change"]
export default function Arena() {
  const [topic, setTopic] = useState('')
  const [rounds, setRounds] = useState(3)
  const [agentPro, setAgentPro] = useState('claude')
  const [agentCon, setAgentCon] = useState('openai')
  const [debate, setDebate] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const pollRef = useRef(null)
  const startDebate = async () => {
    if (!topic.trim()) return
    setLoading(true); setError(null); setDebate(null)
    try {
      const res = await createDebate({ topic, rounds, agent_pro: agentPro, agent_con: agentCon })
      setDebate(res.data)
      pollRef.current = setInterval(async () => {
        const r = await getDebate(res.data.id)
        setDebate(r.data)
        if (['complete','failed'].includes(r.data.status)) { clearInterval(pollRef.current); setLoading(false) }
      }, 1500)
    } catch(e) { setError(e.response?.data?.detail || 'Failed'); setLoading(false) }
  }
  useEffect(() => () => clearInterval(pollRef.current), [])
  const proArgs = (debate?.arguments||[]).filter(a=>a.stance==='pro')
  const conArgs = (debate?.arguments||[]).filter(a=>a.stance==='con')
  return (
    <div style={{ maxWidth:900, margin:'0 auto', padding:'32px 24px' }}>
      <h1 style={{ fontSize:28, marginBottom:8 }}>⚔️ Debate Arena</h1>
      <p style={{ color:'#64748b', fontSize:14, marginBottom:24 }}>Pit two LLMs against each other and score argument quality.</p>
      <div style={{ background:'#12121a', border:'1px solid #2a2a40', borderRadius:12, padding:24, marginBottom:32 }}>
        <label style={{ fontSize:12, color:'#94a3b8', display:'block', marginBottom:6, fontFamily:'Space Mono,monospace' }}>DEBATE TOPIC</label>
        <textarea value={topic} onChange={e=>setTopic(e.target.value)} placeholder="Enter a debate topic..." style={{ width:'100%', background:'#0a0a0f', border:'1px solid #2a2a40', borderRadius:8, color:'#e2e8f0', padding:'10px 14px', fontSize:14, resize:'vertical', minHeight:72, outline:'none', fontFamily:'Inter,sans-serif' }} />
        <div style={{ display:'flex', gap:6, flexWrap:'wrap', marginTop:8, marginBottom:16 }}>
          {SUGGESTED.map(s=><button key={s} onClick={()=>setTopic(s)} style={{ background:'#1a1a28', border:'1px solid #2a2a40', color:'#94a3b8', padding:'4px 10px', borderRadius:20, fontSize:11, cursor:'pointer' }}>{s.slice(0,40)}…</button>)}
        </div>
        <div style={{ display:'flex', gap:16, flexWrap:'wrap', alignItems:'flex-end' }}>
          <div><label style={{ fontSize:12, color:'#94a3b8', display:'block', marginBottom:6 }}>ROUNDS</label>
            <select value={rounds} onChange={e=>setRounds(Number(e.target.value))} style={{ background:'#0a0a0f', border:'1px solid #2a2a40', color:'#e2e8f0', padding:'8px 12px', borderRadius:8, fontSize:14 }}>{[1,2,3,4,5].map(r=><option key={r} value={r}>{r}</option>)}</select></div>
          <div><label style={{ fontSize:12, color:'#4ade80', display:'block', marginBottom:6 }}>PRO AGENT</label>
            <select value={agentPro} onChange={e=>setAgentPro(e.target.value)} style={{ background:'#0a0a0f', border:'1px solid #4ade8044', color:'#4ade80', padding:'8px 12px', borderRadius:8, fontSize:14 }}><option value="claude">Claude</option><option value="openai">GPT-4o-mini</option></select></div>
          <div><label style={{ fontSize:12, color:'#f472b6', display:'block', marginBottom:6 }}>CON AGENT</label>
            <select value={agentCon} onChange={e=>setAgentCon(e.target.value)} style={{ background:'#0a0a0f', border:'1px solid #f472b644', color:'#f472b6', padding:'8px 12px', borderRadius:8, fontSize:14 }}><option value="openai">GPT-4o-mini</option><option value="claude">Claude</option></select></div>
          <button onClick={startDebate} disabled={loading||!topic.trim()} style={{ background:loading?'#1a1a28':'linear-gradient(135deg,#4ade80,#22d3ee)', border:'none', borderRadius:8, padding:'10px 24px', color:loading?'#64748b':'#0a0a0f', fontWeight:700, fontSize:14, cursor:loading?'not-allowed':'pointer', fontFamily:'Space Mono,monospace' }}>{loading?'Running...':'START DEBATE'}</button>
        </div>
        {error && <p style={{ color:'#f472b6', fontSize:13, marginTop:12 }}>⚠ {error}</p>}
      </div>
      {debate && (
        <div>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:16 }}>
            <div><h2 style={{ fontSize:18, marginBottom:4 }}>{debate.topic}</h2>
              <span style={{ fontSize:11, padding:'2px 10px', borderRadius:20, fontFamily:'Space Mono,monospace', background:debate.status==='complete'?'#4ade8022':'#facc1522', color:debate.status==='complete'?'#4ade80':'#facc15' }}>{debate.status.toUpperCase()}</span></div>
            {debate.winner && <div style={{ textAlign:'right' }}><div style={{ fontSize:11, color:'#64748b' }}>WINNER</div><div style={{ fontSize:16, fontFamily:'Space Mono,monospace', color:'#facc15' }}>🏆 {debate.winner.toUpperCase()}</div></div>}
          </div>
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:16 }}>
            <div><div style={{ fontSize:11, color:'#4ade80', fontFamily:'Space Mono,monospace', marginBottom:8 }}>PRO — {debate.agent_pro.toUpperCase()}</div>{proArgs.map(a=><ArgumentCard key={a.id} arg={a} />)}</div>
            <div><div style={{ fontSize:11, color:'#f472b6', fontFamily:'Space Mono,monospace', marginBottom:8 }}>CON — {debate.agent_con.toUpperCase()}</div>{conArgs.map(a=><ArgumentCard key={a.id} arg={a} />)}</div>
          </div>
        </div>
      )}
    </div>
  )
}
