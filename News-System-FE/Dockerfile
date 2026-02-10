# --- Stage 1: Build Stage ---
FROM node:20-alpine AS build-stage

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file định nghĩa package trước để tận dụng Docker cache
COPY package*.json ./

# Cài đặt dependencies (sử dụng npm ci để đảm bảo tính nhất quán)
RUN npm ci

# Copy toàn bộ mã nguồn và build
COPY . .
RUN npm run build

# --- Stage 2: Production Stage ---
FROM nginx:stable-alpine AS production-stage

# Hardening: Tạo user không có quyền root để chạy Nginx
# Alpine mặc định có user 'nginx', chúng ta sẽ tinh chỉnh quyền hạn.

# Copy file cấu hình Nginx tùy chỉnh
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy thành phẩm từ build-stage vào thư mục phục vụ của Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Hardening: Thay đổi quyền sở hữu thư mục để user không phải root có thể truy cập
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /usr/share/nginx/html /var/cache/nginx /var/log/nginx /etc/nginx/conf.d

# Chuyển sang user nginx (không có quyền root)
USER nginx

# Expose port (Nginx chạy ở port 8080 thay vì 80 để không cần quyền root)
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]