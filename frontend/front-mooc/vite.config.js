import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  base: './',  // Important for relative paths
  build: {
    outDir: 'dist',  // Default output directory
    emptyOutDir: true,
    rollupOptions: {
      output: {
        // Improve asset naming and chunking
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash][extname]'
      }
    }
  },
  server: {
    // Development only: proxy API requests to your FastAPI server
    proxy: {
      // Proxy all /api requests to your backend
      '/api': {
        target: 'http://localhost:7860',
        changeOrigin: true,
        // Uncomment if you need to remove /api from the path
        //rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },

})

