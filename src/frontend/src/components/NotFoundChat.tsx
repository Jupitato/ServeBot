"use client";

import { Button, Result } from "antd";
import { useRouter } from "next/navigation";

export default function NotFoundChat() {
  const router = useRouter();

  const handleBackToHome = () => {
    router.push("/dashboard");
  };

  return (
    <Result
      status="404"
      title="聊天记录不存在"
      subTitle="您访问的聊天记录不存在或已被删除"
      extra={
        <Button type="primary" onClick={handleBackToHome}>
          返回首页
        </Button>
      }
    />
  );
} 