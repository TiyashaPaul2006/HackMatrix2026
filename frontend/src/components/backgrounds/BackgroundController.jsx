import React, { useState } from 'react';
import PacketFlowBackground from './PacketFlowBackground';
import ThreatContourBackground from './ThreatContourBackground';
import CyberRadarBackground from './CyberRadarBackground';
import ChromaticVoidBackground from './ChromaticVoidBackground';

const MODES = [
  { id: 'radar', label: '🛡️ Radar', component: CyberRadarBackground },
  { id: 'packet', label: '🧠 Neural Flow', component: PacketFlowBackground },
  { id: 'contour', label: '〰️ Contours', component: ThreatContourBackground },
  { id: 'aurora', label: '🌌 Void', component: ChromaticVoidBackground },
];

export const BackgroundController = () => {
  const [activeMode, setActiveMode] = useState('radar');
  const ActiveBg = MODES.find((m) => m.id === activeMode)?.component || CyberRadarBackground;

  return (
    <>
      <ActiveBg />

      {/* Floating switcher pill in bottom-right corner */}
      <div className="fixed bottom-5 right-5 z-40 hidden sm:flex items-center gap-1.5 p-1.5 bg-[#0C1A2E]/85 backdrop-blur-md border border-[#00E5FF]/30 rounded-full shadow-[0_8px_32px_rgba(0,0,0,0.6)]">
        <span className="text-[10px] font-rajdhani font-semibold text-[#8E9EB5] px-2 uppercase tracking-wider">
          Theme
        </span>
        {MODES.map((btn) => (
          <button
            key={btn.id}
            type="button"
            onClick={() => setActiveMode(btn.id)}
            className={`px-3 py-1 rounded-full text-xs font-rajdhani font-bold tracking-wider transition-all ${
              activeMode === btn.id
                ? 'bg-[#00E5FF] text-[#060D1A] shadow-cyan-sm'
                : 'text-[#8E9EB5] hover:text-white hover:bg-[#162440]'
            }`}
          >
            {btn.label}
          </button>
        ))}
      </div>
    </>
  );
};

export default BackgroundController;

