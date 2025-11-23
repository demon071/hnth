#!/bin/bash
# Script để sửa quyền database cho LiteSpeed Web Server

# Thay đổi đường dẫn này thành đường dẫn thực tế của project trên server
PROJECT_PATH="/home/username/conference_manager"

# Thay đổi user này thành user chạy LiteSpeed (thường là nobody, lsadm, hoặc www-data)
LSWS_USER="nobody"
LSWS_GROUP="nobody"

echo "Đang sửa quyền cho database..."

# Cấp quyền cho thư mục project
chmod 775 "$PROJECT_PATH"
chown $LSWS_USER:$LSWS_GROUP "$PROJECT_PATH"

# Cấp quyền cho file database
chmod 664 "$PROJECT_PATH/db.sqlite3"
chown $LSWS_USER:$LSWS_GROUP "$PROJECT_PATH/db.sqlite3"

# Cấp quyền cho thư mục staticfiles
chmod -R 755 "$PROJECT_PATH/staticfiles"
chown -R $LSWS_USER:$LSWS_GROUP "$PROJECT_PATH/staticfiles"

# Cấp quyền cho thư mục media (nếu có)
if [ -d "$PROJECT_PATH/media" ]; then
    chmod -R 775 "$PROJECT_PATH/media"
    chown -R $LSWS_USER:$LSWS_GROUP "$PROJECT_PATH/media"
fi

echo "Hoàn tất! Quyền đã được cập nhật."
echo "Kiểm tra quyền:"
ls -la "$PROJECT_PATH/db.sqlite3"
