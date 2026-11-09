import React, { useEffect, useRef } from 'react';

const PacketFlowBackground = () => {
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

    const cols = 6;
    const rows = 4;
    const nodes = [];
    for (let c = 0; c < cols; c++) {
      for (let r = 0; r < rows; r++) {
        nodes.push({
          x: width * 0.1 + (c / (cols - 1)) * (width * 0.8),
          y: height * 0.2 + (r / (rows - 1)) * (height * 0.6),
          pulse: Math.random() * Math.PI * 2,
        });
      }
    }

    const count = 75;
    const packets = Array.from({ length: count }, () => {
      const srcIdx = Math.floor(Math.random() * nodes.length * 0.5);
      const dstIdx = Math.floor(nodes.length * 0.5 + Math.random() * nodes.length * 0.5);
      return {
        srcIdx,
        dstIdx,
        t: Math.random(),
        speed: 0.0025 + Math.random() * 0.003,
        baseLength: 30 + Math.random() * 45,
        thickness: 0.8 + Math.random() * 1.0,
        opacity: 0.08 + Math.random() * 0.16,
        isPhishing: Math.random() > 0.68,
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

    const render = () => {
      const prevCurrent = scroll.current;
      scroll.current += (scroll.target - scroll.current) * 0.06;
      scroll.velocity = Math.abs(scroll.current - prevCurrent);

      mouse.x += (mouse.targetX - mouse.x) * 0.05;
      mouse.y += (mouse.targetY - mouse.y) * 0.05;

      ctx.fillStyle = '#060D1A';
      ctx.fillRect(0, 0, width, height);

      const speedMult = 1 + Math.min(scroll.velocity * 0.09, 3.5);
      const stretchMult = 1 + Math.min(scroll.velocity * 0.16, 4.0);

      nodes.forEach((nd) => {
        nd.pulse += 0.012 * speedMult;
        const pulseAlpha = 0.03 + Math.sin(nd.pulse) * 0.02;
        const grd = ctx.createRadialGradient(nd.x, nd.y, 0, nd.x, nd.y, 16);
        grd.addColorStop(0, `rgba(0, 229, 255, ${pulseAlpha})`);
        grd.addColorStop(1, 'rgba(0, 229, 255, 0)');
        ctx.fillStyle = grd;
        ctx.beginPath();
        ctx.arc(nd.x, nd.y, 16, 0, Math.PI * 2);
        ctx.fill();
      });

      ctx.strokeStyle = 'rgba(30, 51, 87, 0.15)';
      ctx.lineWidth = 0.5;
      nodes.slice(0, Math.floor(nodes.length / 2)).forEach((src) => {
        nodes.slice(Math.floor(nodes.length / 2)).forEach((dst) => {
          ctx.beginPath();
          ctx.moveTo(src.x, src.y);
          ctx.lineTo(dst.x, dst.y);
          ctx.stroke();
        });
      });

      packets.forEach((p) => {
        p.t += p.speed * speedMult;
        if (p.t >= 1) {
          p.t = 0;
          p.isPhishing = Math.random() > 0.68;
        }

        const src = nodes[p.srcIdx % nodes.length];
        const dst = nodes[p.dstIdx % nodes.length];

        const hx = src.x + (dst.x - src.x) * p.t;
        const hy = src.y + (dst.y - src.y) * p.t - scroll.current * 0.08;

        const tailT = Math.max(0, p.t - p.baseLength * stretchMult * 0.001);
        const tx = src.x + (dst.x - src.x) * tailT;
        const ty = src.y + (dst.y - src.y) * tailT - scroll.current * 0.08;

        const rgb = p.isPhishing ? '255, 59, 59' : '0, 229, 255';
        const grad = ctx.createLinearGradient(hx, hy, tx, ty);
        grad.addColorStop(0, `rgba(${rgb}, ${p.opacity * (1 + scroll.velocity * 0.04)})`);
        grad.addColorStop(1, `rgba(${rgb}, 0)`);

        ctx.strokeStyle = grad;
        ctx.lineWidth = p.thickness;
        ctx.beginPath();
        ctx.moveTo(hx, hy);
        ctx.lineTo(tx, ty);
        ctx.stroke();
      });

      animId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onResize);
      window.removeEventListener('mousemove', onMouseMove);
    };
  }, []);

  return <canvas ref={canvasRef} className="fixed inset-0 -z-10 pointer-events-none" />;
};

export default PacketFlowBackground;

