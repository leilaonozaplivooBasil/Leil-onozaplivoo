import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Portal com sessão por cookie: páginas são dinâmicas, sem cache de componentes.
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
