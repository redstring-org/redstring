import { useEffect, useRef } from "react";

const DOT_COUNT    = 38;
const MAX_DIST     = 180;   // px — max distance to draw a string
const DOT_RADIUS   = 1.8;
const DOT_OPACITY  = 0.35;
const LINE_OPACITY = 0.55;  // max line opacity at zero distance
const SPEED        = 0.28;  // px per frame

type Dot = {
  x: number;
  y: number;
  vx: number;
  vy: number;
};

function randomDot(w: number, h: number): Dot {
  const angle = Math.random() * Math.PI * 2;
  return {
    x: Math.random() * w,
    y: Math.random() * h,
    vx: Math.cos(angle) * SPEED * (0.4 + Math.random() * 0.6),
    vy: Math.sin(angle) * SPEED * (0.4 + Math.random() * 0.6),
  };
}

export function RedStringCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let raf: number;
    let dots: Dot[] = [];

    function resize() {
      if (!canvas) return;
      canvas.width  = window.innerWidth;
      canvas.height = window.innerHeight;
      dots = Array.from({ length: DOT_COUNT }, () =>
        randomDot(canvas.width, canvas.height)
      );
    }

    function draw() {
      if (!canvas || !ctx) return;
      const W = canvas.width;
      const H = canvas.height;

      ctx.clearRect(0, 0, W, H);

      // move dots, bounce off walls
      for (const d of dots) {
        d.x += d.vx;
        d.y += d.vy;
        if (d.x < 0)  { d.x = 0;  d.vx = Math.abs(d.vx); }
        if (d.x > W)  { d.x = W;  d.vx = -Math.abs(d.vx); }
        if (d.y < 0)  { d.y = 0;  d.vy = Math.abs(d.vy); }
        if (d.y > H)  { d.y = H;  d.vy = -Math.abs(d.vy); }
      }

      // draw strings between close dots
      for (let i = 0; i < dots.length; i++) {
        for (let j = i + 1; j < dots.length; j++) {
          const dx   = dots[i].x - dots[j].x;
          const dy   = dots[i].y - dots[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist > MAX_DIST) continue;

          const t       = 1 - dist / MAX_DIST;        // 0..1, 1 = closest
          const opacity = LINE_OPACITY * t * t;        // ease falloff

          const grad = ctx.createLinearGradient(
            dots[i].x, dots[i].y,
            dots[j].x, dots[j].y
          );
          grad.addColorStop(0,   `rgba(239,68,68,${opacity})`);
          grad.addColorStop(0.5, `rgba(249,115,22,${opacity * 0.7})`);
          grad.addColorStop(1,   `rgba(239,68,68,${opacity})`);

          ctx.beginPath();
          ctx.moveTo(dots[i].x, dots[i].y);
          ctx.lineTo(dots[j].x, dots[j].y);
          ctx.strokeStyle = grad;
          ctx.lineWidth   = 0.8 + t * 0.6;
          ctx.stroke();
        }
      }

      // draw dots
      for (const d of dots) {
        ctx.beginPath();
        ctx.arc(d.x, d.y, DOT_RADIUS, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(200,210,230,${DOT_OPACITY})`;
        ctx.fill();
      }

      raf = requestAnimationFrame(draw);
    }

    resize();
    window.addEventListener("resize", resize);
    draw();

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: "fixed",
        inset: 0,
        width: "100%",
        height: "100%",
        pointerEvents: "none",
        zIndex: 0,
      }}
    />
  );
}
