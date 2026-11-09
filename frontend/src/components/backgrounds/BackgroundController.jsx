import React, { useState } from 'react';
import PacketFlowBackground from './PacketFlowBackground';
import ThreatContourBackground from './ThreatContourBackground';
import CyberRadarBackground from './CyberRadarBackground';
import ChromaticVoidBackground from './ChromaticVoidBackground';
import StarBorder from '../common/StarBorder';

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
          <StarBorder
            key={btn.id}
            as="button"
            type="button"
            onClick={() => setActiveMode(btn.id)}
            color={activeMode === btn.id ? "#00E5FF" : "#8E9EB5"}
            trailColor={activeMode === btn.id ? "#00E5FF" : "#8E9EB5"}
            duration={activeMode === btn.id ? 4 : 8}
            stars={activeMode === btn.id ? 2 : 1}
            glow={activeMode === btn.id ? 0.6 : 0.2}
            sparkle={activeMode === btn.id}
            radius={999}
            theme="dark"
            backgroundColor={activeMode === btn.id ? "rgba(0, 229, 255, 0.20)" : "transparent"}
            textColor={activeMode === btn.id ? "#00E5FF" : "#8E9EB5"}
            borderColor={activeMode === btn.id ? "rgba(0, 229, 255, 0.4)" : "rgba(142, 158, 181, 0.2)"}
            className="!px-3 !py-1 text-xs font-rajdhani font-bold tracking-wider cursor-pointer"
          >
            {btn.label}
          </StarBorder>
        ))}
      </div>
    </>
  );
};

export default BackgroundController;

