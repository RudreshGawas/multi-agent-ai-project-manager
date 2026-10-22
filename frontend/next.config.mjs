import { resolve } from "node:path";

const nextConfig = {
  output: "standalone",
  turbopack: {
    root: resolve(process.cwd()),
  },
};

export default nextConfig;
