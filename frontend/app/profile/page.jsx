"use client";

import { useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { GlassCard } from "@/components/glass-card";
import { apiRequest, postJson } from "@/lib/api";

const initialState = {
  phone: "",
  platform: "",
  city: "",
  pincode: "",
  vehicle_type: "",
  avg_daily_income: "",
};

export default function ProfilePage() {
  const [form, setForm] = useState(initialState);
  const [message, setMessage] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    apiRequest("/user/profile")
      .then((response) => {
        if (response.profile) {
          setForm({
            ...response.profile,
            avg_daily_income: response.profile.avg_daily_income || "",
          });
        }
      })
      .catch(() => {});
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    try {
      await postJson("/user/profile", {
        ...form,
        avg_daily_income: Number(form.avg_daily_income),
      });
      setMessage("Profile updated successfully.");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <AppShell title="Profile" eyebrow="Coverage Setup">
      <GlassCard className="mx-auto max-w-3xl rounded-[32px]">
        <form className="grid gap-4 md:grid-cols-2" onSubmit={handleSubmit}>
          {[
            ["phone", "Phone"],
            ["platform", "Platform"],
            ["city", "City"],
            ["pincode", "Pincode"],
            ["vehicle_type", "Vehicle Type"],
            ["avg_daily_income", "Average Daily Income"],
          ].map(([key, label]) => (
            <div key={key} className={key === "avg_daily_income" ? "md:col-span-2" : ""}>
              <label className="mb-2 block text-sm text-white/72">{label}</label>
              <input
                value={form[key] ?? ""}
                onChange={(event) => setForm((prev) => ({ ...prev, [key]: event.target.value }))}
                className="w-full rounded-2xl border border-white/10 bg-white/8 px-4 py-3 outline-none transition focus:border-brand-300/40"
              />
            </div>
          ))}
          <div className="md:col-span-2">
            <button disabled={saving} className="w-full rounded-2xl bg-brand-500 px-4 py-3 font-medium text-white transition hover:bg-brand-400 disabled:cursor-not-allowed disabled:opacity-70">
              {saving ? "Saving profile..." : "Save Profile"}
            </button>
          </div>
        </form>
        <p className="mt-4 text-sm text-white/70">{message}</p>
      </GlassCard>
    </AppShell>
  );
}
