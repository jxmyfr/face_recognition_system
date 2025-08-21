import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from 'sonner'
import Sidebar from '@/components/layout/Sidebar';
import { Inter } from 'next/font/google';



const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <aside className="fixed left-0 top-0 w-60 h-full bg-gray-800 text-white p-4">
          <h2 className="font-bold text-lg mb-4">เมนู</h2>
          <ul>
            <li><a href="/admin/dashboard">📊 Dashboard</a></li>
            <li><a href="/admin/students">👤 นักเรียน</a></li>
          </ul>
        </aside>
        <main className="ml-60 p-4">{children}</main>
      </body>
    </html>
  );
}



