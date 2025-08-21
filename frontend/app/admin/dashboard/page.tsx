// app/admin/dashboard/page.tsx
// 'use client'

import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { toast } from 'sonner';
import Image from 'next/image';

// const menuItems = [
//   { label: 'แดชบอร์ด', icon: '/frontend/public/dashboard.svg', href: '/admin/dashboard' },
//   { label: 'ข้อมูลการเข้าเรียน', icon: '/icons/attendances.svg', href: '/admin/attendances' },
//   { label: 'จัดการข้อมูลนักเรียน', icon: '/icons/students.svg', href: '/admin/students' },
//   { label: 'จัดการข้อมูลวิชา', icon: '/icons/subjects.svg', href: '/admin/subjects' },
//   { label: 'จัดการชั้นเรียน', icon: '/icons/rooms.svg', href: '/admin/rooms' },
//   { label: 'รายงาน', icon: '/icons/reports.svg', href: '/admin/reports' },
//   { label: 'ตั้งค่า', icon: '/icons/settings.svg', href: '/admin/settings' },
// ];

interface AttendanceSummary {
  total_students: number;
  present_today: number;
  absent_today: number;
  late_today: number;
}

export default function DashboardPage() {
  const [students, setStudents] = useState([]);
  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/students`)
      .then(res => res.json())
      .then(data => setStudents(data));
  }, []);

  return (
    <main className="p-4">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <ul>
        {students.map((s: any) => (
          <li key={s.id}>{s.name}</li>
        ))}
      </ul>
    </main>
  );
}

