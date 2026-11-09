import React, { useState } from 'react';
import { ArrowRight, AlertTriangle, CheckCircle2, ShieldAlert, Sparkles, Shield, Cpu, RefreshCw } from 'lucide-react';
import RotatingText from '../common/RotatingText';
import CurvedInput from '../common/CurvedInput';
import SpotlightCard from '../common/SpotlightCard';
import StarBorder from '../common/StarBorder';
import FullScanResults from '../scanner/FullScanResults';
import { scanUrl, predictUrl } from '../../services/api';

export const HeroSection = () => {
  const [targetUrl, setTargetUrl] = useState('');
  const [scanMode, setScanMode] = useState('full'); // 'full' (Trust Scan) or 'quick' (ML only)
  const [loading, setLoading] = useState(false);
  const [verdict, setVerdict] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const sampleLegit = 'https://www.google.com/';
  const samplePhish = 'https://keraekken-loagginnusa.godaddysites.com/';

  const executeScan = async (urlOverride, forcedMode) => {
    const finalUrl = (urlOverride !== undefined ? urlOverride : targetUrl).trim();
    if (!finalUrl) return;

    const activeMode = forcedMode || scanMode;

    setLoading(true);
    setErrorMsg(null);
    setVerdict(null);

    try {
      let data;
      if (activeMode === 'full') {
        data = await scanUrl(finalUrl);
      } else {
        data = await predictUrl(finalUrl);
      }

      setVerdict({
        ...data,
        targetUrl: finalUrl,
        mode: activeMode,
      });
    } catch (err) {
      setErrorMsg(err.message || 'An unexpected error occurred during threat scanning.');
    } finally {
      setLoading(false);
    }
  };

  const handleSampleClick = (sample) => {
    setTargetUrl(sample);
    executeScan(sample);
  };

  const isPhishing =
    verdict?.prediction?.toLowerCase() === 'phishing' ||
    verdict?.label === 1 ||
    verdict?.verdict === 'DANGEROUS';

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
      <p className="font-ui text-[#06B6D4] text-sm sm:text-[15px] max-w-2xl mx-auto mb-6 leading-relaxed">
        Inspect suspicious URLs with a 16-feature machine-learning classifier, cryptographic SSL/TLS verification, and HTTP security header audits.
      </p>

      {/* Scan Mode Switcher */}
      <div className="flex items-center justify-center gap-2 mb-8">
        <button
          type="button"
          onClick={() => setScanMode('full')}
          className={`px-3.5 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all flex items-center gap-1.5 border ${
            scanMode === 'full'
              ? 'bg-[#06B6D4]/20 text-[#06B6D4] border-[#06B6D4] shadow-[0_0_12px_rgba(6,182,212,0.25)]'
              : 'bg-[#0C1A2E]/60 text-[#94A3B8] border-[#1E3357] hover:text-[#F8FAFC]'
          }`}
        >
          <Shield className="w-3.5 h-3.5" />
          <span>Full Digital Trust Scan (ML + SSL + Headers)</span>
        </button>

        <button
          type="button"
          onClick={() => setScanMode('quick')}
          className={`px-3.5 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all flex items-center gap-1.5 border ${
            scanMode === 'quick'
              ? 'bg-[#06B6D4]/20 text-[#06B6D4] border-[#06B6D4] shadow-[0_0_12px_rgba(6,182,212,0.25)]'
              : 'bg-[#0C1A2E]/60 text-[#94A3B8] border-[#1E3357] hover:text-[#F8FAFC]'
          }`}
        >
          <Cpu className="w-3.5 h-3.5" />
          <span>Quick ML Only</span>
        </button>
      </div>

      {/* 3. Target URL CurvedInput Command Box */}
      <div className="text-left max-w-2xl mx-auto mb-4">
        <CurvedInput
          topLabel="Target URL"
          bottomLeftText="Enter a complete URL to request live analysis."
          bottomRightText="[Enter] to scan"
          placeholder="https://example.com/login"
          buttonText={loading ? "Analyzing…" : (scanMode === 'full' ? "Full Trust Scan" : "Scan ML Threat")}
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

      {/* Quick-Test Interactive Sample Pills */}
      <div className="flex flex-wrap items-center justify-between text-xs font-mono max-w-2xl mx-auto mb-8 px-2 gap-2 text-[#8E9EB5]">
        <div className="flex items-center gap-2">
          <span className="font-medium text-[#8E9EB5]/80">Quick Test:</span>
          
          <StarBorder
            as="button"
            type="button"
            onClick={() => handleSampleClick(sampleLegit)}
            disabled={loading}
            color="#00E676"
            trailColor="#00E676"
            duration={5}
            stars={2}
            trailLength={0.3}
            thickness={1.5}
            radius={6}
            glow={0.5}
            theme="dark"
            backgroundColor="#0C1A2E"
            textColor="#00E676"
            borderColor="rgba(0, 230, 118, 0.3)"
            className="flex items-center gap-1.5 !px-2.5 !py-1 text-xs cursor-pointer"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-[#00E676]"></span>
            <span>Google (Legitimate)</span>
          </StarBorder>

          <StarBorder
            as="button"
            type="button"
            onClick={() => handleSampleClick(samplePhish)}
            disabled={loading}
            color="#FF3B3B"
            trailColor="#FF3B3B"
            duration={5}
            stars={2}
            trailLength={0.3}
            thickness={1.5}
            radius={6}
            glow={0.5}
            theme="dark"
            backgroundColor="#0C1A2E"
            textColor="#FF3B3B"
            borderColor="rgba(255, 59, 59, 0.3)"
            className="flex items-center gap-1.5 !px-2.5 !py-1 text-xs cursor-pointer"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-[#FF3B3B]"></span>
            <span>Phishing Sample</span>
          </StarBorder>
        </div>

        <span className="text-[11px] text-[#8E9EB5]/60">Real FastAPI unified backend</span>
      </div>

      {/* Loading Spinner Indicator */}
      {loading && (
        <div className="max-w-md mx-auto p-6 bg-[#06111C]/90 border border-[#06B6D4]/30 rounded-2xl shadow-xl flex flex-col items-center justify-center gap-3 animate-pulse">
          <div className="w-8 h-8 border-3 border-[#06B6D4] border-t-transparent rounded-full animate-spin" />
          <p className="text-xs font-mono text-[#06B6D4] font-semibold">
            {scanMode === 'full'
              ? 'Executing Full Scan: ML Inference + SSL/TLS Inspection + Headers Audit…'
              : 'Extracting 16 Lexical Features & Running XGBoost Model…'}
          </p>
        </div>
      )}

      {/* Error Message */}
      {errorMsg && (
        <div className="max-w-2xl mx-auto bg-amber-950/30 border border-amber-900/60 rounded-xl p-4 text-xs text-amber-200/90 font-mono mb-8 text-left flex items-start gap-3 shadow-lg">
          <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <span className="font-bold text-amber-300">Scanner Notice</span>
            <p className="leading-relaxed">{errorMsg}</p>
          </div>
        </div>
      )}

      {/* 4A. Full Digital Trust Results Card (Comprehensive) */}
      {verdict && verdict.trust_score !== undefined && (
        <FullScanResults
          scanData={verdict}
          onScanAgain={() => {
            setVerdict(null);
            setTargetUrl('');
          }}
        />
      )}

      {/* 4B. Quick ML-Only Inference Result Card */}
      {verdict && verdict.trust_score === undefined && (
        <SpotlightCard
          theme="dark"
          shape="beam"
          spotlightColor={isPhishing ? '#EF4444' : '#06b6d4'}
          intensity={0.45}
          spotlightSize={350}
          softness={0.6}
          borderGlow={0.6}
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
              Confidence: <strong className="text-[#F8FAFC]">{Math.round((verdict.confidence || verdict.confidence_score || 0.99) * 100)}%</strong>
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

    </section>
  );
};

export default HeroSection;
