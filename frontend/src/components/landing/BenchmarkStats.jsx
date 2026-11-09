import React from 'react';
import { AlertTriangle } from 'lucide-react';
import SpotlightCard from '../common/SpotlightCard';

export const BenchmarkStats = () => {
  return (
    <section id="evaluation" className="relative z-10 py-12 px-4 max-w-5xl mx-auto">
      <SpotlightCard
        theme="dark"
        spotlightColor="#06b6d4"
        intensity={0.45}
        spotlightSize={350}
        softness={0.6}
        shape="beam"
        borderGlow={0.6}
        proximity={120}
        smoothing={0.4}
        grain={0.15}
        ambient={true}
        flare={true}
        className="transition-all duration-300"
      >
        {/* Header Row */}
        <div className="flex flex-wrap justify-between items-start gap-4 mb-8">
          <div>
            <div className="text-[#06B6D4] text-xs font-mono font-bold uppercase tracking-wider mb-1">
              RECORDED MODEL RESULTS
            </div>
            <h3 className="font-display text-2xl font-bold text-[#F8FAFC]">
              Evaluation, not marketing claims.
            </h3>
            <p className="font-ui text-xs text-[#94A3B8] mt-1">
              Selected XGBoost model - LegitPhish held-out test split
            </p>
          </div>

          <div className="text-[11px] font-mono text-[#94A3B8] border border-[#06B6D4]/30 px-3 py-1 rounded bg-[#06B6D4]/5">
            100,872 CLEANED URL RECORDS
          </div>
        </div>

        {/* 4 Core Verification Metric Columns */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 pb-8 border-b border-[#06B6D4]/20">
          
          {/* Metric 1 */}
          <div>
            <div className="font-display text-3xl font-extrabold text-[#06B6D4] mb-1">
              99.9868%
            </div>
            <div className="text-xs font-ui font-bold text-white mb-0.5">
              Accuracy
            </div>
            <div className="text-[11px] font-ui text-[#94A3B8]">
              15,131 held-out test records
            </div>
          </div>

          {/* Metric 2 */}
          <div>
            <div className="font-display text-3xl font-extrabold text-[#F8FAFC] mb-1">
              99.9895%
            </div>
            <div className="text-xs font-ui font-bold text-white mb-0.5">
              Phishing F1-score
            </div>
            <div className="text-[11px] font-ui text-[#94A3B8]">
              Precision and recall reported at the same value
            </div>
          </div>

          {/* Metric 3 */}
          <div>
            <div className="font-display text-3xl font-extrabold text-[#F8FAFC] mb-1">
              0.9999995
            </div>
            <div className="text-xs font-ui font-bold text-white mb-0.5">
              ROC-AUC
            </div>
            <div className="text-[11px] font-ui text-[#94A3B8]">
              Reported held-out test result
            </div>
          </div>

          {/* Metric 4 */}
          <div>
            <div className="font-display text-3xl font-extrabold text-[#F8FAFC] mb-1">
              15,131
            </div>
            <div className="text-xs font-ui font-bold text-white mb-0.5">
              Test records
            </div>
            <div className="text-[11px] font-ui text-[#94A3B8]">
              Separate from the training and validation sets
            </div>
          </div>

        </div>

        {/* Confusion Matrix Row */}
        <div className="py-4 border-b border-[#06B6D4]/20 flex flex-wrap items-center gap-x-6 gap-y-2 text-xs font-mono">
          <span className="font-bold text-white">Confusion matrix:</span>
          <span className="text-[#94A3B8]">
            True negatives: <strong className="text-white">5,606</strong>
          </span>
          <span className="text-[#64748B] hidden sm:inline">|</span>
          <span className="text-[#94A3B8]">
            False positives: <strong className="text-white">1</strong>
          </span>
          <span className="text-[#64748B] hidden sm:inline">|</span>
          <span className="text-[#94A3B8]">
            False negatives: <strong className="text-white">1</strong>
          </span>
          <span className="text-[#64748B] hidden sm:inline">|</span>
          <span className="text-[#94A3B8]">
            True positives: <strong className="text-white">9,523</strong>
          </span>
        </div>

        {/* Validation Note Strip */}
        <div className="mt-6 border border-amber-900/40 bg-amber-950/20 rounded-lg p-4 text-xs font-ui text-amber-200/90 leading-relaxed flex items-start gap-3">
          <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <span>
            <strong>Validation note.</strong> The technical report does not confirm that the final split was strictly grouped by registrable domain. These figures describe the reported held-out dataset; they should not be presented as proof of generalisation to unseen domains. The independent PhiUSIIL figures in the README still require reconciliation with the evaluation report.
          </span>
        </div>

      </SpotlightCard>
    </section>
  );
};

export default BenchmarkStats;
