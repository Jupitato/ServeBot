'use client';

import { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [clientId, setClientId] = useState('');
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 生成客户端ID
  useEffect(() => {
    const storedClientId = localStorage.getItem('clientId');
    if (storedClientId) {
      setClientId(storedClientId);
    } else {
      const newClientId = uuidv4();
      localStorage.setItem('clientId', newClientId);
      setClientId(newClientId);
    }
  }, []);

  // 建立WebSocket连接
  useEffect(() => {
    if (!clientId) return;

    const connectWebSocket = () => {
      const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
      
      ws.onopen = () => {
        console.log('WebSocket连接已建立');
        setIsConnected(true);
      };
      
      ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        console.log('收到消息:', message);
        
        setMessages(prev => {
          // 同时处理用户消息和AI回复
          const isExisting = prev.some(m => m.id === message.id);
          if (!isExisting) {
            // 根据角色类型更新对应消息
            if (message.role === 'user') {
              return prev.map(m => m.id === `temp-${message.id}` ? message : m);
            }
            return [...prev, message];
          }
          return prev;
        });
      };
      
      ws.onclose = () => {
        console.log('WebSocket连接已关闭');
        setIsConnected(false);
        // 尝试重新连接
        setTimeout(connectWebSocket, 3000);
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket错误:', error);
        ws.close();
      };
      
      wsRef.current = ws;
    };
    
    connectWebSocket();
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [clientId]);

  // 滚动到最新消息
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = () => {
    if (!input.trim() || !isConnected) return;
    
    const tempId = `temp-${Date.now()}`;
    // 创建临时用户消息
    const tempUserMessage: Message = {
      id: tempId,
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };
    
    // 立即显示临时消息
    setMessages(prev => [...prev, tempUserMessage]);
    
    // 发送消息到后端（不带ID）
    wsRef.current?.send(JSON.stringify({
      content: input
    }));
    setInput('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearHistory = async () => {
    try {
      await fetch(`http://localhost:8000/api/history/${clientId}`, {
        method: 'DELETE',
      });
      // 只需清空消息，不需要重新建立WebSocket连接
      setMessages([]);
    } catch (error) {
      console.error('清除历史记录失败:', error);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* 头部 */}
      <header className="bg-white shadow-sm p-4 flex justify-between items-center">
        <div className="flex items-center">
          <h1 className="text-xl font-bold text-gray-800">ServeBot</h1>
        </div>
        <button
          onClick={clearHistory}
          className="text-sm text-gray-600 hover:text-gray-900"
        >
          清除历史记录
        </button>
      </header>

      {/* 聊天区域 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-700 mb-2">我是ServeBot，很高兴见到你！</h2>
              <p className="text-gray-500">我可以帮助你解决问题，请告诉我你需要什么帮助。</p>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              } mb-4`}
            >
              {/* 机器人头像 */}
              {message.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-2">
                  <span className="text-blue-500 text-xs">Bot</span>
                </div>
              )}
              
              {/* 消息内容 */}
              <div
                className={`max-w-[70%] rounded-lg p-3 ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white rounded-tr-none'
                    : 'bg-white shadow-md rounded-tl-none'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div
                  className={`text-xs mt-1 ${
                    message.role === 'user' ? 'text-blue-100' : 'text-gray-400'
                  }`}
                >
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </div>
              
              {/* 用户头像 */}
              {message.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center ml-2">
                  <span className="text-white text-xs">You</span>
                </div>
              )}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* 输入区域 */}
      <div className="bg-white border-t p-4">
        <div className="flex items-center space-x-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="输入消息..."
            className="flex-1 border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            rows={1}
          />
          <button
            onClick={sendMessage}
            disabled={!isConnected || !input.trim()}
            className={`p-3 rounded-lg ${
              isConnected && input.trim()
                ? 'bg-blue-500 hover:bg-blue-600 text-white'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            发送
          </button>
        </div>
        <div className="text-xs text-gray-400 mt-1">
          {isConnected ? '已连接' : '连接中...'}
        </div>
      </div>
    </div>
  );
}