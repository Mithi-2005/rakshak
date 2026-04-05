"use client";

import { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { GlassCard } from "@/components/glass-card";

export function StatCard({ icon, label, value, suffix = "", tone = "text-brand-300" }) {
  const numericValue = Number(value) || 0;
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    let frameId;
    const startedAt = performance.now();
    const duration = 900;

    const tick = (time) => {
      const progress = Math.min((time - startedAt) / duration, 1);
      setDisplayValue(numericValue * progress);
      if (progress < 1) frameId = requestAnimationFrame(tick);
    };

    frameId = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frameId);
  }, [numericValue]);

  return (
    <GlassCard className="h-full">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-white/70">{label}</p>
          <p className="mt-2 text-3xl font-semibold tracking-tight">
            {displayValue.toFixed(0)}
            {suffix}
          </p>
        </div>
        <div className={`grid h-12 w-12 place-items-center rounded-2xl bg-white/10 ${tone}`}>
          <FontAwesomeIcon icon={icon} />
        </div>
      </div>
    </GlassCard>
  );
}
