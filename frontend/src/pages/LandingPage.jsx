import React from 'react';
import DotGrid from '../components/backgrounds/DotGrid';
import Navbar from '../components/layout/Navbar';
import HeroSection from '../components/hero/HeroSection';
import ArchitecturalPillars from '../components/landing/ArchitecturalPillars';
import BenchmarkStats from '../components/landing/BenchmarkStats';
import Footer from '../components/layout/Footer';

export const LandingPage = () => {
  return (
    <div className="min-h-screen bg-[#080C14] text-[#F8FAFC] font-ui relative selection:bg-[#06B6D4]/30 selection:text-white">
      
      {/* Overall Full-App Interactive WebGL Background: React Bits DotGrid (Softened & Subtle Blur) */}
      <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden bg-[#080C14]">
        <div className="w-full h-full scale-[1.02] filter blur-[1.2px] opacity-65">
          <DotGrid
            baseColor="#14404e"
            activeColor="#06b6d4"
            shape="square"
            dotSize={5}
            gap={15}
            proximity={180}
            strength={0.5}
            bounce={0}
            tension={0.6}
            returnDuration={1}
            shockRadius={400}
            shockStrength={6}
            swell={1}
            stretch={0.5}
            glow={0.5}
            fade={0}
            intro={true}
            clickShock={false}
            opacity={0.7}
          />
        </div>
      </div>

      {/* Section 1: Navigation Header */}
      <Navbar />

      {/* Main Content Flow */}
      <main className="relative z-10">
        {/* Section 2: Hero Command Center with Live Target URL Scanner */}
        <HeroSection />

        {/* Section 3: Analysis Pipeline (Three parts of a website assessment) */}
        <ArchitecturalPillars />

        {/* Section 4: Recorded Model Results (Evaluation, not marketing claims) */}
        <BenchmarkStats />
      </main>

      {/* Section 5: Operational Footer */}
      <Footer />

    </div>
  );
};

export default LandingPage;
