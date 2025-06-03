// final_frontend/tailwind.config.js
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: "#D97706",    // 橙黃主色
        secondary: "#FEF3C7",  // 米白底色
        accent: "#65A30D",     // 綠色強調色
        neutral: "#6B7280",    // 中性灰
      },
      spacing: {
        72: "18rem",
        84: "21rem",
        96: "24rem",
      },
      borderRadius: {
        xl: "1.5rem",
      },
      // 若範本有其他 extend 設定，也可放在這裡
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};