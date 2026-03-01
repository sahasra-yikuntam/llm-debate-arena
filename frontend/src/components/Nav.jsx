import React from 'react'
import { Link, useLocation } from 'react-router-dom'
const links = [{to:'/',label:'Arena'},{to:'/history',label:'History'},{to:'/scorer',label:'Scorer'},{to:'/stats',label:'Stats'}]
export default function Nav() {
  const loc = useLocation()
  return (
    <nav style={{ background:'#0d0d16', borderBottom:'1px solid #2a2a40', padding:'0 24px', display:'flex', alignItems:'center', gap:8, height:56, position:'sticky', top:0, zIndex:100 }}>
      <Link to="/" style={{ textDecoration:'none', marginRight:24, fontFamily:'Space Mono,monospace', fontSize:14, color:'#e2e8f0', fontWeight:700 }}>⚔️ LLM Debate Arena</Link>
      {links.map(({to,label}) => (
        <Link key={to} to={to} style={{ textDecoration:'none', padding:'6px 12px', borderRadius:6, color:loc.pathname===to?'#e2e8f0':'#64748b', background:loc.pathname===to?'#1a1a28':'transparent', fontSize:13 }}>{label}</Link>
      ))}
    </nav>
  )
}
