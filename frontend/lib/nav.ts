export type Role = "admin"|"teacher"|"student";
const NAV = [
  { label: "แดชบอร์ด", href: "/dashboard", allow: ["admin","teacher","student"] },
  { label: "ผู้เรียน", href: "/admin/students", allow: ["admin","teacher"] },
  { label: "อุปกรณ์", href: "/admin/devices", allow: ["admin"] },
  { label: "ชั้นเรียนของฉัน", href: "/teacher/my-classes", allow: ["teacher"] },
  { label: "การเข้าเรียนของฉัน", href: "/student/my-attendance", allow: ["student"] },
];
export const navFor = (role: Role) => NAV.filter(i => i.allow.includes(role));