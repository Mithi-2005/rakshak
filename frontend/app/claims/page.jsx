"use client";

import { useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { AnimatedSection } from "@/components/animated-section";
import { GlassCard } from "@/components/glass-card";
import { LoadingScreen } from "@/components/loading-screen";
import { apiRequest } from "@/lib/api";

const badgeClasses = {
  CREATED: "bg-amber-500/20 text-amber-100",
  APPROVED: "bg-emerald-500/20 text-emerald-100",
  REJECTED: "bg-rose-500/20 text-rose-100",
};

export default function ClaimsPage() {
  const [claims, setClaims] = useState([]);
  const [message, setMessage] = useState("");
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    apiRequest("/claims/")
      .then((response) => {
        setClaims(response.items || []);
        setLoaded(true);
      })
      .catch((error) => {
        setMessage(error.message);
        setLoaded(true);
      });
  }, []);

  if (!loaded) {
    return (
      <AppShell title="Claims" eyebrow="Automatic Payout Trail">
        <LoadingScreen label="Loading claim ledger" />
      </AppShell>
    );
  }

  return (
    <AppShell title="Claims" eyebrow="Automatic Payout Trail">
      <AnimatedSection>
        <GlassCard>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-brand-200/75">Claim Ledger</p>
              <h2 className="mt-2 text-2xl font-semibold">Auto-created claims from real trigger events</h2>
            </div>
            <p className="text-sm text-white/60">{claims.length} records</p>
          </div>
          <div className="mt-6 space-y-3">
            {claims.map((claim, index) => (
              <div
                key={claim.id}
                className="rounded-2xl border border-white/10 bg-white/6 p-4 transition hover:translate-y-[-2px]"
                style={{ animationDelay: `${index * 80}ms` }}
              >
                <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                  <div>
                    <p className="font-medium">Claim #{claim.id}</p>
                    <p className="text-sm text-white/65">
                      Policy {claim.policy_id} · Trigger {claim.trigger_event_id}
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`rounded-full px-3 py-1 text-xs font-medium ${badgeClasses[claim.status] || "bg-white/10 text-white/80"}`}>
                      {claim.status}
                    </span>
                    <p className="text-lg font-semibold">₹{claim.claim_amount}</p>
                  </div>
                </div>
              </div>
            ))}
            {!claims.length && (
              <div className="rounded-2xl border border-dashed border-white/15 p-5 text-sm text-white/65">
                {message || "No claims available yet. Once a covered trigger is processed, it will appear here."}
              </div>
            )}
          </div>
        </GlassCard>
      </AnimatedSection>
    </AppShell>
  );
}
