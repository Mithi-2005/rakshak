"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faArrowRightToBracket,
  faBarsStaggered,
  faChartLine,
  faFileCircleCheck,
  faShieldHeart,
  faUserPlus,
} from "@fortawesome/free-solid-svg-icons";
import { useState } from "react";

const publicLinks = [
  { href: "/#features", label: "Features" },
  { href: "/#workflow", label: "Workflow" },
  { href: "/#pricing", label: "Protection" },
];

const appLinks = [
  { href: "/dashboard", label: "Dashboard", icon: faChartLine },
  { href: "/buy-policy", label: "Buy Policy", icon: faShieldHeart },
  { href: "/claims", label: "Claims", icon: faFileCircleCheck },
];

function NavLink({ href, label, active, icon }) {
  return (
    <Link
      href={href}
      className={`rounded-full px-4 py-2 text-sm transition ${
        active
          ? "bg-brand-500 text-white shadow-glow"
          : "text-white/72 hover:bg-white/10 hover:text-white"
      }`}
    >
      {icon ? <FontAwesomeIcon icon={icon} className="mr-2" /> : null}
      {label}
    </Link>
  );
}

export function SiteNavbar({ mode = "public" }) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const navLinks = mode === "app" ? appLinks : publicLinks;

  return (
    <header className="fixed inset-x-0 top-0 z-50 px-4 pt-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl rounded-[28px] border border-white/12 bg-[#120904]/70 px-4 py-3 shadow-glow backdrop-blur-xl">
        <div className="flex items-center justify-between gap-4">
          <Link href="/" className="flex items-center gap-3">
            <div className="grid h-11 w-11 place-items-center rounded-2xl bg-brand-500/90 text-white shadow-glow">
              <span className="text-lg font-semibold">R</span>
            </div>
            <div>
              <p className="text-lg font-semibold tracking-tight text-white">Rakshak</p>
              <p className="text-[11px] uppercase tracking-[0.34em] text-brand-200/70">
                Income Shield
              </p>
            </div>
          </Link>

          <nav className="hidden items-center gap-2 lg:flex">
            {navLinks.map((item) => (
              <NavLink
                key={item.href}
                href={item.href}
                label={item.label}
                icon={item.icon}
                active={pathname === item.href}
              />
            ))}
          </nav>

          <div className="hidden items-center gap-2 lg:flex">
            {mode === "public" ? (
              <>
                <NavLink href="/login" label="Login" icon={faArrowRightToBracket} active={pathname === "/login"} />
                <Link
                  href="/signup"
                  className="rounded-full bg-brand-500 px-5 py-2 text-sm font-medium text-white transition hover:bg-brand-400"
                >
                  <FontAwesomeIcon icon={faUserPlus} className="mr-2" />
                  Get Started
                </Link>
              </>
            ) : (
              <Link
                href="/profile"
                className="rounded-full bg-white/10 px-5 py-2 text-sm text-white/80 transition hover:bg-white/14"
              >
                Profile
              </Link>
            )}
          </div>

          <button
            type="button"
            onClick={() => setOpen((value) => !value)}
            className="grid h-11 w-11 place-items-center rounded-2xl bg-white/8 text-white lg:hidden"
          >
            <FontAwesomeIcon icon={faBarsStaggered} />
          </button>
        </div>

        {open ? (
          <div className="mt-4 space-y-2 border-t border-white/10 pt-4 lg:hidden">
            {navLinks.map((item) => (
              <NavLink
                key={item.href}
                href={item.href}
                label={item.label}
                icon={item.icon}
                active={pathname === item.href}
              />
            ))}
            <div className="flex gap-2 pt-2">
              <NavLink href="/login" label="Login" icon={faArrowRightToBracket} active={pathname === "/login"} />
              <NavLink href="/signup" label="Signup" icon={faUserPlus} active={pathname === "/signup"} />
            </div>
          </div>
        ) : null}
      </div>
    </header>
  );
}
