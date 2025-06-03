import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/save': 'http://localhost:5001',
      '/diary': 'http://localhost:5001',
      // 將所有 /api 開頭的請求代理到後端 5003
      '/api': {
        target: 'http://localhost:5003',
        changeOrigin: true
      }
    }
  },
})
