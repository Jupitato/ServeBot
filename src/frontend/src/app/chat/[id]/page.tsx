"use client";

import { useParams, useSearchParams } from 'next/navigation';
import { Layout } from "antd";
import { useState, useEffect } from "react";
import { useSession } from "next-auth/react";
import ChatInterface from "@/components/ChatInterface";
import NotFoundChat from "@/components/NotFoundChat";
import Sidebar from "@/components/Sidebar";

export default function ChatPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const chatId = params.id as string;
  const { data: session } = useSession();
  
  // 检查URL参数，判断是否是新创建的聊天
  const initialMessage = searchParams.get('initialMessage');
  const isNewChat = Boolean(initialMessage);
  
  // 聊天状态: 未确认、存在、不存在
  const [chatStatus, setChatStatus] = useState<'initial' | 'exists' | 'not_exists'>(
    // 如果是新聊天，则初始值为exists，否则为initial
    isNewChat ? 'exists' : 'initial'
  );
  
  // 只有在需要验证的情况下才初始化loading状态
  const [isValidating, setIsValidating] = useState(false);

  // 验证聊天ID是否存在
  useEffect(() => {
    // 如果是新聊天，则不需要验证，直接返回
    if (isNewChat) {
      return;
    }
    
    // 如果没有会话或状态已经确定，则不验证
    if (!session || chatStatus !== 'initial') {
      return;
    }
    
    // 设置验证标志，防止重复验证
    let isMounted = true;
    setIsValidating(true);
    
    // 验证函数
    async function validateChatId() {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat/validate`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${session?.user}`,
          },
          body: JSON.stringify({ chatId }),
        });

        if (!isMounted) return;

        if (response.ok) {
          const data = await response.json();
          setChatStatus(data.exists ? 'exists' : 'not_exists');
        } else {
          setChatStatus('not_exists');
        }
      } catch (error) {
        if (!isMounted) return;
        console.error("验证聊天ID错误:", error);
        setChatStatus('not_exists');
      } finally {
        if (isMounted) {
          setIsValidating(false);
        }
      }
    }

    validateChatId();
    
    // 清理函数，防止组件卸载后仍然设置状态
    return () => {
      isMounted = false;
    };
  }, [chatId, session, isNewChat, chatStatus]);

  // 如果是新聊天或已确认存在，显示聊天界面
  const shouldShowChat = chatStatus === 'exists';
  
  // 如果正在验证或尚未确定状态，显示加载中
  const isLoading = isValidating || (chatStatus === 'initial' && !isNewChat);

  // 根据状态渲染不同的内容
  return (
    <Layout style={{ height: '100vh' }}>
      <Sidebar />
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
          {isLoading ? (
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              height: '100%' 
            }}>
              加载中...
            </div>
          ) : shouldShowChat ? (
            <ChatInterface chatId={chatId} />
          ) : (
            <NotFoundChat />
          )}
        </Layout.Content>
      </Layout>
    </Layout>
  );
} 