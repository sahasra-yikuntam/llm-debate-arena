import React, { useState } from 'react'
import ScoreBadge from './ScoreBadge'
const STANCE = { pro: { color:'#4ade80', label:'PRO' }, con: { color:'#f472b6', label:'CON' } }
export default function ArgumentCard({ arg }) {
  const [open, setOpen] = useState(true)
  const s = STANCE[arg.stance] || STANCE.pro
  return (
    <div style={{ background:'#12121a', border:`1px solid ${s.color}33`, borderLeft:`3px solid ${s.color}`, borderRadius:10, marginBottom:12, overflow:'hidden' }}>
      <div style={{ padding:'12px 16px', cursor:'pointer', display:'flex', justifyContent:'space-between', alignItems:'center' }} onClick={() => setOpen(o=>!o)}>
        <div style={{ display:'flex', alignItems:'center', gap:10 }}>
          <span style={{ background:s.color+'22', color:s.color, padding:'2px 8px', borderRadius:4, fontSize:11, fontFamily:'Space Mono,monospace', fontWeight:700 }}>{s.label}</span>
          <span style={{ fontSize:13, color:'#94a3b8' }}>Round {arg.round_number} · {arg.model}</span>
          {arg.overall_score!=null && <span style={{ fontSize:12, color:arg.overall_score>=0.75?'#4ade80':arg.overall_score>=0.5?'#facc15':'#f472b6' }}>⚖ {Math.round(arg.overall_score*100)}</span>}
        </div>
        <span style={{ color:'#64748b' }}>{open?'▲':'▼'}</span>
      </div>
      {open && (
        <div style={{ padding:'0 16px 16px' }}>
          <p style={{ fontSize:14, lineHeight:1.7, color:'#cbd5e1', marginBottom:16 }}>{arg.content}</p>
          <div style={{ display:'flex', gap:12, flexWrap:'wrap' }}>
            <ScoreBadge label="Logic" value={arg.logical_coherence} />
            <ScoreBadge label="Factual" value={arg.factual_grounding} />
            <ScoreBadge label="Rhetoric" value={arg.rhetorical_strength} />
            <ScoreBadge label="Fallacy↓" value={arg.fallacy_score!=null?1-arg.fallacy_score:null} />
            {arg.ml_score!=null && <ScoreBadge label="ML Score" value={arg.ml_score} />}
          </div>
        </div>
      )}
    </div>
  )
}
