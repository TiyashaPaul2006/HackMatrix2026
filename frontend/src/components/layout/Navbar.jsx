import React from 'react';
import { ShieldCheck, ArrowUpRight } from 'lucide-react';

export const Navbar = () => {
  return (
    <header
      className="fixed top-0 left-0 right-0 h-16 z-50 px-6 flex items-center justify-between
        border-b border-[#06B6D4]/25
        shadow-[0_4px_24px_rgba(0,0,0,0.4),0_8px_20px_-4px_rgba(6,182,212,0.15)]
        transition-all duration-300"
      style={{
        backgroundColor: 'rgba(6, 32, 44, 0.40)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
      }}
    >
      {/* Brand Identity (Left) */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-[#0B111E]/80 border border-[#06B6D4]/40 flex items-center justify-center text-[#06B6D4] shadow-[0_0_12px_rgba(6,182,212,0.3)]">
          <ShieldCheck className="w-4 h-4 text-[#06B6D4]" />
        </div>
        <span className="font-display font-bold text-sm tracking-wider text-[#F8FAFC]">
          CYBER SENTINEL
        </span>
      </div>

      {/* Navigation Links + API Reference (Center) */}
      <nav className="hidden sm:flex items-center gap-7 lg:gap-8 text-[13.5px] font-ui font-medium text-[#94A3B8]">
        <a href="#scanner" className="hover:text-[#F8FAFC] transition-colors">
          Scanner
        </a>
        <a href="#pipeline" className="hover:text-[#F8FAFC] transition-colors">
          How it works
        </a>
        <a href="#evaluation" className="hover:text-[#F8FAFC] transition-colors">
          Evaluation
        </a>
        <a
          href="http://127.0.0.1:8000/docs"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-[#F8FAFC] transition-colors"
        >
          API reference
        </a>
      </nav>

      {/* Header Actions (Right) */}
      <div className="flex items-center">
        <a
          href="#scanner"
          className="bg-[#06B6D4] hover:bg-[#0891B2] text-white text-xs font-ui font-semibold px-4 py-2 rounded-md flex items-center gap-1.5 shadow-[0_0_16px_rgba(6,182,212,0.4)] hover:shadow-[0_0_24px_rgba(6,182,212,0.6)] transition-all"
        >
          <span>Open scanner</span>
          <ArrowUpRight className="w-3.5 h-3.5" />
        </a>
      </div>
    </header>
  );
};

export default Navbar;
