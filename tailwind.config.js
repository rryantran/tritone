/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {
      minWidth: {
        'navlink': '15rem',
      },
    },
  },
  plugins: [],
}

