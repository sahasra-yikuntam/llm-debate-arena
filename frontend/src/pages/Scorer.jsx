import React, { useState } from 'react'
import { scoreArgument } from '../utils/api'
const LC = { strong:'#4ade80', moderate:'#facc15', weak:'#f472b6' }
export default function Scorer() {
  const [topic, setTopic] = useState('')
  const [text, setText] = useState('')
  const [stance, setStance] = useState('pro')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const run = async () => {
    setLoading(true)
    try { const r = await scoreArgument({argument_text:text,topic,stance}); setResult(r.data) } finally { setLoading(false) }
  }
  return (
    <div style={{ maxWidth:700, margin:'0 auto', padding:'32px 24px' }}>
      <h1 style={{ fontSize:24, marginBottom:8 }}>⚡ Argument Scorer</h1>
      <p style={{ color:'#64748b', fontSize:14, marginBottom:28 }}>Score any argument using the fine-tuned DistilBERT classifier.</p>
      <div style={{ background:'#12121a', border:'1px solid #2a2a40', borderRadius:12, padding:24 }}>
        <div style={{ marginBottom:16 }}><label style={{ fontSize:12, color:'#94a3b8', display:'block', marginBottom:6 }}>TOPIC</label><input value={topic} onChange={e=>setTopic(e.target.value)} placeholder="What is this argument about?" style={{ width:'100%', background:'#0a0a0f', border:'1px solid #2a2a40', borderRadius:8, color:'#e2e8f0', padding:'8px 12px', fontSize:14, outline:'none' }} /></div>
        <div style={{ marginBottom:16 }}><label style={{ fontSize:12, color:'#94a3b8', display:'block', marginBottom:6 }}>ARGUMENT</label><textarea value={text} onChange={e=>setText(e.target.value)} rows={5} placeholder="Paste an argument to score..." style={{ width:'100%', background:'#0a0a0f', border:'1px solid #2a2a40', borderRadius:8, color:'#e2e8f0', padding:'10px 12px', fontSize:14, resize:'vertical', outline:'none', fontFamily:'Inter,sans-serif' }} /></div>
        <div style={{ display:'flex', gap:12, alignItems:'center' }}>
          <select value={stance} onChange={e=>setStance(e.target.value)} style={{ background:'#0a0a0f', border:'1px solid #2a2a40', color:'#e2e8f0', padding:'8px 12px', borderRadius:8, fontSize:14 }}><option value="pro">PRO</option><option value="con">CON</option></select>
          <button onClick={run} disabled={loading||!text.trim()||!topic.trim()} style={{ background:'linear-gradient(135deg,#a78bfa,#4ade80)', border:'none', borderRadius:8, padding:'10px 20px', color:'#0a0a0f', fontWeight:700, fontSize:14, cursor:'pointer', fontFamily:'Space Mono,monospace' }}>SCORE</button>
        </div>
      </div>
      {result&&<div style={{ marginTop:20, background:'#12121a', border:`1px solid ${LC[result.label]}44`, borderRadius:12, padding:24, textAlign:'center' }}>
        <div style={{ fontSize:48, fontFamily:'Space Mono,monospace', color:LC[result.label], marginBottom:8 }}>{Math.round(result.ml_score*100)}</div>
        <div style={{ fontSize:18, color:LC[result.label], fontFamily:'Space Mono,monospace', marginBottom:4 }}>{result.label.toUpperCase()}</div>
        <div style={{ fontSize:13, color:'#64748b' }}>Confidence: {Math.round(result.confidence*100)}%</div>
      </div>}
    </div>
  )
}
