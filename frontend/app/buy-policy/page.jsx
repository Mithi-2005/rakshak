"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";

import { AppShell } from "@/components/app-shell";
import { AnimatedSection } from "@/components/animated-section";
import { GlassCard } from "@/components/glass-card";
import { LoadingScreen } from "@/components/loading-screen";
import { apiRequest, postJson } from "@/lib/api";

export default function BuyPolicyPage() {
  const [plans, setPlans] = useState([]);
  const [message, setMessage] = useState("");
  const [selectedPlan, setSelectedPlan] = useState("");
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    apiRequest("/policies/plans")
      .then((response) => {
        setPlans(response.plans || []);
        setLoaded(true);
      })
      .catch((error) => {
        setMessage(error.message);
        setLoaded(true);
      });
  }, []);

  if (!loaded) {
    return (
      <AppShell title="Buy Policy" eyebrow="Dynamic ML Pricing">
        <LoadingScreen label="Loading policy recommendations" />
      </AppShell>
    );
  }

  async function handleBuy(plan) {
    try {
      await postJson("/policies/", {
        plan_id: plan.plan_id,
        coverage_amount: plan.coverage,
        premium_amount: plan.premium,
        duration_days: 7,
      });
      setSelectedPlan(plan.plan_id);
      setMessage(`${plan.plan_id} policy activated successfully.`);
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <AppShell title="Buy Policy" eyebrow="Dynamic ML Pricing">
      <AnimatedSection className="grid gap-5 lg:grid-cols-3">
        {plans.map((plan, index) => {
          const active = selectedPlan === plan.plan_id;
          return (
            <motion.div
              key={plan.plan_id}
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.08 }}
              whileHover={{ scale: 1.03 }}
            >
              <GlassCard
                className={`h-full transition ${
                  active ? "border-brand-300/60 bg-brand-500/12" : ""
                }`}
              >
                <p className="text-sm uppercase tracking-[0.3em] text-brand-200/75">
                  {plan.plan_id}
                </p>
                <p className="mt-4 text-4xl font-semibold">₹{plan.premium}</p>
                <p className="mt-1 text-sm text-white/70">Weekly premium</p>
                <div className="mt-6 rounded-2xl bg-black/20 p-4">
                  <p className="text-sm text-white/70">Coverage amount</p>
                  <p className="mt-2 text-2xl font-semibold">{plan.coverage}k</p>
                </div>
                <button
                  onClick={() => handleBuy(plan)}
                  className="mt-6 w-full rounded-2xl bg-brand-500 px-4 py-3 font-medium text-white transition hover:bg-brand-400"
                >
                  Select Plan
                </button>
              </GlassCard>
            </motion.div>
          );
        })}
      </AnimatedSection>

      {message ? (
        <GlassCard className="mt-6">
          <p className="text-sm text-white/72">{message}</p>
        </GlassCard>
      ) : null}
    </AppShell>
  );
}
