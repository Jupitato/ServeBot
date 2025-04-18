"use client";

import { useState } from 'react';
import { Layout, List, Typography, Button, Badge, Divider } from 'antd';
import { MessageOutlined, DownloadOutlined, UserOutlined, LogoutOutlined } from '@ant-design/icons';
import Link from 'next/link';
import { useSession, signOut } from "next-auth/react";
import { useRouter } from 'next/navigation';

const { Sider } = Layout;
const { Title, Text } = Typography;

type ChatHistoryItem = {
  id: string;
  title: string;
  time: Date;
};

const Sidebar = () => {
  const router = useRouter();
  const { data: session } = useSession();
  
  // 模拟聊天历史数据
  const [chatHistory] = useState<{
    yesterday: ChatHistoryItem[];
    sevenDays: ChatHistoryItem[];
    thirtyDays: ChatHistoryItem[];
  }>({
    yesterday: [
      { id: '1', title: '微信OAuth2.0登录接入流程详解', time: new Date() },
    ],
    sevenDays: [
      { id: '2', title: 'NextAuth.js登录认证实现指南', time: new Date() },
      { id: '3', title: '失业状态下理财与购房决策分析', time: new Date() },
      { id: '4', title: '独立开发者需求挖掘与冷启动策略', time: new Date() },
    ],
    thirtyDays: [
      { id: '5', title: 'CSS高效学习资源与路径推荐', time: new Date() },
      { id: '6', title: '米粒卡气管急急处理指南', time: new Date() },
      { id: '7', title: '长沙旅游景点与玩法推荐', time: new Date() },
      { id: '8', title: '学生护眼台灯品牌推荐指南', time: new Date() },
      { id: '9', title: '流行前端框架推荐与比较', time: new Date() },
      { id: '10', title: 'React.js和Next.js入门学习指南', time: new Date() },
      { id: '11', title: '前端主流框架及新兴趋势解析', time: new Date() },
    ],
  });

  const startNewChat = () => {
    // 跳转到 dashboard 页面
    router.push('/dashboard');
  };

  return (
    <Sider
      width={280}
      style={{ 
        background: '#f7f7f7', 
        height: '100%',
        overflowY: 'auto',
        borderRight: '1px solid #e8e8e8'
      }}
    >
      <div style={{ padding: '16px 16px 0' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <Title level={4} style={{ margin: 0 }}>智能客服机器人</Title>
        </div>
        
        <Button 
          type="primary" 
          icon={<MessageOutlined />} 
          style={{ 
            width: '100%', 
            marginBottom: '24px',
            borderRadius: '8px',
            backgroundColor: '#e6f4ff',
            color: '#1677ff',
            border: 'none'
          }}
          onClick={startNewChat}
        >
          开始新对话
        </Button>
      </div>

      <div style={{ padding: '0 16px' }}>
        {/* 昨天的聊天记录 */}
        <div style={{ marginBottom: '16px' }}>
          <Text type="secondary" style={{ fontSize: '12px' }}>昨天</Text>
          <List
            itemLayout="horizontal"
            dataSource={chatHistory.yesterday}
            renderItem={(item) => (
              <List.Item className="chat-history-item" style={{ padding: '8px 0', border: 'none', borderRadius: '4px' }}>
                <Link href={`/chat/${item.id}`} style={{ width: '100%', color: 'inherit', textDecoration: 'none' }}>
                  <Text ellipsis style={{ width: '100%', display: 'block' }}>{item.title}</Text>
                </Link>
              </List.Item>
            )}
          />
        </div>

        {/* 7天内的聊天记录 */}
        <div style={{ marginBottom: '16px' }}>
          <Text type="secondary" style={{ fontSize: '12px' }}>7 天内</Text>
          <List
            itemLayout="horizontal"
            dataSource={chatHistory.sevenDays}
            renderItem={(item) => (
              <List.Item className="chat-history-item" style={{ padding: '8px 0', border: 'none', borderRadius: '4px' }}>
                <Link href={`/chat/${item.id}`} style={{ width: '100%', color: 'inherit', textDecoration: 'none' }}>
                  <Text ellipsis style={{ width: '100%', display: 'block' }}>{item.title}</Text>
                </Link>
              </List.Item>
            )}
          />
        </div>

        {/* 30天内的聊天记录 */}
        <div style={{ marginBottom: '16px' }}>
          <Text type="secondary" style={{ fontSize: '12px' }}>30 天内</Text>
          <List
            itemLayout="horizontal"
            dataSource={chatHistory.thirtyDays}
            renderItem={(item) => (
              <List.Item className="chat-history-item" style={{ padding: '8px 0', border: 'none', borderRadius: '4px' }}>
                <Link href={`/chat/${item.id}`} style={{ width: '100%', color: 'inherit', textDecoration: 'none' }}>
                  <Text ellipsis style={{ width: '100%', display: 'block' }}>{item.title}</Text>
                </Link>
              </List.Item>
            )}
          />
        </div>
      </div>

      {/* 底部区域 */}
      <div style={{ 
        position: 'sticky', 
        bottom: 0, 
        width: '100%', 
        padding: '16px',
        background: '#f7f7f7',
        borderTop: '1px solid #e8e8e8'
      }}>
        <Button 
          block 
          icon={<DownloadOutlined />}
          style={{ 
            borderRadius: '20px',
            height: '40px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          下载 App
          <Badge 
            count={'NEW'} 
            style={{ 
              marginLeft: '8px',
              backgroundColor: '#1677ff',
              fontSize: '10px',
              height: '16px',
              lineHeight: '16px',
              padding: '0 4px'
            }} 
          />
        </Button>
        
        <Divider style={{ margin: '16px 0' }} />
        
        {/* 用户信息和登出按钮 */}
        <div style={{ 
          display: 'flex', 
          flexDirection: 'column',
          gap: '8px'
        }}>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'space-between'
          }}>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <UserOutlined style={{ marginRight: '8px' }} />
              <Text>{session?.user?.name || '用户'}</Text>
            </div>
            <Button 
              type="text" 
              danger 
              icon={<LogoutOutlined />} 
              onClick={() => signOut({ callbackUrl: "/login" })}
              size="small"
            >
              退出登录
            </Button>
          </div>
        </div>
      </div>
    </Sider>
  );
};

export default Sidebar;