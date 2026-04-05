"use client";

import { motion } from "framer-motion";

export function LoadingScreen({ label = "Loading protection experience" }) {
  return (
    <div className="grid min-h-[45vh] place-items-center">
      <div className="glass-panel rounded-[32px] px-10 py-12 text-center">
        <motion.div
          className="mx-auto flex h-20 w-20 items-center justify-center rounded-[28px] bg-brand-500/20"
          animate={{ rotate: 360 }}
          transition={{ repeat: Number.POSITIVE_INFINITY, duration: 2.4, ease: "linear" }}
        >
          <motion.div
            className="h-10 w-10 rounded-2xl bg-brand-500"
            animate={{ scale: [1, 1.16, 1] }}
            transition={{ repeat: Number.POSITIVE_INFINITY, duration: 1.25 }}
          />
        </motion.div>
        <p className="mt-6 text-lg font-medium text-white">Rakshak</p>
        <p className="mt-2 text-sm text-white/64">{label}</p>
      </div>
    </div>
  );
}
