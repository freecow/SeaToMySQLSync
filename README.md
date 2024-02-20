# SeaToMySQLSync
SeaToMySQLSync is a tool designed to synchronize data from SeaTable to a MySQL database.

SeaToMySQLSync 是一个可将数据从 SeaTable 同步到 MySQL 数据库的工具。

## Features

- 数据同步：自动将数据从 SeaTable 同步到 MySQL。
- 字段映射：自定义 SeaTable 列到 MySQL 表字段的映射。
- 值转换：支持在同步前根据预定义的映射转换 SeaTable 值。
- 选择性插入：通过开关设置更新现有记录时同时插入新记录。
- 删除同步：通过开关设置，移除 MySQL 中不再存在于 SeaTable 的记录。

## 前提条件

- Python 3.6 或更高版本
- 具有 API 访问权限的 SeaTable 基地
- 一个 MySQL 数据库

## 安装

1. 克隆仓库到您的本地机器：

```bash
git clone https://github.com/yourusername/SeaToMySQLSync.git
cd SeaToMySQLSync
```

2. 安装所需的 Python 包：

```bash
pip install -r requirements.txt
```

3. 将 env.example 文件复制为 .env 并进行 SeaTable 和 MySQL 的配置：

```bash
cp env.example .env
```

4. 自定义 config.json 文件以定义数据同步行为，包括表名、字段映射和任何值转换.

## 运行

```bash
python main.py
```

## config.json

- SeaTable 配置：在 .env 文件中设置您的 SeaTable 服务器 URL 和 API 令牌。
- MySQL 配置：在 .env 文件中定义您的 MySQL 主机、端口、用户、密码和数据库。
- 同步规则：使用 config.json 定义源 SeaTable 表、目标 MySQL 表、字段映射以及任何额外选项，如 insert_missing_records 或 sync_deletion。

```json
{
  "source": {
    "table_name": "Customer Insights",
    "fields": [
      "Customer ID",
      "Customer Name",
      "Industry Type"
    ],
    "relation_field": "Customer Name"
  },
  "destination": {
    "table_name": "customer_data",
    "relation_field": "customer_name",
    "fields_mapping": {
      "Customer ID": "customer_id",
      "Customer Name": "customer_name",
      "Industry Type": "industry_type"
    }
  },
  "insert_missing_records": true,
  "sync_deletion": false,
  "mappings": {
    "Industry Type": {
      "Financial": "1",
      "Technology": "2",
      "Healthcare": "3"
    }
  }
}
```

- source: 定义来自 SeaTable 的数据源。
   - table_name: 将要同步数据的 SeaTable 表的名称。
   - fields: 您想要同步的 SeaTable 表中的字段名列表。
   - relation_field: 用于关联 SeaTable 和 MySQL 记录的字段。用于匹配记录以确定插入或更新。
- destination: 定义目标 MySQL 表配置。
   - table_name: 数据将被插入或更新的 MySQL 表的名称。
   - relation_field: 与 SeaTable relation_field 对应的 MySQL 表字段，用于匹配记录。
   - fields_mapping: SeaTable 字段名到 MySQL 列名的映射。这决定了如何将 SeaTable 字段的数据插入到 MySQL 列中。
- insert_missing_records: 设置为 true 时，允许工具将不存在的记录插入到 MySQL 中。为 false 时，仅更新现有记录。
- sync_deletion: 启用时，将从 MySQL 表中删除在 SeaTable 源中不再存在的记录。使用时请谨慎，以避免意外的数据丢失。
- mappings: 针对MySQL数据库中有字典支持的字段，采用字段映射，用于在插入到 MySQL 之前转换来自 SeaTable 的值。例如，将“Financial”转换为“1”，“Technology”转换为“2”等。
