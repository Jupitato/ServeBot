"use client";

import { useState, useRef, useEffect } from "react";
import { useSession } from "next-auth/react";
import { Card, Input, Button, Avatar, Typography, Space } from "antd";
import { SendOutlined, UserOutlined, RobotOutlined } from "@ant-design/icons";
import { useSearchParams } from 'next/navigation';

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
};

interface ChatInterfaceProps {
  chatId: string; // 不再是可选参数，必须提供
}

export default function ChatInterface({ chatId }: ChatInterfaceProps) {
  const { data: session } = useSession();
  const searchParams = useSearchParams();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { Title, Paragraph } = Typography;
  
  // 使用ref跟踪是否已处理初始消息
  const initialMessageProcessed = useRef(false);

  // 自动滚动到最新消息
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 处理URL中的初始消息参数，使用ref避免重复执行
  useEffect(() => {
    // 避免在SSR中执行
    if (typeof window === 'undefined') return;
    
    // 检查URL是否包含初始消息参数
    const initialMessage = searchParams.get('initialMessage');
    
    // 如果已经处理过初始消息或没有初始消息或已经有消息，则返回
    if (initialMessageProcessed.current || !initialMessage || messages.length > 0 || isLoading) {
      return;
    }
    
    // 标记为已处理，防止重复处理
    initialMessageProcessed.current = true;
    console.log("Processing initial message:", initialMessage);
    
    // 创建用户消息对象
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: initialMessage,
      timestamp: new Date(),
    };

    // 添加用户消息到列表
    setMessages([userMessage]);
    
    // 发送消息到后端
    sendMessageToAPI(userMessage.content);
    
    // 清除URL参数，但保留当前路径
    if (window.history.replaceState) {
      const newUrl = window.location.pathname;
      window.history.replaceState({ path: newUrl }, '', newUrl);
    }
  }, [searchParams]); // 仅依赖searchParams，不依赖messages或isLoading

  // 发送消息到API的函数
  const sendMessageToAPI = async (messageContent: string) => {
    setIsLoading(true);
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session?.user}`,
        },
        body: JSON.stringify({
          message: messageContent,
          chatId: chatId,
        }),
      });

      if (!response.ok) {
        throw new Error("服务器响应错误");
      }

      const data = await response.json();
      
      const assistantMessage: Message = {
        id: Date.now().toString(),
        role: "assistant",
        content: data.response_msg || "抱歉，我无法处理您的请求。",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("发送消息错误:", error);
      
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: "assistant",
        content: "抱歉，发生了错误，请稍后再试。",
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    // 创建用户消息
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    // 添加到消息列表
    setMessages((prev) => [...prev, userMessage]);
    
    // 清空输入框
    setInput("");
    
    // 发送到API
    await sendMessageToAPI(userMessage.content);
  };

  const handleSearch = () => {
    handleSendMessage(new Event('submit') as unknown as React.FormEvent);
  };

  return (
    <Card 
      className="h-full" 
      styles={{
        body: { 
          padding: 0, 
          display: 'flex', 
          flexDirection: 'column', 
          height: '100%' 
        }
      }}
    >
      {/* 聊天消息区域 */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px' }}>
        {messages.length === 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', textAlign: 'center' }}>
            <Title level={3} style={{ marginBottom: '8px' }}>开始新的对话</Title>
            <Paragraph type="secondary" style={{ marginBottom: '24px' }}>
              发送消息开始与智能客服机器人对话
            </Paragraph>
            <Space direction="vertical" style={{ width: '100%', maxWidth: '500px' }}>
              <Input.Search
                placeholder="输入消息..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onSearch={handleSearch}
                enterButton={<Button type="primary" icon={<SendOutlined />}>发送</Button>}
                disabled={isLoading}
                loading={isLoading}
              />
            </Space>
          </div>
        ) : (
          <div>
            {messages.map((message) => (
              <div
                key={message.id}
                style={{
                  display: 'flex',
                  justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
                  marginBottom: '16px'
                }}
              >
                {message.role === 'assistant' && (
                  <Avatar
                    icon={<RobotOutlined />}
                    style={{ backgroundColor: '#1677ff', marginRight: '8px' }}
                  />
                )}
                <div
                  style={{
                    maxWidth: '70%',
                    padding: '12px 16px',
                    borderRadius: '8px',
                    backgroundColor: message.role === 'user' ? '#1677ff' : '#f0f0f0',
                    color: message.role === 'user' ? 'white' : 'rgba(0, 0, 0, 0.85)'
                  }}
                >
                  <div style={{ whiteSpace: 'pre-wrap' }}>{message.content}</div>
                  <div
                    style={{
                      fontSize: '12px',
                      marginTop: '4px',
                      color: message.role === 'user' ? 'rgba(255, 255, 255, 0.7)' : 'rgba(0, 0, 0, 0.45)'
                    }}
                  >
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>
                {message.role === 'user' && (
                  <Avatar
                    icon={<UserOutlined />}
                    style={{ backgroundColor: '#1677ff', marginLeft: '8px' }}
                  />
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* 输入区域 - 当有消息时显示 */}
      {messages.length > 0 && (
        <div style={{ padding: '16px', borderTop: '1px solid #f0f0f0' }}>
          <form onSubmit={handleSendMessage} style={{ display: 'flex' }}>
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="输入消息..."
              disabled={isLoading}
              style={{ flexGrow: 1 }}
            />
            <Button
              type="primary"
              htmlType="submit"
              disabled={isLoading}
              loading={isLoading}
              icon={<SendOutlined />}
              style={{ marginLeft: '8px' }}
            >
              {isLoading ? "发送中..." : "发送"}
            </Button>
          </form>
        </div>
      )}
    </Card>
  );
}