"use client";

import { useState } from "react";
import { Card, Input, Button, Typography, Space } from "antd";
import { SendOutlined } from "@ant-design/icons";
import { useRouter } from 'next/navigation';
import { v4 as uuidv4 } from 'uuid';

export default function NewChatInterface() {
  const router = useRouter();
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { Title, Paragraph } = Typography;

  const handleCreateNewChat = () => {
    if (!input.trim() || isLoading) return;
    
    // 设置加载状态
    setIsLoading(true);
    
    // 生成新的对话ID
    const newChatId = uuidv4();
    console.log("FirstPage: Creating new chat with ID:", newChatId);
    console.log("FirstPage: Initial message:", input);
    
    // 确保URL参数正确编码
    const encodedMessage = encodeURIComponent(input);
    const url = `/chat/${newChatId}?initialMessage=${encodedMessage}`;
    console.log("FirstPage: Navigating to:", url);
    
    // 跳转到新的聊天页面，并传递初始消息
    router.push(url);
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
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', textAlign: 'center' }}>
          <img src="/file.svg" alt="avatar" style={{ width: '80px', height: '80px', marginBottom: '16px' }} />
          <Title level={3} style={{ marginBottom: '8px' }}>我是 智能客服机器人，很高兴见到你！</Title>
          <Paragraph type="secondary" style={{ marginBottom: '24px' }}>
            我可以处理各种客服问题，请把你的问题交给我吧~
          </Paragraph>
          <Space direction="vertical" style={{ width: '100%', maxWidth: '500px' }}>
            <Input.Search
              placeholder="给 智能客服机器人 发送消息"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onSearch={handleCreateNewChat}
              enterButton={<Button type="primary" icon={<SendOutlined />}>发送</Button>}
              disabled={isLoading}
              loading={isLoading}
            />
          </Space>
        </div>
      </div>
    </Card>
  );
} 