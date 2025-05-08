# CrystalEssence 部署指南

## 1. 环境要求

- Node.js >= 14.0.0
- Python >= 3.8
- MySQL >= 8.0
- Redis >= 6.0
- Nginx >= 1.18

## 2. 安装步骤

### 2.1 前端部署

```bash
# 安装依赖
npm install

# 构建生产版本
npm run build

# 启动服务
npm start
```

### 2.2 后端部署

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
flask db upgrade

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 2.3 Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## 3. 环境变量配置

创建 `.env` 文件并配置以下环境变量：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=crystal_shop
DB_USER=your_username
DB_PASSWORD=your_password

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# 支付配置
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_SECRET=your_paypal_secret
WECHAT_APP_ID=your_wechat_app_id
WECHAT_MCH_ID=your_wechat_mch_id
ALIPAY_APP_ID=your_alipay_app_id
ALIPAY_PRIVATE_KEY=your_alipay_private_key

# 邮件配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_email_password

# 分析配置
GA_TRACKING_ID=your_ga_tracking_id
FB_PIXEL_ID=your_fb_pixel_id
```

## 4. 安全配置

1. 启用 HTTPS
```bash
# 使用 Let's Encrypt 获取 SSL 证书
sudo certbot --nginx -d your-domain.com
```

2. 配置防火墙
```bash
# 开放必要端口
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22
```

3. 设置数据库安全
```sql
-- 创建受限用户
CREATE USER 'crystal_shop'@'localhost' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON crystal_shop.* TO 'crystal_shop'@'localhost';
FLUSH PRIVILEGES;
```

## 5. 监控和日志

1. 设置日志轮转
```bash
# 编辑 logrotate 配置
sudo nano /etc/logrotate.d/crystal_shop

# 添加以下内容
/var/log/crystal_shop/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```

2. 配置监控
```bash
# 安装 Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.30.0/prometheus-2.30.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*

# 配置 Prometheus
nano prometheus.yml
```

## 6. 备份策略

1. 数据库备份
```bash
# 创建备份脚本
nano /usr/local/bin/backup_db.sh

#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/var/backups/crystal_shop"
mkdir -p $BACKUP_DIR
mysqldump -u crystal_shop -p crystal_shop > $BACKUP_DIR/db_backup_$TIMESTAMP.sql
find $BACKUP_DIR -type f -mtime +7 -delete

# 设置定时任务
chmod +x /usr/local/bin/backup_db.sh
crontab -e
# 添加以下行
0 2 * * * /usr/local/bin/backup_db.sh
```

2. 文件备份
```bash
# 创建文件备份脚本
nano /usr/local/bin/backup_files.sh

#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/var/backups/crystal_shop"
SOURCE_DIR="/var/www/crystal_shop"
mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/files_backup_$TIMESTAMP.tar.gz $SOURCE_DIR
find $BACKUP_DIR -type f -mtime +7 -delete

# 设置定时任务
chmod +x /usr/local/bin/backup_files.sh
crontab -e
# 添加以下行
0 3 * * * /usr/local/bin/backup_files.sh
```

## 7. 性能优化

1. 配置 Nginx 缓存
```nginx
# 在 nginx.conf 中添加
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m use_temp_path=off;

# 在 server 块中添加
location /static/ {
    proxy_cache my_cache;
    proxy_cache_use_stale error timeout http_500 http_502 http_503 http_504;
    proxy_cache_valid 200 60m;
    expires 1d;
    add_header Cache-Control "public, no-transform";
}
```

2. 配置 Redis 缓存
```bash
# 编辑 redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
```

## 8. 故障恢复

1. 创建恢复脚本
```bash
nano /usr/local/bin/recover.sh

#!/bin/bash
# 停止服务
systemctl stop nginx
systemctl stop crystal_shop

# 恢复数据库
mysql -u crystal_shop -p crystal_shop < /var/backups/crystal_shop/latest_db_backup.sql

# 恢复文件
tar -xzf /var/backups/crystal_shop/latest_files_backup.tar.gz -C /var/www/

# 启动服务
systemctl start crystal_shop
systemctl start nginx
```

2. 设置监控告警
```bash
# 配置 Prometheus 告警规则
nano /etc/prometheus/rules/crystal_shop.yml

groups:
- name: crystal_shop
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: High error rate detected
      description: "Error rate is {{ $value }}"
```

## 9. 更新流程

1. 创建更新脚本
```bash
nano /usr/local/bin/update.sh

#!/bin/bash
# 拉取最新代码
cd /var/www/crystal_shop
git pull origin main

# 更新依赖
npm install
pip install -r requirements.txt

# 构建前端
npm run build

# 更新数据库
flask db upgrade

# 重启服务
systemctl restart crystal_shop
systemctl restart nginx
```

2. 设置更新检查
```bash
# 添加定时任务
crontab -e
# 添加以下行
0 4 * * * /usr/local/bin/update.sh
```

## 10. 维护检查清单

- [ ] 检查系统日志
- [ ] 检查数据库性能
- [ ] 检查磁盘空间
- [ ] 检查备份状态
- [ ] 检查安全更新
- [ ] 检查 SSL 证书有效期
- [ ] 检查监控系统
- [ ] 检查错误率
- [ ] 检查响应时间
- [ ] 检查缓存命中率 