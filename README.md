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

## config.json示例

- 同步规则：使用 config.json 定义源 SeaTable 表、目标 MySQL 表、字段映射以及任何额外选项，如 insert_missing_records 或 sync_deletion参数。

```json
{
  "source": {
    "table_name": "客户口径",
    "fields": [
      "客户编号",
      "客户名称",
      "客户性质"
    ],
    "relation_field": "客户名称"
  },
  "destination": {
    "table_name": "project_total_contract",
    "relation_field": "customer_units",
    "fields_mapping": {
      "客户编号": "customer_code",
      "客户名称": "customer_units",
      "客户性质": "customer_type"
    }
  },
  "mappings": {
    "客户性质": {
      "政府部门": "0",
      "事业单位": "10",
      "国有企业": "20",
      "民营企业": "30"
    }
  },
  "insert_missing_records": true,
  "sync_deletion": false,
}
```

- source: 定义来自 SeaTable 的数据源。
   - table_name: 将要同步数据的 SeaTable 表的名称，如表名为客户口径。
   - fields: 您想要同步的 SeaTable 表中的字段名列表，如客户编号、客户名称、客户性质。
   - relation_field: 用于关联 SeaTable 和 MySQL表间的字段，用于匹配记录以确定插入或更新，如客户名称。
- destination: 定义目标 MySQL 表配置。
   - table_name: 数据将被插入或更新的 MySQL 表的名称，如表名为project_total_contract。
   - relation_field: 与 SeaTable relation_field 对应的 MySQL 表字段，用于匹配记录，如customer_units。
   - fields_mapping: SeaTable 字段名到 MySQL 列名的映射，决定了如何将 SeaTable 字段的数据插入到 MySQL 列中，左边为Seatable字段名，右面为MySQL的字段名。
- mappings: 专门针对MySQL数据库中有字典表支持的字段，采用字段映射，用于在插入到 MySQL 之前转换来自 SeaTable 的值。例如，我们在MySQL中对客户性质进行字典编码，要求将“政府部门”转换为“0”，“事业单位”转换为“10”等。
- insert_missing_records: 该参数设置为 true 时，允许程序将不存在的记录插入到 MySQL 中，设置为 false 时，仅更新已有记录。
- sync_deletion: 该参数设置为 true 时，将从 MySQL 表中删除在 SeaTable 源中不再存在的记录，使用时请谨慎，以避免意外的数据丢失。


## .env示例

- SeaTable 配置：在 .env 文件中设置您的 SeaTable 服务器 URL 和 API 令牌，API 令牌针对Seatable表格，具体获取方法请参考Seatable官方文档。
- MySQL 配置：在 .env 文件中定义您的 MySQL 主机、端口、用户、密码和数据库。

```json
# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_mysql_username_here
MYSQL_PASSWORD=your_mysql_password_here
MYSQL_DB=your_mysql_database_name_here

# SeaTable API Configuration
SEATABLE_SERVER_URL=https://cloud.seatable.io
SEATABLE_API_TOKEN=your_seatable_api_token_here
```
