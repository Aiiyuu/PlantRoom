/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{vue,js,ts,jsx,tsx,html}"
  ],
  theme: {
    extend: {
      colors: {
        cream: '#FFFDF6',
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

