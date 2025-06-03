import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/save': 'http://localhost:5001',
      '/diary': 'http://localhost:5001'
    }
  },
})
