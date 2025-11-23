# Checklist Deploy Django lên LSWS

## Trước Khi Deploy

- [ ] Chạy `python manage.py collectstatic`
- [ ] Tạo file `requirements.txt`
- [ ] Test tất cả tính năng trên local
- [ ] Backup database hiện tại

## Cấu Hình Settings

- [ ] Đổi `DEBUG = False`
- [ ] Cập nhật `ALLOWED_HOSTS` với domain thực
- [ ] Tạo `SECRET_KEY` mới cho production
- [ ] Cập nhật `CSRF_TRUSTED_ORIGINS` với domain HTTPS
- [ ] Kiểm tra `STATIC_ROOT` và `STATIC_URL`

## Trên Server

- [ ] Upload code lên server
- [ ] Tạo virtual environment
- [ ] Cài đặt dependencies: `pip install -r requirements.txt`
- [ ] Chạy migrations: `python manage.py migrate`
- [ ] Tạo superuser: `python manage.py createsuperuser`
- [ ] Thu thập static files: `python manage.py collectstatic`
- [ ] Phân quyền files và folders

## Cấu Hình LiteSpeed

- [ ] Tạo Virtual Host
- [ ] Cấu hình External App (LSAPI)
- [ ] Thiết lập Script Handler
- [ ] Cấu hình Context cho WSGI
- [ ] Cấu hình Context cho Static files
- [ ] Cấu hình Context cho Media files
- [ ] Thiết lập Rewrite Rules
- [ ] Restart LiteSpeed

## Kiểm Tra

- [ ] Truy cập website qua domain
- [ ] Kiểm tra static files load đúng
- [ ] Test đăng nhập
- [ ] Test CRUD hội nghị
- [ ] Test CRUD điểm cầu
- [ ] Test CRUD thành phần
- [ ] Test tìm kiếm
- [ ] Test dashboard/thống kê
- [ ] Kiểm tra responsive trên mobile

## Bảo Mật

- [ ] Cài đặt SSL certificate
- [ ] Bật HTTPS redirect
- [ ] Kiểm tra CSRF protection
- [ ] Giới hạn quyền truy cập files
- [ ] Thiết lập backup tự động
- [ ] Cấu hình firewall

## Sau Deploy

- [ ] Monitor error logs
- [ ] Thiết lập monitoring/alerting
- [ ] Tạo tài liệu hướng dẫn sử dụng
- [ ] Train người dùng
