/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fffbf0',
          100: '#fef3e2',
          200: '#fde8c8',
          300: '#fcd9a1',
          400: '#fac575',
          500: '#f8ae4a',
          600: '#f5933d',
          700: '#e87a2f',
          800: '#c75d2b',
          900: '#a34d26',
        },
        accent: {
          50: '#fffef5',
          100: '#fffceb',
          200: '#fff9d6',
          300: '#fff5b3',
          400: '#ffee80',
          500: '#ffe74c',
          600: '#ffd700',
          700: '#ffb700',
          800: '#ff9500',
          900: '#ff7100',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
