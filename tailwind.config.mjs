/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Sora", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      maxWidth: {
        content: "620px",
        wide: "1000px",
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: "none",
            a: {
              color: "#0f766e",
              textDecorationColor: "#0f766e",
            },
          },
        },
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
