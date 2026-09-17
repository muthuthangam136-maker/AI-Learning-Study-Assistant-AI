/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f4ff',
          100: '#d9e2ff',
          200: '#b9ccff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#0f172a'
        },
        ibm: {
          blue: '#0f62fe',
          dark: '#161616',
          gray: '#262626',
          cyan: '#1192e8'
        }
      }
    },
  },
  plugins: [],
}
