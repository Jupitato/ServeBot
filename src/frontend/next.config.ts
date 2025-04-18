import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  devIndicators: {
    position: 'bottom-right' // 原buildActivityPosition的值
  },
  // 确保这里的代理配置正确
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
        // 排除 NextAuth.js 路由
        has: [
          {
            type: 'header',
            key: 'x-exclude-auth',
            value: '(?!)',
          },
        ],
      },
    ];
  }
};

export default nextConfig;
