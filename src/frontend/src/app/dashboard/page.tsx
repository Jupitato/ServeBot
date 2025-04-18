"use client";

import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Layout } from "antd";
import NewChatInterface from "@/components/FirstPageChatInterface";
import Sidebar from "@/components/Sidebar";

export default function DashboardPage() {
  const { status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/login");
    }
  }, [status, router]);

  if (status === "loading") {
    return <div className="flex h-screen items-center justify-center">加载中...</div>;
  }

  return (
    <Layout style={{ height: '100vh' }}>
      {/* 侧边栏 */}
      <Sidebar />
      
      {/* 主内容区 */}
      <Layout style={{ padding: '0 24px 24px' }}>
        <Layout.Content style={{ 
          background: '#fff', 
          padding: '24px', 
          margin: 0, 
          minHeight: 280,
          borderRadius: '8px',
          height: 'calc(100vh - 100px)',
          overflow: 'auto'
        }}>
          <NewChatInterface />
        </Layout.Content>
      </Layout>
    </Layout>
  );
}