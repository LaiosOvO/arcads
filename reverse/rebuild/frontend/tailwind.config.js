/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: { extend: { colors: { ink: "#0f1115", panel: "#171a21", line: "#262b36",
    brand: "#5b8cff", ok: "#3ddc97", warn: "#ffb454" } } },
  plugins: [],
};
