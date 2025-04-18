import NextAuth from "next-auth";
import type { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions: NextAuthOptions = {
  debug: true, // 开启调试模式
  providers: [
    CredentialsProvider({
      name: "邮箱登录",
      credentials: {
        email: { label: "邮箱", type: "email", placeholder: "请输入邮箱" },
        password: { label: "密码", type: "password", placeholder: "请输入密码" }
      },
      async authorize(credentials) {
        // 简化登录逻辑，用于测试
        if (credentials?.email === "test@example.com" && credentials?.password === "password") {
          return {
            id: "1",
            name: "测试用户",
            email: "test@example.com",
            accessToken: "mock_token_123"
          };
        }
        
        // 如果需要连接后端，取消注释以下代码
        /*
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              email: credentials?.email,
              password: credentials?.password,
            }),
          });

          const user = await response.json();

          if (response.ok && user) {
            return {
              id: user.id,
              name: user.name,
              email: user.email,
              accessToken: user.accessToken,
            };
          }
        } catch (error) {
          console.error('登录验证错误:', error);
        }
        */
        
        return null;
      }
    }),
  ],
  callbacks: {
    async jwt({ token, user ,account}) {
      if (user) {
        token.accessToken = account?.access_token
        token.userId = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.name = token.userId as string;
      }
      return session;
    },
  },
  pages: {
    signIn: "/login",
  },
};

export const { handlers, auth, signIn, signOut } = NextAuth(authOptions);