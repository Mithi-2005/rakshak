"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { AppShell } from "@/components/app-shell";
import { GlassCard } from "@/components/glass-card";
import { postJson, setToken } from "@/lib/api";

export default function SignupPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    try {
      const response = await postJson("/auth/signup", form);
      setToken(response.access_token);
      setMessage("Signup successful. Redirecting to profile setup.");
      router.push("/profile");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AppShell title="Create Account" eyebrow="Worker Onboarding" mode="public">
      <GlassCard className="mx-auto max-w-xl rounded-[32px]">
        <form className="space-y-4" onSubmit={handleSubmit}>
          {[
            ["name", "Full name"],
            ["email", "Email"],
            ["password", "Password"],
          ].map(([key, label]) => (
            <div key={key}>
              <label className="mb-2 block text-sm text-white/72">{label}</label>
              <input
                type={key === "password" ? "password" : "text"}
                value={form[key]}
                onChange={(event) => setForm((prev) => ({ ...prev, [key]: event.target.value }))}
                className="w-full rounded-2xl border border-white/10 bg-white/8 px-4 py-3 outline-none transition focus:border-brand-300/40"
              />
            </div>
          ))}
          <button disabled={submitting} className="w-full rounded-2xl bg-brand-500 px-4 py-3 font-medium text-white transition hover:bg-brand-400 disabled:cursor-not-allowed disabled:opacity-70">
            {submitting ? "Creating account..." : "Create Account"}
          </button>
        </form>
        <p className="mt-4 text-sm text-white/70">{message}</p>
        <Link href="/login" className="mt-4 inline-block text-sm text-brand-200">
          Already have an account
        </Link>
      </GlassCard>
    </AppShell>
  );
}
