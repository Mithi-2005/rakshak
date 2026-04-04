export function GlassCard({ className = "", children }) {
  return (
    <div
      className={`glass-panel rounded-3xl border border-white/12 bg-white/10 p-5 shadow-glow ${className}`}
    >
      {children}
    </div>
  );
}
