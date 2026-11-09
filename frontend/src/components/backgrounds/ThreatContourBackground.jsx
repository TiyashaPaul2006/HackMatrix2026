import React, { useEffect, useRef } from 'react';

const ThreatContourBackground = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let animId;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const scroll = { current: 0, target: 0, velocity: 0 };
    const mouse = { x: width / 2, y: height / 2, targetX: width / 2, targetY: height / 2 };

    const riskLevels = [
      { label: 'CRITICAL', color: '220, 38, 38', speed: 0.0010, zDepth: 120, harmonics: [{ freq: 3, amp: 4, spd: 0.0014 }, { freq: 5, amp: 2, spd: -0.002 }], alpha: 0.5 },
      { label: 'HIGH', color: '249, 115, 22', speed: 0.0008, zDepth: 85, harmonics: [{ freq: 4, amp: 5, spd: 0.0011 }, { freq: 6, amp: 2, spd: -0.0016 }], alpha: 0.35 },
      { label: 'MEDIUM', color: '245, 158, 11', speed: 0.0007, zDepth: 50, harmonics: [{ freq: 3, amp: 6, spd: 0.0009 }, { freq: 5, amp: 3, spd: -0.0012 }], alpha: 0.22 },
      { label: 'SAFE', color: '16, 185, 129', speed: 0.0005, zDepth: 18, harmonics: [{ freq: 4, amp: 7, spd: 0.0007 }, { freq: 7, amp: 2, spd: -0.001 }], alpha: 0.12 },
    ];

    const ringCount = 14;
    const rings = Array.from({ length: ringCount }, (_, i) => {
      const tNorm = i / (ringCount - 1);
      const riskIdx = Math.min(Math.floor(tNorm * riskLevels.length), riskLevels.length - 1);
      const risk = riskLevels[riskIdx];
      return {
        baseRadius: 55 + Math.pow(tNorm, 1.3) * (Math.max(width, height) * 0.56),
        risk,
        zDepthFactor: risk.zDepth * (1 - tNorm * 0.5),
        harmonics: risk.harmonics,
        alpha: risk.alpha * (1 - tNorm * 0.5) + 0.03,
        isLabelRing: i % 4 === 0,
      };
    });

    const onScroll = () => { scroll.target = window.scrollY; };
    const onResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    const onMouseMove = (e) => {
      mouse.targetX = e.clientX;
      mouse.targetY = e.clientY;
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize);
    window.addEventListener('mousemove', onMouseMove);

    const render = (timestamp) => {
      const prev = scroll.current;
      scroll.current += (scroll.target - scroll.current) * 0.05;
      scroll.velocity = Math.abs(scroll.current - prev);

      mouse.x += (mouse.targetX - mouse.x) * 0.05;
      mouse.y += (mouse.targetY - mouse.y) * 0.05;

      ctx.fillStyle = '#060D1A';
      ctx.fillRect(0, 0, width, height);

      const maxScroll = document.documentElement.scrollHeight - height || 1;
      const scrollRatio = Math.min(scroll.current / maxScroll, 1.0);

      const centerX = width * 0.5 + (mouse.x - width / 2) * 0.03;
      const centerY = height * 0.5 - scroll.current * 0.14 + (mouse.y - height / 2) * 0.03;

      rings.forEach((ring, idx) => {
        const steps = 150;
        ctx.beginPath();

        const zDisplacement = ring.zDepthFactor * scrollRatio * 1.6;
        const ringCenterY = centerY + zDisplacement;

        for (let i = 0; i <= steps; i++) {
          const angle = (i / steps) * Math.PI * 2;
          let wave = 0;
          const flutterAmp = 1 + Math.min(scroll.velocity * 0.09, 3.0);
          ring.harmonics.forEach((h) => {
            wave += Math.sin(angle * h.freq + timestamp * h.spd) * h.amp * flutterAmp;
          });

          const currentRadius = ring.baseRadius + wave;
          const yCompress = 0.82 - scrollRatio * 0.22;

          let px = centerX + Math.cos(angle) * currentRadius;
          let py = ringCenterY + Math.sin(angle) * currentRadius * yCompress;

          const dx = px - mouse.x;
          const dy = py - mouse.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 180) {
            const factor = Math.cos((dist / 180) * (Math.PI / 2)) * 12;
            px += (dx / dist) * factor;
            py += (dy / dist) * factor;
          }

          if (i === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }

        ctx.closePath();
        ctx.lineWidth = idx === 0 ? 1.5 : 0.75;
        ctx.strokeStyle = `rgba(${ring.risk.color}, ${ring.alpha + Math.min(scroll.velocity * 0.015, 0.2)})`;
        ctx.stroke();

        if (ring.isLabelRing) {
          const labelAngle = 0.4 + idx * 0.14;
          const lx = centerX + Math.cos(labelAngle) * ring.baseRadius;
          const ly = ringCenterY + Math.sin(labelAngle) * ring.baseRadius * (0.82 - scrollRatio * 0.22);
          ctx.font = '9px "JetBrains Mono", monospace';
          ctx.fillStyle = `rgba(${ring.risk.color}, ${0.35 + scrollRatio * 0.3})`;
          ctx.fillText(ring.risk.label, lx + 7, ly);
        }
      });

      animId = requestAnimationFrame(render);
    };

    render(0);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onResize);
      window.removeEventListener('mousemove', onMouseMove);
    };
  }, []);

  return <canvas ref={canvasRef} className="fixed inset-0 -z-10 pointer-events-none" />;
};

export default ThreatContourBackground;

