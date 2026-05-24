import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/index": "http://backend:8000",
      "/query": "http://backend:8000",
    },
  },
});
