from bs4 import SoupStrainer, BeautifulSoup

ALLOWED_TAGS = [
    # 核心文本结构
    "h1", "h2", "h3", "h4", "h5", "h6",  # 标题
    "p", "br", "hr",  # 段落与分隔
    "ul", "ol", "li",  # 列表
    "pre", "code", "blockquote",  # 代码和引用
    "table", "thead", "tbody", "tr", "th", "td",  # 表格
    # 语义化标签
    "div", "span", "article", "section", "main", "header", "footer",
    # 其他有用内容
    "a", "img",  # 链接和图片（需要控制属性）
    "strong", "em", "b", "i", "u"  # 文本强调
]
ALLOWED_ATTRIBUTES = {
    "a": ["href"],  # 保留链接地址
    "img": ["alt", "src"],  # 保留图片描述和路径
    "code": ["class"],  # 可选：保留代码块语言类型（如 class="python"）
    "table": ["border"]  # 可选：表格基础属性
}


def clean_html(html):
    # 使用 SoupStrainer 提升解析性能（仅处理白名单标签）
    strainer = SoupStrainer(ALLOWED_TAGS)
    soup = BeautifulSoup(html, "lxml", parse_only=strainer)

    # 删除所有非白名单属性
    for tag in soup.find_all(True):
        # 获取当前标签允许的属性列表
        allowed_attrs = ALLOWED_ATTRIBUTES.get(tag.name, [])
        attrs = list(tag.attrs.items())  # 转换为列表避免遍历时修改问题

        for attr, value in attrs:
            attr_lower = attr.lower()
            # 删除条件：属性不在白名单 或 值为空/纯空格
            if (attr_lower not in allowed_attrs) or (str(value).strip() == ""):
                del tag[attr]

    # 提取文本并清理（保留段落结构）
    text = soup.get_text(separator="\n", strip=True)
    # 后处理：合并多余空行和空格
    # text = re.sub(r'\n{3,}', '\n\n', text)  # 超过2个换行合并为2个
    # text = re.sub(r' {2,}', ' ', text)  # 多个空格合并为1个
    return text
