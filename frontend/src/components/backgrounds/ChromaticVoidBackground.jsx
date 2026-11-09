import React, { useEffect, useState, useRef } from 'react';

const ChromaticVoidBackground = () => {
  const [state, setState] = useState({ scrollY: 0, velocity: 0, mouseX: 0, mouseY: 0 });
  const scrollRef = useRef({ current: 0, target: 0, velocity: 0 });
  const animRef = useRef(null);

  useEffect(() => {
    const handleScroll = () => { scrollRef.current.target = window.scrollY; };

    const handleMouseMove = (e) => {
      const mouseX = (e.clientX / window.innerWidth - 0.5) * 40;
      const mouseY = (e.clientY / window.innerHeight - 0.5) * 40;
      setState((prev) => ({ ...prev, mouseX, mouseY }));
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('mousemove', handleMouseMove);

    const updatePhysics = () => {
      const prev = scrollRef.current.current;
      scrollRef.current.current += (scrollRef.current.target - scrollRef.current.current) * 0.05;
      scrollRef.current.velocity = Math.abs(scrollRef.current.current - prev);

      setState((prev) => ({
        ...prev,
        scrollY: scrollRef.current.current,
        velocity: scrollRef.current.velocity,
      }));

      animRef.current = requestAnimationFrame(updatePhysics);
    };

    updatePhysics();

    return () => {
      cancelAnimationFrame(animRef.current);
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  const stretch = 1 + Math.min(state.velocity * 0.04, 0.6);
  const squeeze = 1 - Math.min(state.velocity * 0.015, 0.2);

  return (
    <div className="fixed inset-0 -z-10 bg-[#060D1A] overflow-hidden pointer-events-none">
      <style>{`
        @keyframes drift-cyan {
          0%, 100% { transform: translate(0px, 0px); }
          50% { transform: translate(38px, -28px); }
        }
        @keyframes drift-navy {
          0%, 100% { transform: translate(0px, 0px); }
          50% { transform: translate(-32px, 36px); }
        }
      `}</style>

      {/* Layer 1: Threat Intelligence Cyan (Fast Parallax: 0.35x) */}
      <div
        className="absolute top-[12%] left-[22%] w-[52vw] h-[52vw] rounded-full blur-[95px] transition-transform duration-100 ease-linear"
        style={{
          background: 'radial-gradient(circle, rgba(0, 229, 255, 0.11) 0%, rgba(0, 229, 255, 0) 70%)',
          transform: `translate(${state.mouseX}px, ${-state.scrollY * 0.35 + state.mouseY}px) scale(${squeeze}, ${stretch})`,
          animation: 'drift-cyan 22s ease-in-out infinite',
        }}
      />

      {/* Layer 2: Deep Void Navy (Slow Parallax: 0.12x) */}
      <div
        className="absolute bottom-[8%] right-[18%] w-[68vw] h-[68vw] rounded-full blur-[115px] transition-transform duration-100 ease-linear"
        style={{
          background: 'radial-gradient(circle, rgba(12, 26, 46, 0.45) 0%, rgba(12, 26, 46, 0) 70%)',
          transform: `translate(${-state.mouseX * 0.5}px, ${-state.scrollY * 0.12}px)`,
          animation: 'drift-navy 28s ease-in-out infinite',
        }}
      />

      {/* Layer 3: Phishing Red Accent (High Parallax: 0.55x) */}
      <div
        className="absolute top-[58%] left-[42%] w-[34vw] h-[34vw] rounded-full blur-[85px] transition-transform duration-100 ease-linear"
        style={{
          background: 'radial-gradient(circle, rgba(255, 59, 59, 0.045) 0%, rgba(255, 59, 59, 0) 70%)',
          transform: `translate(${state.mouseX * 0.75}px, ${-state.scrollY * 0.55}px) scale(${stretch}, ${squeeze})`,
        }}
      />

      {/* Layer 4: Infrastructure Dot Grid */}
      <div
        className="absolute inset-0 opacity-[0.025]"
        style={{
          backgroundImage: 'radial-gradient(rgba(255, 255, 255, 0.8) 1px, transparent 1px)',
          backgroundSize: '28px 28px',
        }}
      />
    </div>
  );
};

export default ChromaticVoidBackground;

