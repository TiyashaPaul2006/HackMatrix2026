import React, { useEffect, useRef } from 'react';

const CyberRadarBackground = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let animId;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const scroll = { current: 0, target: 0, velocity: 0 };
    let sweepAngle = 0;

    const blips = Array.from({ length: 45 }, () => ({
      distNorm: 0.1 + Math.random() * 0.85,
      angle: Math.random() * Math.PI * 2,
      size: 1.5 + Math.random() * 2.2,
      intensity: 0.4 + Math.random() * 0.55,
      lastHitAlpha: 0,
      isPhishing: Math.random() > 0.62,
    }));

    const onScroll = () => { scroll.target = window.scrollY; };
    const onResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize);

    const render = () => {
      const prev = scroll.current;
      scroll.current += (scroll.target - scroll.current) * 0.05;
      scroll.velocity = Math.abs(scroll.current - prev);

      ctx.fillStyle = '#060D1A';
      ctx.fillRect(0, 0, width, height);

      const maxScroll = document.documentElement.scrollHeight - height || 1;
      const scrollRatio = Math.min(scroll.current / maxScroll, 1.0);

      const centerX = width * 0.5;
      const centerY = height * 0.5 - scroll.current * 0.10;

      const zoomScale = 1.0 + scrollRatio * 0.75;
      const maxRadius = Math.min(width, height) * 0.44 * zoomScale;

      const sweepSpeed = 0.013 * (1 + Math.min(scroll.velocity * 0.09, 3.0));
      sweepAngle = (sweepAngle + sweepSpeed) % (Math.PI * 2);

      const rings = [0.25, 0.5, 0.75, 1.0];
      ctx.strokeStyle = 'rgba(30, 51, 87, 0.25)';
      ctx.lineWidth = 0.8;

      rings.forEach((ratio) => {
        const r = maxRadius * ratio;
        ctx.beginPath();
        ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
        ctx.stroke();
        const urlCount = Math.round((100 / zoomScale) * ratio);
        ctx.font = '8px "JetBrains Mono", monospace';
        ctx.fillStyle = 'rgba(142, 158, 181, 0.3)';
        ctx.fillText(`${urlCount} URLs`, centerX + r + 4, centerY - 4);
      });

      ctx.beginPath();
      ctx.moveTo(centerX - maxRadius, centerY);
      ctx.lineTo(centerX + maxRadius, centerY);
      ctx.moveTo(centerX, centerY - maxRadius);
      ctx.lineTo(centerX, centerY + maxRadius);
      ctx.stroke();

      const sectorSegments = 28;
      const sectorSpan = Math.PI / 3.5;
      for (let s = 0; s < sectorSegments; s++) {
        const segAngle = sweepAngle - (s / sectorSegments) * sectorSpan;
        const alpha = (1 - s / sectorSegments) * 0.12;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, maxRadius, segAngle - 0.02, segAngle);
        ctx.closePath();
        ctx.fillStyle = `rgba(0, 229, 255, ${alpha})`;
        ctx.fill();
      }

      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(centerX + Math.cos(sweepAngle) * maxRadius, centerY + Math.sin(sweepAngle) * maxRadius);
      ctx.strokeStyle = 'rgba(0, 229, 255, 0.65)';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      blips.forEach((b) => {
        let angleDiff = sweepAngle - b.angle;
        if (angleDiff < 0) angleDiff += Math.PI * 2;

        if (angleDiff < 0.065) b.lastHitAlpha = b.intensity;
        else b.lastHitAlpha *= 0.98;

        if (b.lastHitAlpha > 0.01) {
          const currentDist = b.distNorm * maxRadius;
          const bx = centerX + Math.cos(b.angle) * currentDist;
          const by = centerY + Math.sin(b.angle) * currentDist;

          const r = b.isPhishing ? '255, 59, 59' : '0, 230, 118';
          ctx.beginPath();
          ctx.arc(bx, by, b.size * zoomScale, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(${r}, ${b.lastHitAlpha * 0.8})`;
          ctx.fill();
        }
      });

      animId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onResize);
    };
  }, []);

  return <canvas ref={canvasRef} className="fixed inset-0 -z-10 pointer-events-none" />;
};

export default CyberRadarBackground;

