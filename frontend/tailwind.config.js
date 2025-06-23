/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{vue,js,ts,jsx,tsx,html}"
  ],
  theme: {
    extend: {
      colors: {
        'light-gray': '#F2F2F2',
        cream: '#FFFDF6',
        'dark-cream': '#FEF3E2',
        'pale-yellow': '#FFEEA9',
        'peach-orange': '#FFBF78',
        dark: '#222831',
      },
      fontFamily: {
        outfit: ['Outfit', 'sans-serif'],
        roboto: ['Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

