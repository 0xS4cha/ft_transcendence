FROM    node:22-alpine AS builder

WORKDIR /app

COPY    package*.json ./
COPY    prisma ./prisma
COPY    . .

RUN     npm ci && \
        npx prisma generate && \
        npm run build

FROM    node:22-alpine

WORKDIR /app

COPY    package*.json ./
COPY    --from=builder /app/node_modules ./node_modules
COPY    --from=builder /app/generated ./generated
COPY    --from=builder /app/dist ./dist
COPY    --from=builder /app/prisma ./prisma
COPY    --from=builder /app/prisma.config.ts ./prisma.config.ts

RUN     npm ci --omit=dev

EXPOSE  3000

CMD     ["node", "dist/src/main.js"]