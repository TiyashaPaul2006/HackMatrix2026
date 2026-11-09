import React from 'react';
import { ShieldCheck, ExternalLink } from 'lucide-react';

export const Footer = () => {
  return (
    <footer
      className="border-t border-[#06B6D4]/25 mt-16 py-12 px-6 relative z-10 text-xs font-ui
        shadow-[0_-4px_24px_rgba(0,0,0,0.4),0_-8px_20px_-4px_rgba(6,182,212,0.12)]
        transition-all duration-300"
      style={{
        backgroundColor: 'rgba(6, 32, 44, 0.40)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
      }}
    >
      <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 mb-10">
        
        {/* Column 1: Brand & Mission */}
        <div>
          <div className="flex items-center gap-2 mb-3">
            <ShieldCheck className="w-4 h-4 text-[#06B6D4]" />
            <span className="font-display font-bold text-sm tracking-wider text-white">
              CYBER SENTINEL
            </span>
          </div>
          <p className="text-[#94A3B8] leading-relaxed max-w-sm">
            AI-powered URL threat detection and digital-trust assessment, built around XGBoost classification, SHAP explainability and a FastAPI inference service.
          </p>
        </div>

        {/* Column 2: Explore Navigation */}
        <div>
          <div className="font-bold text-white uppercase tracking-wider mb-3 text-[11px] font-mono">
            EXPLORE
          </div>
          <ul className="space-y-2 text-[#94A3B8]">
            <li>
              <a href="#scanner" className="hover:text-[#06B6D4] transition-colors">
                URL scanner
              </a>
            </li>
            <li>
              <a href="#pipeline" className="hover:text-[#06B6D4] transition-colors">
                Assessment approach
              </a>
            </li>
            <li>
              <a href="#evaluation" className="hover:text-[#06B6D4] transition-colors">
                Model evaluation
              </a>
            </li>
          </ul>
        </div>

        {/* Column 3: Developer Endpoints */}
        <div>
          <div className="font-bold text-white uppercase tracking-wider mb-3 text-[11px] font-mono">
            DEVELOPER
          </div>
          <ul className="space-y-2 text-[#94A3B8]">
            <li>
              <a
                href="http://127.0.0.1:8000/docs"
                target="_blank"
                rel="noreferrer"
                className="hover:text-[#06B6D4] transition-colors flex items-center gap-1.5"
              >
                <span>FastAPI documentation</span>
                <ExternalLink className="w-3 h-3 text-[#64748B]" />
              </a>
            </li>
            <li>
              <a
                href="http://127.0.0.1:8000/"
                target="_blank"
                rel="noreferrer"
                className="hover:text-[#06B6D4] transition-colors flex items-center gap-1.5"
              >
                <span>API health endpoint</span>
                <ExternalLink className="w-3 h-3 text-[#64748B]" />
              </a>
            </li>
          </ul>
        </div>

      </div>

      {/* Bottom Legal / Palette Bar */}
      <div className="max-w-5xl mx-auto border-t border-[#1E293B] pt-6 flex flex-wrap justify-between items-center text-[11px] text-[#64748B]">
        <div>© 2026 Cyber Sentinel • HackMatrix</div>
        <div className="font-mono tracking-wider">
          OBSIDIAN SLATE / NEON THREAT SPECTRUM
        </div>
      </div>
    </footer>
  );
};

export default Footer;
