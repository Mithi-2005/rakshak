"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { AppShell } from "@/components/app-shell";
import { GlassCard } from "@/components/glass-card";
import { postJson, setToken } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    try {
      const response = await postJson("/auth/login", { email, password });
      setToken(response.access_token);
      setMessage("Login successful. Redirecting to dashboard.");
      router.push("/dashboard");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AppShell title="Login" eyebrow="Secure Access" mode="public">
      <GlassCard className="mx-auto max-w-xl rounded-[32px]">
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="mb-2 block text-sm text-white/72">Email</label>
            <input value={email} onChange={(e) => setEmail(e.target.value)} className="w-full rounded-2xl border border-white/10 bg-white/8 px-4 py-3 outline-none transition focus:border-brand-300/40" />
          </div>
          <div>
            <label className="mb-2 block text-sm text-white/72">Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full rounded-2xl border border-white/10 bg-white/8 px-4 py-3 outline-none transition focus:border-brand-300/40" />
          </div>
          <button disabled={submitting} className="w-full rounded-2xl bg-brand-500 px-4 py-3 font-medium text-white transition hover:bg-brand-400 disabled:cursor-not-allowed disabled:opacity-70">
            {submitting ? "Signing in..." : "Sign In"}
          </button>
        </form>
        <p className="mt-4 text-sm text-white/70">{message}</p>
        <Link href="/signup" className="mt-4 inline-block text-sm text-brand-200">
          Need an account
        </Link>
      </GlassCard>
    </AppShell>
  );
}
