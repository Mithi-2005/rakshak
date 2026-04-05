"use client";

import { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCloudRain,
  faFileCircleCheck,
  faShieldHeart,
  faSmog,
} from "@fortawesome/free-solid-svg-icons";

import { apiRequest } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { AnimatedSection } from "@/components/animated-section";
import { GlassCard } from "@/components/glass-card";
import { LoadingScreen } from "@/components/loading-screen";
import { StatCard } from "@/components/stat-card";

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    apiRequest("/policies/dashboard")
      .then((payload) => {
        setData(payload);
        setLoaded(true);
      })
      .catch((err) => {
        setError(err.message);
        setLoaded(true);
      });
  }, []);

  if (!loaded) {
    return (
      <AppShell title="Worker Dashboard" eyebrow="Phase 2 Live Monitoring">
        <LoadingScreen label="Syncing risk, coverage, and trigger data" />
      </AppShell>
    );
  }

  const activePolicy = data?.active_policy;

  return (
    <AppShell title="Worker Dashboard" eyebrow="Phase 2 Live Monitoring">
      <div className="space-y-6">
        <AnimatedSection className="relative overflow-hidden rounded-[32px] border border-white/12 bg-white/6 p-6 shadow-glow">
          <div className="absolute -top-20 right-0 h-56 w-56 rounded-full bg-brand-500/20 blur-3xl" />
          <div className="relative z-10 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
            <div>
              <p className="text-sm uppercase tracking-[0.35em] text-brand-200/70">Income Shield</p>
              <h2 className="mt-3 max-w-xl text-4xl font-semibold leading-tight">
                Real triggers, active cover, and automatic claim visibility in one view.
              </h2>
              <p className="mt-4 max-w-2xl text-white/72">
                Rakshak tracks weather, AQI, and civic disruption signals for your pincode every
                fifteen minutes and prepares claims automatically when covered events occur.
              </p>
            </div>
            <GlassCard className="self-start">
              <p className="text-sm text-white/70">Current protection</p>
              <p className="mt-3 text-3xl font-semibold">
                {activePolicy ? `${activePolicy.plan_id.toUpperCase()} Plan` : "No active policy"}
              </p>
              <p className="mt-2 text-sm text-white/65">
                {activePolicy
                  ? `Covered through ${activePolicy.end_date}`
                  : "Buy a plan to activate trigger monitoring for your zone."}
              </p>
            </GlassCard>
          </div>
        </AnimatedSection>

        {error ? (
          <GlassCard className="border-brand-400/30">
            <p className="text-sm text-brand-200">{error}</p>
          </GlassCard>
        ) : null}

        <AnimatedSection delay={0.1} className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <StatCard icon={faShieldHeart} label="Risk Score" value={(data?.risk_score || 0) * 100} suffix="%" />
          <StatCard icon={faCloudRain} label="Open Triggers" value={data?.open_triggers_count || 0} />
          <StatCard icon={faFileCircleCheck} label="Claims" value={data?.recent_claims_count || 0} />
          <StatCard
            icon={faSmog}
            label="Coverage"
            value={activePolicy?.coverage_amount || 0}
            suffix="k"
            tone="text-brand-200"
          />
        </AnimatedSection>

        <AnimatedSection delay={0.15} className="grid gap-6 lg:grid-cols-2">
          <GlassCard>
            <p className="text-sm uppercase tracking-[0.3em] text-brand-200/75">Risk Plans</p>
            <div className="mt-4 space-y-3">
              {(data?.plans || []).map((plan, index) => (
                <div
                  key={plan.plan_id}
                  className={`rounded-2xl border border-white/10 bg-white/6 p-4 transition hover:scale-[1.02] ${
                    index === 1 ? "border-brand-400/40 bg-brand-500/10" : ""
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium capitalize">{plan.plan_id}</p>
                      <p className="text-sm text-white/65">{plan.coverage}k coverage</p>
                    </div>
                    <p className="text-xl font-semibold">Rs {plan.premium}</p>
                  </div>
                </div>
              ))}
            </div>
          </GlassCard>

          <GlassCard>
            <p className="text-sm uppercase tracking-[0.3em] text-brand-200/75">Live trigger sources</p>
            <div className="mt-4 grid gap-3">
              {[
                { label: "Rain monitoring", value: "Open-Meteo hourly precipitation" },
                { label: "Air quality tracking", value: "WAQI with Open-Meteo fallback" },
                { label: "Disruption headlines", value: "News keyword scoring" },
              ].map((item) => (
                <div key={item.label} className="rounded-2xl border border-white/10 bg-black/15 p-4">
                  <p className="font-medium">{item.label}</p>
                  <p className="mt-1 text-sm text-white/65">{item.value}</p>
                </div>
              ))}
            </div>
          </GlassCard>
        </AnimatedSection>
      </div>
    </AppShell>
  );
}
