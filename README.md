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

## Docker 部署排错

- 如果你之前拉取的是旧版本，`Dockerfile` 里可能包含 `COPY static ./static`，在 `static/` 目录不存在时会构建失败。当前版本已移除该步骤。
- 建议先执行：

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

## 没有 HDHive API 时如何解析

可以，方式是**规则提取**而不是调用官方接口：

1. 直接把帖子正文或评论文本粘贴到输入框。
2. 如果页面是动态渲染/有反爬，先在浏览器中打开页面，使用“查看源代码”，把源码整体粘贴到输入框。
3. 工具会同时扫描：
   - 可见文本
   - HTML `href` 链接
   - `<script>` 内嵌文本

这样即使没有 API，只要 115 链接或提取码出现在页面源码中，仍可被识别。
