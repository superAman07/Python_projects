/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}", // ✅ For App Router (app directory)
    "./components/**/*.{js,ts,jsx,tsx}", // ✅ For shared components
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
