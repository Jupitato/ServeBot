import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 开启React严格模式，帮助发现潜在问题
  reactStrictMode: true,
  
  // API请求代理配置，用于解决跨域问题
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
  
  // 图片优化配置
  images: {
    domains: ['localhost'],
    formats: ['image/avif', 'image/webp'],
  },
  
  // 环境变量配置
  env: {
    NEXT_PUBLIC_API_URL: 'http://localhost:8000',
  },
  
  // 压缩配置
  compress: true,
  
  // 输出模式配置
  output: 'standalone',
};

export default nextConfig;
