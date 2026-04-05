"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faArrowTrendUp,
  faCloudRain,
  faFileCircleCheck,
  faNewspaper,
  faShieldHeart,
  faSmog,
} from "@fortawesome/free-solid-svg-icons";

import { AnimatedSection } from "@/components/animated-section";
import { GlassCard } from "@/components/glass-card";
import { SiteNavbar } from "@/components/site-navbar";

const features = [
  {
    title: "Real trigger intelligence",
    copy: "Open-Meteo, AQI feeds, and news signals run continuously so policy actions are based on live external conditions.",
    icon: faCloudRain,
  },
  {
    title: "Dynamic worker pricing",
    copy: "Risk scoring uses zone, weather horizon, AQI trend, claim history, and income to tailor plan recommendations.",
    icon: faArrowTrendUp,
  },
  {
    title: "Automatic claim creation",
    copy: "Nightly claim jobs transform verified trigger events into visible worker claims with deterministic payout logic.",
    icon: faFileCircleCheck,
  },
];

const workflow = [
  { title: "Register", copy: "Create a worker account and complete your profile with pincode and income." },
  { title: "Choose cover", copy: "Buy an active plan generated from the ML pricing service." },
  { title: "Monitor zone", copy: "Rakshak polls weather, AQI, and disruption feeds every 15 minutes." },
  { title: "Receive claim", copy: "Valid trigger windows create claims automatically and surface them in your dashboard." },
];

export function LandingPage() {
  return (
    <>
      <SiteNavbar mode="public" />
      <main className="safe-shell">
        <section className="relative overflow-hidden rounded-[40px] border border-white/12 bg-white/6 px-6 py-14 shadow-glow md:px-10 md:py-20">
          <div className="absolute inset-y-0 right-0 w-1/2 bg-[radial-gradient(circle_at_top,rgba(249,115,22,0.28),transparent_52%)]" />
          <div className="relative z-10 grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
            <div>
              <motion.p
                initial={{ opacity: 0, y: 18 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="text-xs uppercase tracking-[0.38em] text-brand-200/75"
              >
                Parametric Insurance Platform
              </motion.p>
              <motion.h1
                initial={{ opacity: 0, y: 18 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.08 }}
                className="mt-5 max-w-3xl text-5xl font-semibold leading-[1.02] tracking-tight md:text-6xl"
              >
                Protection for gig workers built on live disruption signals, not guesswork.
              </motion.h1>
              <motion.p
                initial={{ opacity: 0, y: 18 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.16 }}
                className="mt-6 max-w-2xl text-lg leading-8 text-white/72"
              >
                Rakshak combines real-time weather, air quality, and disruption monitoring with ML-based
                risk pricing so workers can buy coverage, stay informed, and view auto-generated claims in one experience.
              </motion.p>
              <motion.div
                initial={{ opacity: 0, y: 18 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.24 }}
                className="mt-8 flex flex-wrap gap-3"
              >
                <Link href="/signup" className="rounded-full bg-brand-500 px-6 py-3 text-sm font-medium text-white transition hover:bg-brand-400">
                  Start With Rakshak
                </Link>
                <Link href="/login" className="rounded-full border border-white/14 bg-white/8 px-6 py-3 text-sm text-white/80 transition hover:bg-white/12">
                  Login
                </Link>
                <Link href="/dashboard" className="rounded-full border border-brand-400/30 bg-brand-500/10 px-6 py-3 text-sm text-brand-100 transition hover:bg-brand-500/16">
                  View Dashboard
                </Link>
              </motion.div>
            </div>

            <motion.div
              initial={{ opacity: 0, scale: 0.96, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              transition={{ duration: 0.65, delay: 0.18 }}
              className="grid gap-4"
            >
              <GlassCard className="rotate-[-2deg]">
                <p className="text-sm uppercase tracking-[0.3em] text-brand-200/70">Live Protection Stack</p>
                <div className="mt-5 grid gap-3">
                  {[
                    { label: "Weather feed", value: "Open-Meteo hourly precipitation", icon: faCloudRain },
                    { label: "AQI tracking", value: "WAQI with resilient fallback", icon: faSmog },
                    { label: "Disruption scanning", value: "Strike, bandh, and curfew headlines", icon: faNewspaper },
                  ].map((item) => (
                    <div key={item.label} className="rounded-2xl border border-white/10 bg-black/20 p-4">
                      <div className="flex items-center gap-3">
                        <div className="grid h-11 w-11 place-items-center rounded-2xl bg-brand-500/14 text-brand-200">
                          <FontAwesomeIcon icon={item.icon} />
                        </div>
                        <div>
                          <p className="font-medium">{item.label}</p>
                          <p className="text-sm text-white/64">{item.value}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </GlassCard>
              <GlassCard className="translate-x-4">
                <div className="flex items-end justify-between">
                  <div>
                    <p className="text-sm text-white/64">Platform promise</p>
                    <p className="mt-2 text-3xl font-semibold">Fast, automatic, readable</p>
                  </div>
                  <div className="grid h-14 w-14 place-items-center rounded-3xl bg-brand-500 text-white">
                    <FontAwesomeIcon icon={faShieldHeart} />
                  </div>
                </div>
              </GlassCard>
            </motion.div>
          </div>
        </section>

        <AnimatedSection className="mt-12 grid gap-5 md:grid-cols-3" id="features">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.45, delay: index * 0.08 }}
              whileHover={{ y: -6, scale: 1.01 }}
            >
              <GlassCard className="h-full rounded-[30px]">
                <div className="grid h-14 w-14 place-items-center rounded-3xl bg-brand-500/14 text-brand-200">
                  <FontAwesomeIcon icon={feature.icon} />
                </div>
                <h2 className="mt-6 text-2xl font-semibold">{feature.title}</h2>
                <p className="mt-4 leading-7 text-white/68">{feature.copy}</p>
              </GlassCard>
            </motion.div>
          ))}
        </AnimatedSection>

        <AnimatedSection className="mt-12 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]" id="workflow">
          <GlassCard className="rounded-[34px]">
            <p className="text-xs uppercase tracking-[0.34em] text-brand-200/70">Product Workflow</p>
            <h2 className="mt-4 text-3xl font-semibold">A journey that feels operational, not experimental.</h2>
            <p className="mt-4 leading-7 text-white/68">
              Every screen and service in the flow is designed to support a production-grade worker experience with clear actions and low friction.
            </p>
          </GlassCard>
          <div className="grid gap-4">
            {workflow.map((step, index) => (
              <motion.div
                key={step.title}
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.45, delay: index * 0.08 }}
                className="glass-panel rounded-[28px] p-5"
              >
                <div className="flex items-start gap-4">
                  <div className="grid h-12 w-12 flex-none place-items-center rounded-2xl bg-brand-500 text-sm font-semibold text-white">
                    0{index + 1}
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold">{step.title}</h3>
                    <p className="mt-2 text-white/66">{step.copy}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </AnimatedSection>

        <AnimatedSection className="mt-12 mb-4 grid gap-5 lg:grid-cols-[1.1fr_0.9fr]" id="pricing">
          <GlassCard className="rounded-[34px]">
            <p className="text-xs uppercase tracking-[0.34em] text-brand-200/70">Ready to onboard</p>
            <h2 className="mt-4 text-3xl font-semibold">A cleaner front door for the entire Rakshak workflow.</h2>
            <p className="mt-4 leading-7 text-white/68">
              Landing page, signup, login, dashboard, buy policy, profile, and claims now follow one visual system with fixed navigation, motion discipline, and mobile-first structure.
            </p>
          </GlassCard>
          <GlassCard className="rounded-[34px]">
            <div className="space-y-3">
              {[
                "Fixed navbar with product sections and auth actions",
                "Scroll reveal animations with restrained motion",
                "Reusable loading experience for route and data states",
                "Mobile-safe layout with fast transforms and minimal visual overhead",
              ].map((item) => (
                <div key={item} className="rounded-2xl border border-white/10 bg-black/15 px-4 py-3 text-white/74">
                  {item}
                </div>
              ))}
            </div>
          </GlassCard>
        </AnimatedSection>
      </main>
    </>
  );
}
