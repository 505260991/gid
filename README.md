# HDHive + 115 链接提取网站

一个可独立部署的 Web 项目：

- HDHive 页面链接识别
- 115 网盘分享链接自动提取
- 提取码自动识别
- 一键复制单条/全部结果

> 仅用于合规场景下的文本整理，不绕过任何认证或访问控制。

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

访问：`http://localhost:8080`

## Docker 一键部署

```bash
docker compose up -d --build
```

## API

`POST /api/unlock`

请求示例：

```json
{
  "url": "https://example.com/post",
  "text": "115链接 https://115.com/s/abc123 提取码: d9x2"
}
```

返回示例：

```json
{
  "count": 1,
  "items": [
    {
      "panUrl": "https://115.com/s/abc123",
      "code": "d9x2",
      "quickCopy": "https://115.com/s/abc123 提取码: d9x2"
    }
  ],
  "hdhiveLinks": []
}
```
