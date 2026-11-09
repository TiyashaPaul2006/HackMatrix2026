import React from 'react';
import { ShieldCheck, ArrowDownCircle, Lock } from 'lucide-react';
import GradientText from '../common/GradientText';
import HoloCard from '../common/HoloCard';

export const ArchitecturalPillars = () => {
  return (
    <section id="pipeline" className="relative z-10 py-16 px-4 max-w-5xl mx-auto">
      {/* Section Header */}
      <div className="text-center mb-12">
        <h2
          style={{ fontFamily: "'Kelly Slab', serif" }}
          className="font-kelly text-2xl sm:text-3xl text-[#F8FAFC] tracking-wide mb-3"
        >
          <GradientText
            colors={["#06b6d4", "#ffffff", "#06b6d4", "#ffffff"]}
            animationSpeed={5}
            variant="flow"
            glow={0.3}
          >
            Three parts of a website assessment
          </GradientText>
        </h2>
        <p className="font-ui text-xs sm:text-sm text-[#06B6D4] max-w-xl mx-auto leading-relaxed">
          The current system classifies URL structure and supports model explainability. Certificate and header checks are separate assessment modules being integrated.
        </p>
      </div>

      {/* 3-Card Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Card 1: 01 / CLASSIFY */}
        <HoloCard
          width="100%"
          aspectRatio={0.82}
          preset="shards"
          foilColor="#06b6d4"
          cardBorderColor="rgba(6, 182, 212, 0.35)"
          intensity={0.35}
          scale={1.2}
          edgeSparkle={0.35}
          frame={2.5}
          glare={0.2}
          radius={16}
          tiltMax={14}
          hoverScale={1.04}
        >
          <div className="flex flex-col justify-between h-full">
            <div>
              <div className="text-xs font-mono font-semibold tracking-wider text-[#06B6D4] mb-4 drop-shadow-[0_1px_3px_rgba(0,0,0,0.9)]">
                01 / CLASSIFY
              </div>
              
              <div className="w-9 h-9 rounded-lg border border-[#06B6D4]/50 bg-[#06111C]/90 backdrop-blur-md flex items-center justify-center text-[#06B6D4] mb-4 shadow-[0_2px_8px_rgba(0,0,0,0.7)]">
                <ShieldCheck className="w-5 h-5 text-[#06B6D4]" />
              </div>

              <h3 className="font-display text-lg font-bold text-[#22D3EE] mb-2 drop-shadow-[0_2px_6px_rgba(0,0,0,0.9)]">
                URL threat engine
              </h3>

              <p className="font-ui text-xs text-[#A5F3FC] leading-relaxed mb-6 font-normal drop-shadow-[0_1px_4px_rgba(0,0,0,0.9)]">
                Sixteen lexical and structural features feed the selected XGBoost classifier to distinguish legitimate URLs from phishing attempts.
              </p>
            </div>

            <div className="pt-4 border-t border-[#06B6D4]/30 text-[10px] font-mono font-medium text-[#38BDF8] uppercase tracking-wider drop-shadow-[0_1px_3px_rgba(0,0,0,0.9)]">
              INPUT URL structure • OUTPUT class probabilities
            </div>
          </div>
        </HoloCard>

        {/* Card 2: 02 / EXPLAIN */}
        <HoloCard
          width="100%"
          aspectRatio={0.82}
          preset="cosmos"
          foilColor="#818cf8"
          cardBorderColor="rgba(129, 140, 248, 0.35)"
          intensity={0.35}
          scale={1.2}
          edgeSparkle={0.35}
          frame={2.5}
          glare={0.2}
          radius={16}
          tiltMax={14}
          hoverScale={1.04}
        >
          <div className="flex flex-col justify-between h-full">
            <div>
              <div className="text-xs font-mono font-semibold tracking-wider text-[#818CF8] mb-4 drop-shadow-[0_1px_3px_rgba(0,0,0,0.9)]">
                02 / EXPLAIN
              </div>

              <div className="w-9 h-9 rounded-lg border border-[#818CF8]/50 bg-[#06111C]/90 backdrop-blur-md flex items-center justify-center text-[#818CF8] mb-4 shadow-[0_2px_8px_rgba(0,0,0,0.7)]">
                <ArrowDownCircle className="w-5 h-5 text-[#818CF8]" />
              </div>

              <h3 className="font-display text-lg font-bold text-[#A5B4FC] mb-2 drop-shadow-[0_2px_6px_rgba(0,0,0,0.9)]">
                Model explainability
              </h3>

              <p className="font-ui text-xs text-[#C7D2FE] leading-relaxed mb-6 font-normal drop-shadow-[0_1px_4px_rgba(0,0,0,0.9)]">
                SHAP TreeExplainer attributes model output to extracted features, helping analysts inspect which URL characteristics influenced a prediction.
              </p>
            </div>

            <div className="pt-4 border-t border-[#818CF8]/30 text-[10px] font-mono font-medium text-[#818CF8] uppercase tracking-wider drop-shadow-[0_1px_3px_rgba(0,0,0,0.9)]">
              METHOD SHAP attribution • OUTPUT feature impact
            </div>
          </div>
        </HoloCard>

        {/* Card 3: 03 / ASSESS */}
        <HoloCard
          width="100%"
          aspectRatio={0.82}
          preset="gold"
          foilColor="#f59e0b"
          cardBorderColor="rgba(245, 158, 11, 0.35)"
          intensity={0.35}
          scale={1.2}
          edgeSparkle={0.35}
          frame={2.5}
          glare={0.2}
          radius={16}
          tiltMax={14}
          hoverScale={1.04}
        >
          <div className="flex flex-col justify-between h-full">
            <div>
              <div className="text-xs font-mono font-semibold tracking-wider text-[#F59E0B] mb-4 drop-shadow-[0_1px_3px_rgba(0,0,0,0.9)]">
                03 / ASSESS
              </div>

              <div className="w-9 h-9 rounded-lg border border-[#F59E0B]/50 bg-[#06111C]/90 backdrop-blur-md flex items-center justify-center text-[#F59E0B] mb-4 shadow-[0_2px_8px_rgba(0,0,0,0.7)]">
                <Lock className="w-5 h-5 text-[#F59E0B]" />
              </div>

              <h3 className="font-display text-lg font-bold text-[#FCD34D] mb-2 drop-shadow-[0_2px_6px_rgba(0,0,0,0.9)]">
                Website security checks
              </h3>

              <p className="font-ui text-xs text-[#FDE68A] leading-relaxed mb-6 font-normal drop-shadow-[0_1px_4px_rgba(0,0,0,0.9)]">
                Planned complementary checks cover SSL/TLS certificate properties and HTTP response headers such as HSTS, CSP and X-Frame-Options.
              </p>
            </div>

            <div className="pt-4 border-t border-[#F59E0B]/30 text-[10px] font-mono font-medium text-[#FBBF24] uppercase tracking-wider drop-shadow-[0_1px_3px_rgba(0,0,0,0.9)]">
              SCOPE Certificate &amp; headers • STATUS integration in progress
            </div>
          </div>
        </HoloCard>

      </div>
    </section>
  );
};

export default ArchitecturalPillars;
