import { useEffect, useRef } from 'react';

/**
 * CyberNetworkBackground
 * High-performance HTML5 Canvas cybersecurity network visualization.
 * Renders floating security nodes, connecting neural mesh lines, traveling data particles,
 * and responds subtly to mouse movement. Fully responsive and accessible.
 */
export default function CyberNetworkBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Check prefers-reduced-motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    let animationFrameId;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    // Responsive configuration
    const isMobile = width < 768;
    const NODE_COUNT = isMobile ? 26 : 52;
    const MAX_DISTANCE = isMobile ? 110 : 155;
    const PARTICLE_SPEED = 0.45;

    // Pointer tracker for subtle interaction
    const pointer = {
      x: width / 2,
      y: height / 2,
      isActive: false,
    };

    // Node definition
    class Node {
      constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * PARTICLE_SPEED;
        this.vy = (Math.random() - 0.5) * PARTICLE_SPEED;
        this.radius = Math.random() * 1.5 + 1.2;
        this.baseRadius = this.radius;
        this.pulse = Math.random() * Math.PI * 2;
        this.pulseSpeed = 0.02 + Math.random() * 0.02;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        // Bounce gently at screen edges
        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;

        // Subtle mouse attraction/deflection
        if (pointer.isActive) {
          const dx = pointer.x - this.x;
          const dy = pointer.y - this.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 140 && dist > 0) {
            const force = (140 - dist) / 140 * 0.015;
            this.x -= (dx / dist) * force * 10;
            this.y -= (dy / dist) * force * 10;
          }
        }

        this.pulse += this.pulseSpeed;
      }

      draw() {
        const currentRadius = this.baseRadius + Math.sin(this.pulse) * 0.5;
        ctx.beginPath();
        ctx.arc(this.x, this.y, Math.max(0.5, currentRadius), 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(96, 165, 250, 0.75)';
        ctx.shadowBlur = 8;
        ctx.shadowColor = 'rgba(59, 130, 246, 0.5)';
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    }

    // Traveling packet particle
    class DataPacket {
      constructor(fromNode, toNode) {
        this.from = fromNode;
        this.to = toNode;
        this.progress = Math.random();
        this.speed = 0.006 + Math.random() * 0.008;
      }

      update() {
        this.progress += this.speed;
        if (this.progress > 1) {
          this.progress = 0;
        }
      }

      draw() {
        const x = this.from.x + (this.to.x - this.from.x) * this.progress;
        const y = this.from.y + (this.to.y - this.from.y) * this.progress;

        ctx.beginPath();
        ctx.arc(x, y, 1.8, 0, Math.PI * 2);
        ctx.fillStyle = '#38bdf8';
        ctx.shadowBlur = 6;
        ctx.shadowColor = '#38bdf8';
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    }

    // Initialize nodes
    const nodes = Array.from({ length: NODE_COUNT }, () => new Node());
    const packets = [];

    // Create fixed packet pairs between nearby nodes
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        if (Math.hypot(dx, dy) < MAX_DISTANCE && Math.random() > 0.65) {
          packets.push(new DataPacket(nodes[i], nodes[j]));
        }
      }
    }

    // Animation Loop
    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // Draw dynamic network connections
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[i].x - nodes[j].x;
          const dy = nodes[i].y - nodes[j].y;
          const dist = Math.hypot(dx, dy);

          if (dist < MAX_DISTANCE) {
            const alpha = (1 - dist / MAX_DISTANCE) * 0.22;
            ctx.beginPath();
            ctx.moveTo(nodes[i].x, nodes[i].y);
            ctx.lineTo(nodes[j].x, nodes[j].y);
            ctx.strokeStyle = `rgba(59, 130, 246, ${alpha})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }
      }

      // Update and draw packets
      for (let p of packets) {
        p.update();
        p.draw();
      }

      // Update and draw nodes
      for (let node of nodes) {
        node.update();
        node.draw();
      }

      if (!prefersReducedMotion) {
        animationFrameId = requestAnimationFrame(render);
      }
    };

    // Draw once or start loop
    if (prefersReducedMotion) {
      render();
    } else {
      render();
    }

    // Window event handlers
    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };

    const handleMouseMove = (e) => {
      pointer.x = e.clientX;
      pointer.y = e.clientY;
      pointer.isActive = true;
    };

    const handleMouseLeave = () => {
      pointer.isActive = false;
    };

    window.addEventListener('resize', handleResize);
    window.addEventListener('mousemove', handleMouseMove, { passive: true });
    document.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  return (
    <>
      <div className="cyber-grid-overlay" aria-hidden="true" />
      <canvas ref={canvasRef} className="cyber-canvas" aria-hidden="true" />
    </>
  );
}
