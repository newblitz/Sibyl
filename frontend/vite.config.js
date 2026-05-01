import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/create': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/appointment': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/know_more': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/internship': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
