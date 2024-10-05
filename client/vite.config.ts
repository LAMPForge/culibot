import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import * as path from "path";

export const envPath = path.resolve(process.cwd());

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, envPath, "");

  return {
    define: {
      "process.env": {
        APP_URL: env.VITE_APP_URL,
      },
      'APP_VERSION': JSON.stringify(process.env.npm_package_version),
    },
    plugins: [react()],
    resolve: {
      alias: {
        "@": "/src",
      },
    },
    server: {
      proxy: {
        '/v1': {
          target: env.VITE_APP_URL || 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/v1/, '/v1'),
          followRedirects: true,
        },
      },
    },
    optimizeDeps: {
      include: ["@tabler/icons-react"],
    }
  };
});