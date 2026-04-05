"use client";

import { motion } from "framer-motion";

export function AnimatedSection({ delay = 0, className = "", children }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 28, scale: 0.98 }}
      whileInView={{ opacity: 1, y: 0, scale: 1 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.55, delay }}
      className={className}
    >
      {children}
    </motion.section>
  );
}
