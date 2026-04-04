"use client";

import { motion } from "framer-motion";

import { BottomNav } from "@/components/bottom-nav";
import { SiteNavbar } from "@/components/site-navbar";

export function AppShell({ title, eyebrow, children, mode = "app" }) {
  return (
    <>
      <SiteNavbar mode={mode} />
      <div className="safe-shell">
        <header className="glass-panel mb-6 rounded-[32px] px-6 py-8">
          <p className="text-xs uppercase tracking-[0.35em] text-brand-200/80">{eyebrow}</p>
          <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white md:text-4xl">{title}</h1>
        </header>

        <motion.main
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          {children}
        </motion.main>
      </div>
      {mode === "app" ? <BottomNav /> : null}
    </>
  );
}
