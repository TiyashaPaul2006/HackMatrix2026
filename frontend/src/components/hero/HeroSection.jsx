import React, { useState } from 'react';
import { ArrowRight, AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';
import RotatingText from '../common/RotatingText';
import CurvedInput from '../common/CurvedInput';
import SpotlightCard from '../common/SpotlightCard';

export const HeroSection = () => {
  const [targetUrl, setTargetUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [verdict, setVerdict] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const executeScan = async (urlOverride) => {
    const finalUrl = (urlOverride !== undefined ? urlOverride : targetUrl).trim();
    if (!finalUrl) return;

    setLoading(true);
    setErrorMsg(null);
    setVerdict(null);

    const startTime = performance.now();

    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ url: finalUrl }),
      });

      const clientLatency = (performance.now() - startTime).toFixed(1);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      setVerdict({
        ...data,
        targetUrl: finalUrl,
        clientLatency: data.response_time_ms ? `${data.response_time_ms} ms` : `${clientLatency} ms`,
      });
    } catch (err) {
      setErrorMsg(
        'FastAPI service unreachable at http://127.0.0.1:8000. Start backend with `python -m uvicorn src.app:app --host 127.0.0.1 --port 8000 --reload`'
      );
    } finally {
      setLoading(false);
    }
  };

  const isPhishing = verdict?.prediction?.toLowerCase() === 'phishing' || verdict?.label === 1;

  return (
    <section id="scanner" className="relative z-10 pt-28 pb-16 px-4 max-w-4xl mx-auto text-center">
      
      {/* 1. Main Title with React Bits RotatingText */}
      <h1
        style={{ fontFamily: "'Kelly Slab', serif" }}
        className="font-kelly text-4xl sm:text-5xl md:text-[56px] text-[#F8FAFC] tracking-wide leading-[1.25] mb-4"
      >
        <span>
          <span className="bg-[#06B6D4] text-[#080C14] px-2.5 py-0.5 rounded-md shadow-[0_0_20px_rgba(6,182,212,0.35)] inline-block mr-2">
            Web
          </span>
          threat detection,
        </span>
        <br />
        <span className="inline-flex items-center justify-center gap-2.5 flex-wrap">
          <span>with</span>
          <RotatingText
            texts={['evidence.', 'proof.', 'confidence.']}
            effect="slide"
            direction="down"
            highlight={true}
            highlightColor="#06b6d4"
            staggerFrom="random"
            staggerDuration={0.05}
            splitLevelClassName="overflow-hidden pb-0.5 sm:pb-1 md:pb-1"
            rotationInterval={2500}
            splitBy="words"
            blur={8}
            mainClassName="inline-flex text-[#080C14] px-2.5 py-0.5 rounded-md shadow-[0_0_20px_rgba(6,182,212,0.35)]"
            elementLevelClassName="text-[#080C14]"
          />
        </span>
      </h1>

      {/* 2. Subtitle */}
      <p className="font-ui text-[#06B6D4] text-sm sm:text-[15px] max-w-2xl mx-auto mb-10 leading-relaxed">
        Inspect suspicious URLs with a 16-feature machine-learning classifier. See the signals behind its prediction, then assess website security separately.
      </p>

      {/* 3. Target URL CurvedInput Command Box */}
      <div className="text-left max-w-2xl mx-auto mb-10">
        <CurvedInput
          topLabel="Target URL"
          bottomLeftText="Enter a complete URL to request a model prediction."
          bottomRightText="[Enter] to scan"
          placeholder="https://example.com/login"
          buttonText={loading ? "Scanning…" : "Scan target URL"}
          theme="dark"
          bend={-15}
          height={52}
          width="100%"
          type="url"
          value={targetUrl}
          onChange={val => setTargetUrl(val)}
          onSubmit={val => executeScan(val)}
          backgroundColor="rgba(6, 32, 44, 0.45)"
          borderColor="rgba(6, 182, 212, 0.35)"
          buttonColor="#06b6d4"
          buttonTextColor="#080C14"
          textColor="#F8FAFC"
          placeholderColor="#64748B"
          fontSize={14}
          cornerRadius={14}
          borderWidth={1.5}
          showIcon={true}
          icon={
            <g>
              <rect x={-15} y={-10} width={30} height={20} rx={4} fill="#0F172A" stroke="#1E293B" strokeWidth={1} />
              <text x={0} y={4} textAnchor="middle" fill="#38BDF8" fontSize={9} fontWeight={700} fontFamily="monospace">
                URI
              </text>
            </g>
          }
        />
      </div>

      {/* 4. Live Inference Result Card (Rendered on Scan) */}
      {verdict && (
        <SpotlightCard
          theme="dark"
          shape="beam"
          spotlightColor={isPhishing ? '#EF4444' : '#06b6d4'}
          intensity={0.45}
          spotlightSize={350}
          softness={0.6}
          borderGlow={0.6}
          proximity={120}
          smoothing={0.4}
          grain={0.15}
          ambient={true}
          flare={true}
          className="max-w-2xl mx-auto mb-10 text-left transition-all duration-300"
          style={{
            backgroundColor: 'rgba(6, 32, 44, 0.40)',
            backdropFilter: 'blur(16px)',
            WebkitBackdropFilter: 'blur(16px)',
            padding: '1.5rem',
            borderRadius: '1.25rem',
          }}
        >
          {/* Header Row */}
          <div className={`flex items-center justify-between border-b ${isPhishing ? 'border-[#EF4444]/20' : 'border-[#06B6D4]/20'} pb-3.5 mb-3.5`}>
            <div className="flex items-center gap-2.5">
              {isPhishing ? (
                <ShieldAlert className="w-5 h-5 text-[#EF4444]" />
              ) : (
                <CheckCircle2 className="w-5 h-5 text-[#00E676]" />
              )}
              <span
                className={`px-2.5 py-0.5 rounded text-xs font-mono font-bold uppercase tracking-wider ${
                  isPhishing
                    ? 'bg-[#EF4444]/15 text-[#EF4444] border border-[#EF4444]/30'
                    : 'bg-[#00E676]/15 text-[#00E676] border border-[#00E676]/30'
                }`}
              >
                {isPhishing ? 'CRITICAL THREAT — PHISHING' : 'VERIFIED LEGITIMATE'}
              </span>
            </div>

            <span className="text-xs font-mono text-[#06B6D4]">
              Confidence: <strong className="text-[#F8FAFC]">{Math.round((verdict.confidence || 0.9998) * 100)}%</strong>
            </span>
          </div>

          {/* Inspected URL Box */}
          <div className={`text-xs font-mono text-[#94A3B8] truncate mb-3.5 bg-[#06111C]/80 px-3.5 py-2 rounded-lg border ${isPhishing ? 'border-[#EF4444]/25' : 'border-[#06B6D4]/25'} shadow-inner flex items-center`}>
            <span className="text-[#64748B] mr-2">Inspected:</span>
            <span className="text-[#F8FAFC] font-medium selection:bg-[#06B6D4]/30">{verdict.targetUrl}</span>
          </div>

          {/* Footer Metadata */}
          <div className="flex flex-wrap justify-between items-center text-xs font-ui gap-2 pt-0.5">
            <span className="text-[#94A3B8] font-mono text-[11px]">
              Latency: <span className="text-[#F8FAFC]">{verdict.clientLatency}</span> • 16 Engineered Features Parsed
            </span>
            <span className="text-[11px] font-mono text-[#06B6D4] border border-[#06B6D4]/30 px-2.5 py-1 rounded bg-[#06B6D4]/5 flex items-center gap-1.5">
              <span>XGBoost Champion Model</span>
            </span>
          </div>
        </SpotlightCard>
      )}

      {/* Error Message */}
      {errorMsg && (
        <div className="max-w-2xl mx-auto bg-amber-950/20 border border-amber-900/40 rounded-lg p-3.5 text-xs text-amber-200/90 font-mono mb-10 text-left flex items-start gap-2.5">
          <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <span>{errorMsg}</span>
        </div>
      )}

    </section>
  );
};

export default HeroSection;
