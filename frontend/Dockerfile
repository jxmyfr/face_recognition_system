# 1. ติดตั้ง dependencies
# FROM node:18.20-alpine AS deps
# WORKDIR /app

# # คัดลอกไฟล์ที่จำเป็นสำหรับติดตั้ง
# COPY package.json package-lock.json ./
# RUN npm ci

# # 2. Build แอปด้วย .env.production
# FROM node:18.20-alpine AS builder
# WORKDIR /app

# # คัดลอกไฟล์ทั้งหมด (รวม .env.production)
# COPY . .

# # คัดลอก node_modules จากขั้นตอน deps
# COPY --from=deps /app/node_modules ./node_modules

# # ⚠️ ตรวจสอบให้แน่ใจว่า .env.production อยู่ในโปรเจกต์ และถูกคัดลอกเข้ามา
# # แล้ว Build
# RUN npm run build

# # 3. รัน production server
# FROM node:18.20-alpine AS runner
# WORKDIR /app

# ENV NODE_ENV=production

# # คัดลอกไฟล์ที่ build แล้ว + production assets
# COPY --from=builder /app/public ./public
# COPY --from=builder /app/.next ./.next
# COPY --from=builder /app/node_modules ./node_modules
# COPY --from=builder /app/package.json ./package.json

# # เพิ่ม .env.production เข้าไปใน container ด้วย (optional, เผื่อบาง env ไม่ถูก hardcoded)
# COPY --from=builder /app/.env.production ./.env.production

# EXPOSE 3000

# CMD ["npm", "start"]


# =========================
# 1) Deps (ติดตั้ง dependences)
# =========================
FROM node:20-alpine AS deps
WORKDIR /app
# สำหรับไลบรารีที่พึ่งพา glibc (เช่น sharp)
RUN apk add --no-cache libc6-compat
COPY package.json package-lock.json ./
# ใช้ npm ci เพื่อความ reproducible
RUN npm ci

# =========================
# 2) Builder (build Next.js)
# =========================
FROM node:20-alpine AS builder
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
RUN apk add --no-cache libc6-compat
# ใช้ node_modules จากขั้น deps เพื่อ cache ดีขึ้น
COPY --from=deps /app/node_modules ./node_modules
# คัดลอกโค้ดทั้งหมด (อย่าใส่ .env.* ลงอิมเมจ)
COPY . .
# สร้างเป็นโหมด standalone เพื่อลดขนาด runtime
# (ต้องตั้งค่าใน next.config.js: module.exports = { output: 'standalone' })
RUN npm run build

# =========================
# 3) Runner (โปรดักชัน)
# =========================
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
RUN apk add --no-cache libc6-compat

# รันแบบ non-root เพื่อความปลอดภัย
RUN addgroup -g 1001 -S nodejs \
 && adduser  -u 1001 -S nextjs -G nodejs
USER nextjs

# คัดลอกเฉพาะสิ่งที่จำเป็นสำหรับรันจริง (เล็กและปลอดภัยกว่า)
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# ถ้ามี i18n locales ให้คัดลอกด้วย (ปลดคอมเมนต์บรรทัดล่าง)
# COPY --from=builder /app/public/locales ./public/locales

EXPOSE 3000
# (ถ้าคุณมี health endpoint อาจเพิ่ม HEALTHCHECK ได้)
# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
#   CMD wget -qO- http://localhost:3000/ || exit 1

CMD ["node", "server.js"]
