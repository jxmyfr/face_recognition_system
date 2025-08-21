import { NextResponse } from "next/server";
import { decode } from "jsonwebtoken";

export async function middleware(req: Request) {
  const url = new URL(req.url);
  const token = req.headers.get("cookie")?.match(/token=([^;]+)/)?.[1];
  if (!token && url.pathname !== "/login")
    return NextResponse.redirect(new URL("/login", req.url));

  if (token) {
    const { role } = decode(token) as any || {};
    const path = url.pathname;
    if (path.startsWith("/admin") && role !== "admin")
      return NextResponse.redirect(new URL("/403", req.url));
    if (path.startsWith("/teacher") && !["teacher","admin"].includes(role))
      return NextResponse.redirect(new URL("/403", req.url));
    if (path.startsWith("/student") && !["student","teacher","admin"].includes(role))
      return NextResponse.redirect(new URL("/403", req.url));
  }
  return NextResponse.next();
}
export const config = { matcher: ["/((?!_next|api|login|403|public).*)"] };