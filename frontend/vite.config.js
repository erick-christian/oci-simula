import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
    plugins: [
        vue(),
        VitePWA({
            registerType: 'autoUpdate',
            manifest: {
                name: 'OCI Simulador 2026',
                short_name: 'OCI 2026',
                description: 'Simulador de Examen de Conocimiento',
                theme_color: '#4f46e5',
                background_color: '#f0fdfa',
                display: 'standalone',
                icons: [
                    {
                        src: '/favicon/favicon-16x16.png',
                        sizes: '16x16',
                        type: 'image/png'
                    },
                    {
                        src: '/favicon/favicon-32x32.png',
                        sizes: '32x32',
                        type: 'image/png'
                    },
                    {
                        src: 'pwa-192x192.png',
                        sizes: '192x192',
                        type: 'image/png'
                    },
                    {
                        src: 'pwa-512x512.png',
                        sizes: '512x512',
                        type: 'image/png',
                        purpose: 'any maskable'
                    }
                ]
            },
            workbox: {
                // Previene que el Service Worker intercepte la carga de PDFs en los iframes y devuelva index.html
                navigateFallbackDenylist: [/^\/referencias/],
            }
        })
    ],
    server: {
        host: '0.0.0.0', // Necesario para Docker
        port: 5173,
        watch: {
            usePolling: true // Necesario para que funcione bien en VirtualBox
        },
        proxy: {
            '/api': {
                target: 'http://backend:5000',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, '')
            }
        },
        allowedHosts: ['oci.terian.com.mx', 'midudev.terian.com.mx']
    }
})