import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import * as path from "path";
export var envPath = path.resolve(process.cwd());
export default defineConfig(function (_a) {
    var mode = _a.mode;
    var APP_URL = loadEnv(mode, envPath, "").APP_URL;
    return {
        define: {
            "process.env": {
                APP_URL: APP_URL,
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
                "/api": {
                    target: 'http://localhost:8000',
                    changeOrigin: true,
                },
            },
        },
    };
});
