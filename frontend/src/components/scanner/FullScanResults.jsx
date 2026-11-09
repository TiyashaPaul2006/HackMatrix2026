import React, { useState } from 'react';
import {
  ShieldAlert,
  CheckCircle2,
  Lock,
  ShieldCheck,
  AlertTriangle,
  Info,
  Server,
  Key,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  Cpu,
  Layers,
  Sparkles,
  Check,
  X,
  Clock
} from 'lucide-react';
import SpotlightCard from '../common/SpotlightCard';

export const FullScanResults = ({ scanData, onScanAgain }) => {
  const [activeTab, setActiveTab] = useState('ml'); // 'ml', 'ssl', 'headers', 'findings'
  const [showAllShap, setShowAllShap] = useState(false);

  if (!scanData) return null;

  const {
    url,
    trust_score = 0,
    max_score = 100,
    verdict = 'UNKNOWN',
    risk_level = 'UNKNOWN',
    badge_color = 'emerald',
    ml_threat_detection = {},
    ssl_certificate = {},
    security_headers = {},
    score_breakdown = {},
    shap_explanation = [],
    key_findings = [],
    clientLatency,
    scan_time_ms
  } = scanData;

  const isPhishing =
    ml_threat_detection?.prediction?.toLowerCase() === 'phishing' ||
    ml_threat_detection?.label === 1 ||
    verdict === 'DANGEROUS';

  // Badge styling
  const getBadgeStyle = () => {
    switch (badge_color) {
      case 'emerald':
        return 'bg-[#00E676]/15 text-[#00E676] border-[#00E676]/30';
      case 'amber':
        return 'bg-amber-400/15 text-amber-300 border-amber-400/30';
      case 'orange':
        return 'bg-orange-500/15 text-orange-400 border-orange-500/30';
      case 'red':
      default:
        return 'bg-[#FF3B3B]/15 text-[#FF3B3B] border-[#FF3B3B]/30';
    }
  };

  const scorePercentage = Math.min(100, Math.max(0, trust_score));
  const shapFeatures = showAllShap ? shap_explanation : shap_explanation.slice(0, 8);

  return (
    <div className="w-full max-w-4xl mx-auto mt-6 text-left animate-in fade-in slide-in-from-top-4 duration-400">
      <SpotlightCard
        theme="dark"
        shape="beam"
        spotlightColor={isPhishing ? '#EF4444' : '#06B6D4'}
        intensity={0.4}
        spotlightSize={400}
        softness={0.6}
        borderGlow={0.6}
        className="rounded-2xl border border-[#06B6D4]/30 overflow-hidden shadow-2xl"
        style={{
          backgroundColor: 'rgba(6, 17, 28, 0.85)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
        }}
      >
        {/* Top Banner: Composite Trust Score & Status */}
        <div className="p-6 sm:p-7 border-b border-[#1E3357]/80">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            
            {/* Left: Overall Verdict & URL */}
            <div className="space-y-2.5 max-w-xl">
              <div className="flex items-center gap-2.5 flex-wrap">
                <span
                  className={`px-3 py-1 rounded-md text-xs font-mono font-bold uppercase tracking-wider border flex items-center gap-1.5 ${getBadgeStyle()}`}
                >
                  {isPhishing ? (
                    <ShieldAlert className="w-4 h-4 shrink-0" />
                  ) : (
                    <CheckCircle2 className="w-4 h-4 shrink-0" />
                  )}
                  <span>VERDICT: {verdict}</span>
                </span>

                <span className="text-xs font-mono px-2.5 py-0.5 rounded bg-[#0C1A2E] text-[#94A3B8] border border-[#1E3357]">
                  Risk: <strong className={isPhishing ? 'text-[#FF3B3B]' : 'text-[#00E676]'}>{risk_level}</strong>
                </span>

                <span className="text-xs font-mono text-[#06B6D4] flex items-center gap-1 bg-[#06B6D4]/10 px-2 py-0.5 rounded">
                  <Clock className="w-3 h-3" />
                  <span>Latency: {scan_time_ms ? `${scan_time_ms} ms` : clientLatency}</span>
                </span>
              </div>

              <div className="text-xs font-mono text-[#94A3B8] bg-[#030712]/70 px-3.5 py-2 rounded-lg border border-[#1E3357] flex items-center gap-2 overflow-hidden">
                <span className="text-[#64748B] shrink-0">Inspected URL:</span>
                <span className="text-[#F8FAFC] truncate font-medium selection:bg-[#06B6D4]/30">{url}</span>
              </div>
            </div>

            {/* Right: Master Digital Trust Score Gauge */}
            <div className="flex items-center gap-4 shrink-0 bg-[#0C1A2E]/80 border border-[#1E3357] p-4 rounded-xl">
              <div className="relative w-20 h-20 flex items-center justify-center">
                <svg className="w-20 h-20 transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    className="text-[#1E3357]"
                    strokeWidth="3.2"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path
                    className={
                      badge_color === 'emerald'
                        ? 'text-[#00E676]'
                        : badge_color === 'amber'
                        ? 'text-amber-400'
                        : badge_color === 'orange'
                        ? 'text-orange-500'
                        : 'text-[#FF3B3B]'
                    }
                    strokeDasharray={`${scorePercentage}, 100`}
                    strokeWidth="3.2"
                    strokeLinecap="round"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="font-mono font-bold text-xl text-[#F8FAFC]">
                    {Math.round(trust_score)}
                  </span>
                  <span className="text-[9px] font-mono uppercase text-[#94A3B8]">/ 100</span>
                </div>
              </div>

              <div>
                <p className="text-[11px] font-mono text-[#06B6D4] font-semibold uppercase tracking-wider">
                  Digital Trust Score
                </p>
                <p className="text-xs text-[#94A3B8] font-ui mt-0.5">
                  Composite safety index
                </p>
              </div>
            </div>

          </div>

          {/* 4-Pillar Metric Breakdown Bar */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-5 border-t border-[#1E3357]/60">
            <div className="bg-[#030712]/50 p-2.5 rounded-lg border border-[#1E3357]/50">
              <div className="flex items-center justify-between text-[11px] font-mono mb-1">
                <span className="text-[#94A3B8]">1. ML Threat</span>
                <span className="text-[#06B6D4] font-bold">
                  {score_breakdown.ml_threat_points !== undefined ? `${score_breakdown.ml_threat_points}/40` : '—'}
                </span>
              </div>
              <div className="w-full bg-[#162440] h-1.5 rounded-full overflow-hidden">
                <div
                  className="bg-[#06B6D4] h-full rounded-full transition-all duration-500"
                  style={{ width: `${((score_breakdown.ml_threat_points || 0) / 40) * 100}%` }}
                />
              </div>
            </div>

            <div className="bg-[#030712]/50 p-2.5 rounded-lg border border-[#1E3357]/50">
              <div className="flex items-center justify-between text-[11px] font-mono mb-1">
                <span className="text-[#94A3B8]">2. SSL/TLS Cert</span>
                <span className="text-[#00E676] font-bold">
                  {score_breakdown.ssl_certificate_points !== undefined ? `${score_breakdown.ssl_certificate_points}/25` : '—'}
                </span>
              </div>
              <div className="w-full bg-[#162440] h-1.5 rounded-full overflow-hidden">
                <div
                  className="bg-[#00E676] h-full rounded-full transition-all duration-500"
                  style={{ width: `${((score_breakdown.ssl_certificate_points || 0) / 25) * 100}%` }}
                />
              </div>
            </div>

            <div className="bg-[#030712]/50 p-2.5 rounded-lg border border-[#1E3357]/50">
              <div className="flex items-center justify-between text-[11px] font-mono mb-1">
                <span className="text-[#94A3B8]">3. Headers Audit</span>
                <span className="text-amber-400 font-bold">
                  {score_breakdown.security_headers_points !== undefined ? `${score_breakdown.security_headers_points}/20` : '—'}
                </span>
              </div>
              <div className="w-full bg-[#162440] h-1.5 rounded-full overflow-hidden">
                <div
                  className="bg-amber-400 h-full rounded-full transition-all duration-500"
                  style={{ width: `${((score_breakdown.security_headers_points || 0) / 20) * 100}%` }}
                />
              </div>
            </div>

            <div className="bg-[#030712]/50 p-2.5 rounded-lg border border-[#1E3357]/50">
              <div className="flex items-center justify-between text-[11px] font-mono mb-1">
                <span className="text-[#94A3B8]">4. Heuristics</span>
                <span className="text-[#C084FC] font-bold">
                  {score_breakdown.threat_intel_heuristics_points !== undefined ? `${score_breakdown.threat_intel_heuristics_points}/15` : '—'}
                </span>
              </div>
              <div className="w-full bg-[#162440] h-1.5 rounded-full overflow-hidden">
                <div
                  className="bg-[#C084FC] h-full rounded-full transition-all duration-500"
                  style={{ width: `${((score_breakdown.threat_intel_heuristics_points || 0) / 15) * 100}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex items-center border-b border-[#1E3357] px-6 bg-[#080E1A]/80 text-xs font-mono">
          <button
            type="button"
            onClick={() => setActiveTab('ml')}
            className={`py-3 px-4 flex items-center gap-2 border-b-2 font-semibold transition-all ${
              activeTab === 'ml'
                ? 'border-[#06B6D4] text-[#06B6D4]'
                : 'border-transparent text-[#94A3B8] hover:text-[#F8FAFC]'
            }`}
          >
            <Cpu className="w-4 h-4" />
            <span>ML Threat &amp; SHAP</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('ssl')}
            className={`py-3 px-4 flex items-center gap-2 border-b-2 font-semibold transition-all ${
              activeTab === 'ssl'
                ? 'border-[#00E676] text-[#00E676]'
                : 'border-transparent text-[#94A3B8] hover:text-[#F8FAFC]'
            }`}
          >
            <Lock className="w-4 h-4" />
            <span>SSL/TLS Certificate</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('headers')}
            className={`py-3 px-4 flex items-center gap-2 border-b-2 font-semibold transition-all ${
              activeTab === 'headers'
                ? 'border-amber-400 text-amber-400'
                : 'border-transparent text-[#94A3B8] hover:text-[#F8FAFC]'
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span>Security Headers</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('findings')}
            className={`py-3 px-4 flex items-center gap-2 border-b-2 font-semibold transition-all ${
              activeTab === 'findings'
                ? 'border-[#C084FC] text-[#C084FC]'
                : 'border-transparent text-[#94A3B8] hover:text-[#F8FAFC]'
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>Key Findings ({key_findings.length})</span>
          </button>
        </div>

        {/* Tab 1: Machine Learning Threat & SHAP Explainability */}
        {activeTab === 'ml' && (
          <div className="p-6 space-y-6">
            {/* Top ML Verdict Card */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-[#030712]/60 border border-[#1E3357] p-4 rounded-xl">
                <span className="text-[11px] font-mono text-[#94A3B8] uppercase">Classifier Verdict</span>
                <p className={`text-xl font-mono font-bold mt-1 ${isPhishing ? 'text-[#FF3B3B]' : 'text-[#00E676]'}`}>
                  {ml_threat_detection.prediction || 'Unknown'}
                </p>
                <p className="text-xs text-[#64748B] mt-1 font-ui">XGBoost 16-feature champion</p>
              </div>

              <div className="bg-[#030712]/60 border border-[#1E3357] p-4 rounded-xl">
                <span className="text-[11px] font-mono text-[#94A3B8] uppercase">Phishing Probability</span>
                <p className="text-xl font-mono font-bold text-[#F8FAFC] mt-1">
                  {((ml_threat_detection.phishing_probability || 0) * 100).toFixed(1)}%
                </p>
                <div className="w-full bg-[#162440] h-1.5 rounded-full overflow-hidden mt-2">
                  <div
                    className="bg-[#FF3B3B] h-full rounded-full"
                    style={{ width: `${(ml_threat_detection.phishing_probability || 0) * 100}%` }}
                  />
                </div>
              </div>

              <div className="bg-[#030712]/60 border border-[#1E3357] p-4 rounded-xl">
                <span className="text-[11px] font-mono text-[#94A3B8] uppercase">Legitimate Probability</span>
                <p className="text-xl font-mono font-bold text-[#00E676] mt-1">
                  {((ml_threat_detection.legitimate_probability || 0) * 100).toFixed(1)}%
                </p>
                <div className="w-full bg-[#162440] h-1.5 rounded-full overflow-hidden mt-2">
                  <div
                    className="bg-[#00E676] h-full rounded-full"
                    style={{ width: `${(ml_threat_detection.legitimate_probability || 0) * 100}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Heuristic Risk Factors */}
            {ml_threat_detection.detected_risk_factors && ml_threat_detection.detected_risk_factors.length > 0 && (
              <div className="bg-red-950/20 border border-red-900/40 rounded-xl p-4">
                <div className="flex items-center gap-2 text-xs font-mono font-bold text-[#FF3B3B] mb-2 uppercase">
                  <AlertTriangle className="w-4 h-4 text-[#FF3B3B]" />
                  <span>Detected Threat Indicators ({ml_threat_detection.detected_risk_factors.length})</span>
                </div>
                <ul className="space-y-1.5 text-xs font-ui text-red-200/90 pl-6 list-disc">
                  {ml_threat_detection.detected_risk_factors.map((item, idx) => (
                    <li key={idx} className="leading-relaxed">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Real-Time SHAP Waterfall / Local Feature Attributions */}
            <div className="border border-[#1E3357] rounded-xl p-5 bg-[#030712]/40">
              <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
                <div>
                  <h4 className="text-xs font-mono font-bold text-[#06B6D4] uppercase tracking-wider flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-[#06B6D4]" />
                    <span>Explainable AI — SHAP Local Feature Attributions</span>
                  </h4>
                  <p className="text-xs text-[#94A3B8] font-ui mt-0.5">
                    TreeExplainer marginal attribution showing which URL characteristics pushed this prediction.
                  </p>
                </div>

                <div className="flex items-center gap-3 text-[11px] font-mono">
                  <span className="flex items-center gap-1 text-[#FF3B3B]">
                    <span className="w-2 h-2 rounded-full bg-[#FF3B3B]" />
                    <span>Pushes Phishing</span>
                  </span>
                  <span className="flex items-center gap-1 text-[#00E676]">
                    <span className="w-2 h-2 rounded-full bg-[#00E676]" />
                    <span>Pushes Legitimate</span>
                  </span>
                </div>
              </div>

              {shap_explanation && shap_explanation.length > 0 ? (
                <div className="space-y-2.5">
                  {shapFeatures.map((feat, idx) => {
                    const isPhishPush = feat.shap_value > 0;
                    const maxMag = shap_explanation[0]?.magnitude || 1.0;
                    const barWidth = Math.min(100, Math.max(10, (feat.magnitude / maxMag) * 100));

                    return (
                      <div
                        key={idx}
                        className="bg-[#0C1A2E]/60 border border-[#1E3357]/60 rounded-lg p-2.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs font-mono"
                      >
                        <div className="flex items-center gap-2 min-w-[200px]">
                          <span className="text-[#F8FAFC] font-semibold">{feat.feature}</span>
                          <span className="text-[11px] text-[#64748B]">
                            (val: <strong className="text-[#94A3B8]">{feat.value}</strong>)
                          </span>
                        </div>

                        <div className="flex items-center gap-3 w-full sm:w-1/2">
                          <div className="w-full bg-[#162440] h-2 rounded-full overflow-hidden flex">
                            {isPhishPush ? (
                              <div
                                className="bg-[#FF3B3B] h-full rounded-full transition-all"
                                style={{ width: `${barWidth}%` }}
                              />
                            ) : (
                              <div
                                className="bg-[#00E676] h-full rounded-full transition-all"
                                style={{ width: `${barWidth}%` }}
                              />
                            )}
                          </div>
                          <span
                            className={`font-bold text-xs shrink-0 min-w-[55px] text-right ${
                              isPhishPush ? 'text-[#FF3B3B]' : 'text-[#00E676]'
                            }`}
                          >
                            {isPhishPush ? `+${feat.shap_value}` : `${feat.shap_value}`}
                          </span>
                        </div>
                      </div>
                    );
                  })}

                  {shap_explanation.length > 8 && (
                    <button
                      type="button"
                      onClick={() => setShowAllShap(!showAllShap)}
                      className="mt-3 text-xs font-mono text-[#06B6D4] hover:underline flex items-center gap-1 mx-auto"
                    >
                      <span>{showAllShap ? 'Show top 8 features' : `Show all ${shap_explanation.length} features`}</span>
                      {showAllShap ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                    </button>
                  )}
                </div>
              ) : (
                <p className="text-xs text-[#94A3B8] font-mono italic">
                  SHAP feature attributions loaded from XGBoost model metadata.
                </p>
              )}
            </div>
          </div>
        )}

        {/* Tab 2: SSL/TLS Certificate Validation */}
        {activeTab === 'ssl' && (
          <div className="p-6 space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-[#030712]/60 border border-[#1E3357] p-4 rounded-xl">
                <span className="text-[11px] font-mono text-[#94A3B8] uppercase">Certificate Status</span>
                <p
                  className={`text-lg font-mono font-bold mt-1 ${
                    ssl_certificate.status === 'VALID' ? 'text-[#00E676]' : 'text-[#FF3B3B]'
                  }`}
                >
                  {ssl_certificate.status || 'UNAVAILABLE'}
                </p>
                <p className="text-xs text-[#64748B] mt-1 font-ui">
                  Trust Points: {ssl_certificate.trust_points !== undefined ? `${ssl_certificate.trust_points} / 25` : '—'}
                </p>
              </div>

              <div className="bg-[#030712]/60 border border-[#1E3357] p-4 rounded-xl">
                <span className="text-[11px] font-mono text-[#94A3B8] uppercase">Protocol Version</span>
                <p className="text-lg font-mono font-bold text-[#06B6D4] mt-1">
                  {ssl_certificate.tls_version || ssl_certificate.protocol_version || 'TLS / HTTPS'}
                </p>
                <p className="text-xs text-[#64748B] mt-1 font-ui">
                  Cipher: {ssl_certificate.cipher_suite ? ssl_certificate.cipher_suite.substring(0, 18) + '…' : 'Negotiated'}
                </p>
              </div>

              <div className="bg-[#030712]/60 border border-[#1E3357] p-4 rounded-xl">
                <span className="text-[11px] font-mono text-[#94A3B8] uppercase">Remaining Validity</span>
                <p className="text-lg font-mono font-bold text-[#F8FAFC] mt-1">
                  {ssl_certificate.days_until_expiry !== undefined ? `${ssl_certificate.days_until_expiry} days` : 'N/A'}
                </p>
                <p className="text-xs text-[#64748B] mt-1 font-ui">
                  {ssl_certificate.days_until_expiry > 30 ? 'Active & Healthy' : 'Expiring Soon or Expired'}
                </p>
              </div>
            </div>

            {/* Issuer & Subject Details */}
            <div className="bg-[#030712]/40 border border-[#1E3357] rounded-xl p-5 space-y-3 text-xs font-mono">
              <div className="flex flex-col sm:flex-row justify-between py-1 border-b border-[#1E3357]/60">
                <span className="text-[#94A3B8]">Issuer Organization:</span>
                <span className="text-[#F8FAFC] font-semibold">{ssl_certificate.issuer || 'N/A'}</span>
              </div>
              <div className="flex flex-col sm:flex-row justify-between py-1 border-b border-[#1E3357]/60">
                <span className="text-[#94A3B8]">Subject / Common Name:</span>
                <span className="text-[#F8FAFC] font-semibold">{ssl_certificate.subject || 'N/A'}</span>
              </div>
              <div className="flex flex-col sm:flex-row justify-between py-1 border-b border-[#1E3357]/60">
                <span className="text-[#94A3B8]">Valid From:</span>
                <span className="text-[#94A3B8]">{ssl_certificate.valid_from || 'N/A'}</span>
              </div>
              <div className="flex flex-col sm:flex-row justify-between py-1 border-b border-[#1E3357]/60">
                <span className="text-[#94A3B8]">Valid Until:</span>
                <span className="text-[#94A3B8]">{ssl_certificate.valid_until || 'N/A'}</span>
              </div>
              <div className="flex flex-col sm:flex-row justify-between py-1">
                <span className="text-[#94A3B8]">Hostname Match:</span>
                <span className={ssl_certificate.hostname_matched ? 'text-[#00E676]' : 'text-[#FF3B3B]'}>
                  {ssl_certificate.hostname_matched ? 'Verified Match' : 'Mismatch / Not Verified'}
                </span>
              </div>
            </div>

            {/* SANs (Subject Alternative Names) */}
            {ssl_certificate.subject_alternative_names && ssl_certificate.subject_alternative_names.length > 0 && (
              <div className="border border-[#1E3357] rounded-xl p-4 bg-[#030712]/30">
                <span className="text-xs font-mono text-[#06B6D4] uppercase font-semibold block mb-2">
                  Subject Alternative Names (SANs)
                </span>
                <div className="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto">
                  {ssl_certificate.subject_alternative_names.slice(0, 15).map((san, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 rounded text-[11px] font-mono bg-[#0C1A2E] text-[#94A3B8] border border-[#1E3357]"
                    >
                      {san}
                    </span>
                  ))}
                  {ssl_certificate.subject_alternative_names.length > 15 && (
                    <span className="text-[11px] font-mono text-[#64748B] self-center">
                      +{ssl_certificate.subject_alternative_names.length - 15} more
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 3: Security Headers Audit */}
        {activeTab === 'headers' && (
          <div className="p-6 space-y-6">
            <div className="flex items-center justify-between border-b border-[#1E3357] pb-4">
              <div>
                <h4 className="font-mono text-sm font-bold text-amber-400 uppercase">
                  HTTP Security Headers Posture
                </h4>
                <p className="text-xs text-[#94A3B8] font-ui mt-0.5">
                  Passive audit of defensive headers (HSTS, CSP, X-Frame-Options, X-Content-Type)
                </p>
              </div>
              <div className="text-right">
                <span className="font-mono text-2xl font-bold text-amber-400">
                  {security_headers.security_header_score !== undefined
                    ? security_headers.security_header_score
                    : 0}
                </span>
                <span className="text-xs font-mono text-[#94A3B8]"> / 20 pts</span>
              </div>
            </div>

            {/* Present Headers */}
            <div className="space-y-3">
              <span className="text-xs font-mono text-[#00E676] font-semibold uppercase tracking-wider block">
                Implemented Defensive Headers ({security_headers.present_headers?.length || 0})
              </span>
              {security_headers.present_headers && security_headers.present_headers.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {security_headers.present_headers.map((hdr, idx) => (
                    <div
                      key={idx}
                      className="bg-[#030712]/50 border border-[#00E676]/30 rounded-lg p-3 text-xs font-mono"
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-[#00E676] font-bold flex items-center gap-1.5">
                          <Check className="w-3.5 h-3.5" />
                          <span>{hdr.header || hdr.name}</span>
                        </span>
                        <span className="text-[10px] px-1.5 py-0.2 rounded bg-[#00E676]/15 text-[#00E676]">
                          PASS
                        </span>
                      </div>
                      <p className="text-[11px] text-[#94A3B8] truncate">{hdr.value || 'Active'}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs font-mono text-[#64748B] italic">No standard security headers detected.</p>
              )}
            </div>

            {/* Missing Headers */}
            <div className="space-y-3 pt-3 border-t border-[#1E3357]/60">
              <span className="text-xs font-mono text-[#FF3B3B] font-semibold uppercase tracking-wider block">
                Missing Defensive Headers ({security_headers.missing_headers?.length || 0})
              </span>
              {security_headers.missing_headers && security_headers.missing_headers.length > 0 ? (
                <div className="space-y-2">
                  {security_headers.missing_headers.map((hdr, idx) => {
                    const headerName = typeof hdr === 'string' ? hdr : hdr.header || hdr.name;
                    const importance = typeof hdr === 'object' ? hdr.importance : 'Recommended';
                    const description = typeof hdr === 'object' ? hdr.description : '';

                    return (
                      <div
                        key={idx}
                        className="bg-[#030712]/40 border border-[#1E3357] rounded-lg p-3 text-xs font-ui flex items-start justify-between gap-3"
                      >
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-mono font-bold text-[#F8FAFC]">{headerName}</span>
                            <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-amber-500/15 text-amber-300 border border-amber-500/30">
                              {importance} Priority
                            </span>
                          </div>
                          {description && <p className="text-[11px] text-[#94A3B8] mt-1">{description}</p>}
                        </div>
                        <X className="w-4 h-4 text-[#FF3B3B] shrink-0 mt-0.5" />
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="text-xs font-mono text-[#00E676]">All core security headers are active!</p>
              )}
            </div>
          </div>
        )}

        {/* Tab 4: Executive Key Findings */}
        {activeTab === 'findings' && (
          <div className="p-6 space-y-4">
            <h4 className="font-mono text-sm font-bold text-[#C084FC] uppercase">
              Consolidated Threat Intelligence Summary
            </h4>
            <div className="space-y-2.5">
              {key_findings && key_findings.length > 0 ? (
                key_findings.map((item, idx) => (
                  <div
                    key={idx}
                    className="p-3.5 rounded-xl bg-[#030712]/50 border border-[#1E3357] flex items-start gap-3 text-xs font-ui text-[#CBD5E1]"
                  >
                    <Info className="w-4 h-4 text-[#06B6D4] shrink-0 mt-0.5" />
                    <span className="leading-relaxed">{item}</span>
                  </div>
                ))
              ) : (
                <p className="text-xs font-mono text-[#94A3B8]">No critical flags detected.</p>
              )}
            </div>
          </div>
        )}

        {/* Footer Bar */}
        <div className="p-4 bg-[#030712]/80 border-t border-[#1E3357] flex flex-wrap items-center justify-between text-xs font-mono text-[#94A3B8] gap-3">
          <span>Engine: XGBoost Champion • SSL Validator • Security Headers Auditor</span>
          {onScanAgain && (
            <button
              type="button"
              onClick={onScanAgain}
              className="text-[#06B6D4] hover:text-[#22D3EE] font-bold uppercase transition-colors"
            >
              Scan Another URL →
            </button>
          )}
        </div>
      </SpotlightCard>
    </div>
  );
};

export default FullScanResults;

