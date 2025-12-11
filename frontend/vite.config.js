import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import fs from "fs";

export default defineConfig({
  server: {
    https: {
      key: fs.readFileSync("../backend/key.pem"),
      cert: fs.readFileSync("../backend/cert.pem"),
    },
    port: 5173,
  },
  plugins: [react()],
});
