# Khắc Phục Lỗi "attempt to write a readonly database"

## Nguyên nhân
Lỗi này xảy ra khi:
1. File `db.sqlite3` không có quyền ghi
2. Thư mục chứa database không có quyền ghi
3. User chạy LiteSpeed không có quyền truy cập

## Giải pháp

### Cách 1: Sửa Quyền Thủ Công (Khuyến nghị)

Chạy các lệnh sau trên server (qua SSH):

```bash
# Di chuyển đến thư mục project
cd /home/username/conference_manager

# Kiểm tra user đang chạy LiteSpeed
ps aux | grep lshttpd

# Thường là: nobody, lsadm, hoặc www-data
# Thay YOUR_LSWS_USER bằng user thực tế

# Cấp quyền cho thư mục project
sudo chmod 775 /home/username/conference_manager
sudo chown YOUR_LSWS_USER:YOUR_LSWS_USER /home/username/conference_manager

# Cấp quyền cho file database
sudo chmod 664 /home/username/conference_manager/db.sqlite3
sudo chown YOUR_LSWS_USER:YOUR_LSWS_USER /home/username/conference_manager/db.sqlite3

# Restart LiteSpeed
sudo /usr/local/lsws/bin/lswsctrl restart
```

### Cách 2: Sử dụng Script

1. Upload file `fix_permissions.sh` lên server
2. Sửa đường dẫn và user trong script
3. Chạy script:

```bash
chmod +x fix_permissions.sh
sudo ./fix_permissions.sh
```

### Cách 3: Kiểm Tra Chi Tiết

```bash
# Kiểm tra quyền hiện tại
ls -la /home/username/conference_manager/db.sqlite3

# Kết quả mong muốn:
# -rw-rw-r-- 1 nobody nobody 131072 Nov 23 22:00 db.sqlite3

# Kiểm tra quyền thư mục
ls -ld /home/username/conference_manager

# Kết quả mong muốn:
# drwxrwxr-x 8 nobody nobody 4096 Nov 23 22:00 /home/username/conference_manager
```

## Giải Pháp Thay Thế: Sử dụng PostgreSQL/MySQL

Nếu vấn đề vẫn tiếp diễn, khuyến nghị chuyển sang database server:

### Cài đặt PostgreSQL (Khuyến nghị cho Production)

1. **Cài đặt psycopg2:**
```bash
pip install psycopg2-binary
```

2. **Cập nhật settings.py:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'conference_db',
        'USER': 'conference_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Tạo database:**
```bash
sudo -u postgres psql
CREATE DATABASE conference_db;
CREATE USER conference_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE conference_db TO conference_user;
\q
```

4. **Migrate:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

## Kiểm Tra Sau Khi Sửa

1. Truy cập website
2. Thử đăng nhập
3. Thử tạo một hội nghị mới
4. Kiểm tra error log: `/usr/local/lsws/logs/error.log`

## Lưu Ý Bảo Mật

- **KHÔNG** cấp quyền 777 cho database
- Chỉ cấp quyền tối thiểu cần thiết (664 cho file, 775 cho thư mục)
- Đảm bảo chỉ LiteSpeed user có quyền ghi
- Backup database trước khi thay đổi quyền

## Debug

Nếu vẫn gặp lỗi, kiểm tra:

```bash
# Xem log chi tiết
tail -f /usr/local/lsws/logs/error.log

# Kiểm tra SELinux (nếu có)
getenforce
# Nếu là Enforcing, có thể cần:
sudo setenforce 0  # Tạm thời tắt để test
```
