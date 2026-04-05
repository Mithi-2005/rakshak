/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
    "./lib/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#fff7ed",
          100: "#ffedd5",
          200: "#fed7aa",
          300: "#fdba74",
          400: "#fb923c",
          500: "#f97316",
          600: "#ea580c",
          700: "#c2410c",
          800: "#9a3412",
          900: "#7c2d12"
        },
        ember: "#2b1308",
        mist: "rgba(255,255,255,0.18)"
      },
      boxShadow: {
        glow: "0 24px 80px rgba(249, 115, 22, 0.20)"
      },
      backdropBlur: {
        xs: "3px"
      }
    },
  },
  plugins: [],
};
