import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  async rewrites() {
    const apiUrl = process.env.API_URL ?? 'http://localhost:8000';
    return [
      {
        source: '/kite-weather/:path*',
        destination: `${apiUrl}/kite-weather/:path*`,
      },
    ];
  },
};

export default nextConfig;
