'use client';

import {useEffect, useRef, useState} from 'react';
import {v4 as uuidv4} from 'uuid';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
    interrupt_flag: boolean
}

// 新增会话接口
interface Conversation {
    id: string;
    title: string;
    createdAt: string;
}

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isConnected, setIsConnected] = useState(false);
    const [clientId, setClientId] = useState<string | null>(null); // 当前活跃的会话ID
    const [conversations, setConversations] = useState<Conversation[]>([]); // 用户的所有会话
    const [userId, setUserId] = useState<string>("user-123"); // 模拟用户ID，实际应从登录系统获取
    const wsRef = useRef<WebSocket | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // 初始化加载用户会话列表
    useEffect(() => {
        if (userId) {
            // 实际环境中应该从后端API获取用户的会话列表
            fetchUserConversations();
        }
    }, [userId]);

    // 模拟从后端获取用户会话列表
    const fetchUserConversations = async () => {
        try {
            // 实际环境中应该调用API: `/api/users/${userId}/conversations`
            // 这里模拟一些数据
            const mockConversations: Conversation[] = [
                // 如果有历史会话，可以在这里显示
            ];
            setConversations(mockConversations);
        } catch (error) {
            console.error('获取会话列表失败:', error);
        }
    };

    // 新建对话
    const createNewConversation = () => {
        const newClientId = uuidv4();
        const newConversation: Conversation = {
            id: newClientId,
            title: `新对话 ${new Date().toLocaleString()}`,
            createdAt: new Date().toISOString()
        };

        setConversations(prev => [...prev, newConversation]);
        setClientId(newClientId);
        setMessages([]); // 清空当前消息

        // 实际环境中应该调用API保存新会话
        // saveConversation(userId, newConversation);
    };

    // 切换到指定会话
    const switchConversation = (conversationId: string) => {
        if (clientId === conversationId) return;

        // 关闭当前WebSocket连接
        if (wsRef.current) {
            wsRef.current.close();
        }

        setClientId(conversationId);
        setMessages([]); // 清空当前消息，新的消息会通过WebSocket加载
    };

    // 建立WebSocket连接（只在clientId变化时连接）
    useEffect(() => {
        if (!clientId) return;

        const connectWebSocket = () => {
            try {
                const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);

                ws.onopen = () => {
                    console.log('WebSocket连接已建立');
                    setIsConnected(true);
                };

                ws.onmessage = (event) => {
                    try {
                        const message = JSON.parse(event.data);
                        console.log('收到消息:', message);

                        setMessages((prev) => {
                            // 如果不是替换临时消息的情况，检查是否已存在相同ID的消息
                            if (!prev.some(m => m.id === message.id)) {
                                return [...prev, message];
                            }
                            return prev;
                        });
                    } catch (error) {
                        console.error('消息解析错误:', error);
                    }
                };

                ws.onclose = (event) => {
                    console.log('WebSocket连接已关闭', event.code, event.reason);
                    setIsConnected(false);
                    if (clientId && !event.wasClean) { // 只在非正常关闭时重连
                        setTimeout(connectWebSocket, 3000);
                    }
                };

                ws.onerror = (error) => {
                    console.error('WebSocket错误:', error);
                    // 添加更详细的错误日志
                    console.error('WebSocket错误详情:', {
                        message: '连接失败',
                        url: `ws://localhost:8000/ws/${clientId}`,
                        readyState: ws.readyState
                    });
                    setIsConnected(false);
                    ws.close();
                };

                wsRef.current = ws;
            } catch (error) {
                console.error('WebSocket初始化错误:', error);
                setIsConnected(false);
                setTimeout(connectWebSocket, 3000);
            }
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
        messagesEndRef.current?.scrollIntoView({behavior: 'smooth'});
    }, [messages]);

    const sendMessage = () => {
        if (!input.trim() || !isConnected || !clientId) return;

        try {
            const latestInterruptFlag = messages.length > 0
                ? messages[messages.length - 1].interrupt_flag
                : null;
            // 发送消息到服务端，使用与后端ChatRequest DTO匹配的格式
            wsRef.current?.send(JSON.stringify({
                user_id: userId,
                content: input,
                interrupt_flag: latestInterruptFlag
            }));
            setInput('');
        } catch (error) {
            console.error('消息发送失败:', error);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    // 修改clearHistory函数，支持删除会话
    const clearHistory = async () => {
        if (!clientId) return;

        try {
            await fetch(`http://localhost:8000/api/history/${clientId}`, {
                method: 'DELETE',
            });
            setMessages([]);

            // 可选：从会话列表中移除该会话
            // setConversations(prev => prev.filter(conv => conv.id !== clientId));
            // setClientId(conversations.length > 0 ? conversations[0].id : null);
        } catch (error) {
            console.error('清除历史记录失败:', error);
        }
    };

    // 删除会话
    const deleteConversation = async (conversationId: string) => {
        try {
            // 实际环境中应该调用API删除会话
            // await fetch(`/api/users/${userId}/conversations/${conversationId}`, {
            //     method: 'DELETE',
            // });

            setConversations(prev => prev.filter(conv => conv.id !== conversationId));

            // 如果删除的是当前会话，切换到其他会话或清空
            if (clientId === conversationId) {
                const remainingConversations = conversations.filter(conv => conv.id !== conversationId);
                if (remainingConversations.length > 0) {
                    switchConversation(remainingConversations[0].id);
                } else {
                    setClientId(null);
                    setMessages([]);
                }
            }
        } catch (error) {
            console.error('删除会话失败:', error);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gray-50">
            {/* 头部 */}
            <header className="bg-white shadow-sm p-4 flex justify-between items-center">
                <div className="flex items-center">
                    <h1 className="text-xl font-bold text-gray-800">ServeBot</h1>
                </div>
                <div className="flex space-x-2">
                    <button
                        onClick={createNewConversation}
                        className="text-sm bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded"
                    >
                        新建对话
                    </button>
                    {clientId && (
                        <button
                            onClick={clearHistory}
                            className="text-sm text-gray-600 hover:text-gray-900"
                        >
                            清除历史记录
                        </button>
                    )}
                </div>
            </header>

            {/* 主体区域 - 添加侧边栏 */}
            <div className="flex flex-1 overflow-hidden">
                {/* 会话列表侧边栏 */}
                <div className="w-64 bg-gray-100 overflow-y-auto p-2 border-r">
                    <div className="mb-2 text-sm font-medium text-gray-500">我的会话</div>
                    {conversations.length === 0 ? (
                        <div className="text-center text-gray-400 text-sm py-4">
                            暂无会话，点击&quot;新建对话&quot;开始
                        </div>
                    ) : (
                        <div className="space-y-1">
                            {conversations.map(conv => (
                                <div
                                    key={conv.id}
                                    className={`flex justify-between items-center p-2 rounded cursor-pointer ${
                                        clientId === conv.id ? 'bg-blue-100' : 'hover:bg-gray-200'
                                    }`}
                                    onClick={() => switchConversation(conv.id)}
                                >
                                    <div className="truncate text-sm">{conv.title}</div>
                                    <button
                                        className="text-gray-400 hover:text-red-500"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            deleteConversation(conv.id);
                                        }}
                                    >
                                        ×
                                    </button>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* 聊天区域 */}
                <div className="flex-1 flex flex-col">
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
                                    }`}
                                >
                                    <div
                                        className={`max-w-[80%] rounded-lg p-4 ${
                                            message.role === 'user'
                                                ? 'bg-blue-500 text-white'
                                                : 'bg-white shadow-md'
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
                                </div>
                            ))
                        )}
                        <div ref={messagesEndRef}/>
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
                                disabled={!clientId}
                            />
                            <button
                                onClick={sendMessage}
                                disabled={!clientId || !input.trim()} // 仅根据会话ID和输入内容判断
                                className={`p-3 rounded-lg ${
                                    clientId && input.trim()
                                        ? 'bg-blue-500 hover:bg-blue-600 text-white'
                                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                                }`}
                            >
                                发送
                            </button>
                        </div>
                        <div className="text-xs text-gray-400 mt-1">
                            {!clientId ? '请先创建对话' : isConnected ? '已连接' : '连接中...'}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}