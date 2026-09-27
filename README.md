# gurdung

> 灵感“咕咚”一下冒出来，随手记下，不丢。

**gurdung** 是一个轻量级的终端灵感速记与待办管理工具。它用纯 Python 标准库实现，零第三方依赖，安装即可用。

当你灵光一闪、随手想到一个点子，或者列了一堆待办，都可以在终端里用一条命令记下来，再也不怕忘记。

## 功能特性

- 💡 **灵感速记**：随时记录一闪而过的想法
- ✅ **待办管理**：添加、完成、删除待办事项
- 🗂️ **本地持久化**：数据保存在 `~/.gurdung/data.json`，不依赖任何云端服务
- 🎨 **彩色输出**：终端里清晰区分状态与类型
- 🐍 **纯标准库**：零第三方依赖，Python 3.8+ 开箱即用

## 安装

```bash
# 方式一：直接安装（推荐）
pip install .

# 方式二：不安装，直接用
python -m gurdung --help
```

## 快速开始

### 灵感速记

```bash
# 记一条灵感
gurdung note add "给博客加一个暗色模式"

# 查看所有灵感
gurdung note list

# 删除第 2 条灵感
gurdung note rm 2
```

### 待办管理

```bash
# 添加待办
gurdung todo add "写周报"
gurdung todo add "预约体检"

# 查看待办
gurdung todo list

# 把第 1 条待办标记为完成
gurdung todo done 1

# 删除第 2 条待办
gurdung todo rm 2

# 清空所有待办
gurdung todo clear
```

### 统计

```bash
gurdung stats
```

## 数据存储

所有数据保存在 `~/.gurdung/data.json`，JSON 格式，方便备份与迁移：

```bash
# 备份
cp ~/.gurdung/data.json ~/gurdung-backup.json
```

## 开发

```bash
# 运行测试
python -m unittest discover tests

# 手动试用
python -m gurdung note add "hello gurdung"
```

## 许可证

[MIT](LICENSE)
