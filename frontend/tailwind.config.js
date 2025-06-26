/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{vue,js,ts,jsx,tsx,html}"
  ],
  theme: {
    extend: {
      colors: {
        'dark': '#333333',
        'muted': '#A0A0A0',
        'soft-silver': '#F2F2F2',
        'snow-vei': '#FBFBFB',
        'olive-grove': '#5F8B4C',
        'fresh-dew': '#DDF6D2'
      },
      fontFamily: {
        outfit: ['Outfit', 'sans-serif'],
        roboto: ['Roboto', 'sans-serif'],
      },
      fontSize: {
        md: '16px',
      },
    },
  },
  plugins: [],
}

