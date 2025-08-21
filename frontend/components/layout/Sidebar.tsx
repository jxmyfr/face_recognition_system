'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Image from 'next/image';

const menuItems = [
  { label: 'แดชบอร์ด', icon: '/dashboard.svg', href: '/admin/dashboard' },
  { label: 'ข้อมูลการเข้าเรียน', icon: '/attendances.svg', href: '/admin/attendances' },
  { label: 'จัดการข้อมูลนักเรียน', icon: '/students.svg', href: '/admin/students' },
  { label: 'จัดการข้อมูลวิชา', icon: '/subjects.svg', href: '/admin/subjects' },
  { label: 'จัดการชั้นเรียน', icon: '/rooms.svg', href: '/admin/rooms' },
  { label: 'รายงาน', icon: '/reports.svg', href: '/admin/reports' },
  { label: 'ตั้งค่า', icon: '/settings.svg', href: '/admin/settings' },
];

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);
  const pathname = usePathname();

  return (
    <div
      className={`${
        isOpen ? 'w-64' : 'w-20'
      } bg-[#15161B] text-white h-screen transition-all duration-300 fixed z-50 flex flex-col`}
    >
      <div className="flex items-center justify-between px-4 py-5">
        <h1
          className={`text-lg font-bold tracking-wide transition-opacity ${
            isOpen ? 'opacity-100' : 'opacity-0'
          }`}
        >
          FaceAttend
        </h1>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="p-1 rounded hover:bg-white/10"
          title="Toggle sidebar"
        >
          <Image src="/menu.svg" alt="menu" width={20} height={20} />
        </button>
      </div>

      <nav className="flex flex-col gap-1 px-2">
        {menuItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-md transition-colors ${
                isActive ? 'bg-[#2c2f38]' : 'hover:bg-[#2c2f38]/60'
              }`}
            >
              <Image
                src={item.icon}
                alt={item.label}
                width={24}
                height={24}
              />
              <span
                className={`text-sm font-medium transition-all ${
                  isOpen ? 'opacity-100' : 'opacity-0 scale-90'
                }`}
              >
                {item.label}
              </span>
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto px-4 py-3 border-t border-white/10 text-xs text-gray-400 text-center">
        <span className={`${isOpen ? 'block' : 'hidden'}`}>&copy; 2025 FaceAttend</span>
      </div>
    </div>
  );
}