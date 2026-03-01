import React from 'react'
const color = (s) => s >= 0.75 ? '#4ade80' : s >= 0.5 ? '#facc15' : '#f472b6'
export default function ScoreBadge({ label, value }) {
  if (value == null) return null
  const c = color(value)
  return (
    <div style={{ display:'flex', flexDirection:'column', alignItems:'center', gap:4 }}>
      <div style={{ width:48, height:48, borderRadius:'50%', border:`3px solid ${c}`, display:'flex', alignItems:'center', justifyContent:'center', fontSize:13, fontWeight:700, color:c, fontFamily:'Space Mono,monospace' }}>{Math.round(value*100)}</div>
      <span style={{ fontSize:10, color:'#64748b', textAlign:'center', maxWidth:54 }}>{label}</span>
    </div>
  )
}
