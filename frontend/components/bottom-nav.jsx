"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faChartLine,
  faFileCircleCheck,
  faShieldHeart,
  faUserPen,
} from "@fortawesome/free-solid-svg-icons";

const items = [
  { href: "/dashboard", label: "Dashboard", icon: faChartLine },
  { href: "/buy-policy", label: "Buy", icon: faShieldHeart },
  { href: "/claims", label: "Claims", icon: faFileCircleCheck },
  { href: "/profile", label: "Profile", icon: faUserPen },
];

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed inset-x-4 bottom-4 z-40 rounded-3xl border border-white/12 bg-black/25 p-3 backdrop-blur-xl md:hidden">
      <div className="grid grid-cols-4 gap-2">
        {items.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`rounded-2xl px-3 py-2 text-center text-xs transition ${
                active ? "bg-brand-500 text-white shadow-glow" : "bg-white/5 text-white/70"
              }`}
            >
              <FontAwesomeIcon icon={item.icon} className="mb-1 h-4 w-4" />
              <div>{item.label}</div>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
