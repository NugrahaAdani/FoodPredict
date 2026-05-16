/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,mjs,html}"
  ],
  theme: {
    extend: {
      colors: {
        ijo: '#2DD4BF',
      },
      fontFamily: {
        jakarta: ['"Plus Jakarta Sans"', 'sans-serif'],
      },
      backgroundImage: {
        'dark-gradient': 'linear-gradient(to bottom, #0f172a, #1e293b)',
      },
    },
  },
  plugins: [],
}
