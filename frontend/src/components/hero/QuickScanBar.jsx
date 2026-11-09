import React, { useState } from 'react';
import { Search, ArrowRight, AlertTriangle, CheckCircle2, ShieldAlert, Clock, Sparkles, Lock, ShieldCheck } from 'lucide-react';
import StarBorder from '../common/StarBorder';
import { scanUrl } from '../../services/api';

export const QuickScanBar = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const sampleLegit = 'https://www.google.com/';
  const samplePhish = 'https://keraekken-loagginnusa.godaddysites.com/';

  const handleScan = async (overrideUrl) => {
    const targetUrl = (overrideUrl !== undefined ? overrideUrl : url).trim();
    if (!targetUrl) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await scanUrl(targetUrl);
      setResult(data);
    } catch (err) {
      setError(err.message || 'FastAPI backend unreachable on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  const handleSampleClick = (sample) => {
    setUrl(sample);
    handleScan(sample);
  };

  // Determine risk level color scheme
  const isPhishing =
    result?.ml_threat_detection?.prediction?.toLowerCase() === 'phishing' ||
    result?.prediction?.toLowerCase() === 'phishing' ||
    result?.label === 1 ||
    result?.verdict === 'DANGEROUS';

  const riskColorClass = isPhishing
    ? 'text-[#FF3B3B] bg-[#FF3B3B]/10 border-[#FF3B3B]/30'
    : 'text-[#00E676] bg-[#00E676]/10 border-[#00E676]/30';

  return (
    <div className="w-full max-w-2xl mx-auto space-y-3.5">
      
      {/* Primary URL Input Bar */}
      <div className="relative flex items-center bg-[#060D1A]/90 border border-[#1E3357] rounded-xl p-1.5 focus-within:border-[#00E5FF] focus-within:shadow-cyan-glow transition-all">
        <div className="pl-3.5 pr-2 text-[#8E9EB5]">
          <Search className="w-5 h-5 text-[#00E5FF]" />
        </div>

        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleScan()}
          placeholder="Enter target URL (e.g. https://domain.com/path)"
          className="w-full bg-transparent text-white font-jetbrains text-sm focus:outline-none placeholder:text-[#8E9EB5]/50 py-2.5 px-1"
        />

        <StarBorder
          as="button"
          type="button"
          onClick={() => handleScan()}
          disabled={loading || !url.trim()}
          color="#06B6D4"
          trailColor="#06B6D4"
          duration={4}
          stars={2}
          trailLength={0.35}
          thickness={1.5}
          radius={8}
          glow={0.6}
          sparkle={true}
          clickPulse={true}
          theme="dark"
          backgroundColor="#06B6D4"
          textColor="#060D1A"
          borderColor="rgba(6, 182, 212, 0.4)"
          className="flex items-center gap-2 font-rajdhani font-bold text-sm tracking-wider uppercase !px-5 !py-2.5 rounded-lg transition-all disabled:opacity-40 shrink-0 shadow-[0_0_16px_rgba(6,182,212,0.35)] cursor-pointer"
        >
          {loading ? (
            <>
              <span className="w-4 h-4 border-2 border-[#060D1A] border-t-transparent rounded-full animate-spin"></span>
              <span>Scanning…</span>
            </>
          ) : (
            <>
              <span>Analyze Threat</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </StarBorder>
      </div>

      {/* Quick-Test Interactive Sample Pills */}
      <div className="flex flex-wrap items-center justify-between text-xs font-jetbrains px-1 gap-2 text-[#8E9EB5]">
        <div className="flex items-center gap-2">
          <span className="font-medium text-[#8E9EB5]/80">Quick Test:</span>
          <StarBorder
            as="button"
            type="button"
            onClick={() => handleSampleClick(sampleLegit)}
            color="#00E676"
            trailColor="#00E676"
            duration={5.5}
            stars={2}
            trailLength={0.3}
            thickness={1.5}
            radius={6}
            glow={0.5}
            sparkle={true}
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
            color="#FF3B3B"
            trailColor="#FF3B3B"
            duration={5}
            stars={2}
            trailLength={0.3}
            thickness={1.5}
            radius={6}
            glow={0.6}
            sparkle={true}
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
        <span className="text-[11px] text-[#8E9EB5]/60 font-jakarta">Real FastAPI endpoint</span>
      </div>

      {/* Real Inference Output Card (Slide down on prediction) */}
      {result && (
        <div className="p-4 sm:p-5 rounded-xl bg-[#0C1A2E]/95 border border-[#1E3357] shadow-xl backdrop-blur-md animate-in fade-in slide-in-from-top-3 duration-300">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-3 border-b border-[#1E3357]/60">
            
            {/* Prediction Verdict Badge */}
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-lg border ${riskColorClass}`}>
                {isPhishing ? (
                  <ShieldAlert className="w-6 h-6 text-[#FF3B3B]" />
                ) : (
                  <CheckCircle2 className="w-6 h-6 text-[#00E676]" />
                )}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span
                    className={`font-rajdhani font-bold text-lg tracking-wider uppercase px-2.5 py-0.5 rounded ${
                      isPhishing ? 'bg-[#FF3B3B]/20 text-[#FF3B3B]' : 'bg-[#00E676]/20 text-[#00E676]'
                    }`}
                  >
                    {result.verdict || result.prediction || (isPhishing ? 'DANGEROUS' : 'TRUSTED')}
                  </span>
                  <span className="text-xs font-jetbrains px-2 py-0.5 rounded bg-[#162440] text-[#00E5FF] border border-[#1E3357]">
                    Risk: {result.risk_level || (isPhishing ? 'CRITICAL' : 'LOW')}
                  </span>
                </div>
                <p className="text-xs font-jetbrains text-[#8E9EB5] truncate max-w-sm mt-1">
                  {result.url || url}
                </p>
              </div>
            </div>

            {/* Trust Score & Latency */}
            <div className="flex items-center gap-5 sm:text-right">
              <div>
                <p className="text-[10px] font-jetbrains text-[#8E9EB5] uppercase">Trust Score</p>
                <p className="font-jetbrains font-bold text-2xl text-[#00E5FF]">
                  {result.trust_score !== undefined ? `${Math.round(result.trust_score)}/100` : `${(result.confidence * 100).toFixed(0)}%`}
                </p>
              </div>

              <div className="border-l border-[#1E3357] pl-4">
                <p className="text-[10px] font-jetbrains text-[#8E9EB5] uppercase flex items-center gap-1 sm:justify-end">
                  <Clock className="w-3 h-3 text-[#8E9EB5]" />
                  <span>Latency</span>
                </p>
                <p className="font-jetbrains font-medium text-sm text-[#CBD5E1]">
                  {result.clientLatency || `${result.scan_time_ms} ms`}
                </p>
              </div>
            </div>

          </div>

          {/* Action Row */}
          <div className="pt-3 flex items-center justify-between text-xs font-jetbrains">
            <span className="text-[#8E9EB5] flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-[#00E5FF]" />
              <span>Full Trust Engine: XGBoost + SSL/TLS + Security Headers</span>
            </span>
            <a
              href="#scanner"
              className="font-rajdhani font-bold text-[#00E5FF] hover:text-[#22D3EE] uppercase tracking-wider flex items-center gap-1 hover:underline"
            >
              <span>Inspect Full Assessment</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      )}

      {/* Fallback Banner if FastAPI is offline */}
      {error && (
        <div className="p-3.5 rounded-xl bg-red-950/40 border border-red-800/70 text-red-300 text-xs font-jetbrains flex items-start gap-3">
          <AlertTriangle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <p className="font-bold">FastAPI Connection Offline</p>
            <p className="text-red-300/80 leading-relaxed font-jakarta">{error}</p>
          </div>
        </div>
      )}

    </div>
  );
};

export default QuickScanBar;
