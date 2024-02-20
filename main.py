import json
import pymysql
from seatable_api import Base
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 读取数据库配置
mysql_config = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT')),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'db': os.getenv('MYSQL_DB')
}

seatable_config = {
    'server_url': os.getenv('SEATABLE_SERVER_URL'),
    'api_token': os.getenv('SEATABLE_API_TOKEN')
}

# 读取同步配置
with open('config.json', 'r') as f:
    config = json.load(f)

def fetch_seatable_data(base, table_name):
    """Fetch data from SeaTable based on the specified table name."""
    return base.list_rows(table_name)

def apply_mappings(row, field_mappings, value_mappings):
    """Apply mappings to a row of data."""
    mapped_row = {}
    for source_field, dest_field in field_mappings.items():
        original_value = row.get(source_field, "")
        if source_field in value_mappings:
            mapped_value = value_mappings[source_field].get(original_value, original_value)
        else:
            mapped_value = original_value
        mapped_row[dest_field] = mapped_value
    return mapped_row

def sync_seatable_to_mysql():
    base = Base(seatable_config['api_token'], seatable_config['server_url'])
    base.auth()

    # Fetch data from SeaTable
    seatable_data = fetch_seatable_data(base, config['source']['table_name'])

    # Connect to MySQL
    connection = pymysql.connect(**mysql_config, cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Get existing MySQL data for comparison
    #cursor.execute(f"SELECT {config['destination']['relation_field']} FROM {config['destination']['table_name']}")
    #existing_records = {row[config['destination']['relation_field']] for row in cursor.fetchall()}

    # insert_missing不起作用，因为ON DUPLICATE KEY UPDATE已经可以处理插入和更新逻辑
    insert_missing = config.get('insert_missing_records', False)
    sync_deletion = config.get('sync_deletion', False)

    # Prepare SQL statements
    fields_sql = ", ".join(config['destination']['fields_mapping'].values())
    placeholders_sql = ", ".join(["%s"] * len(config['destination']['fields_mapping']))
    on_duplicate_key_update = ", ".join([f"{field} = VALUES({field})" for field in config['destination']['fields_mapping'].values()])

    try:
        # Check existence for insert_missing logic
        existing_records_check_sql = f"SELECT {config['destination']['relation_field']} FROM {config['destination']['table_name']}"
        cursor.execute(existing_records_check_sql)
        existing_records = {row[config['destination']['relation_field']] for row in cursor.fetchall()}

        for row in seatable_data:
            mapped_row = apply_mappings(row, config['destination']['fields_mapping'], config.get('mappings', {}))
            relation_value = mapped_row[config['destination']['relation_field']]

            if relation_value in existing_records or insert_missing:
                # Insert or update the record
                insert_update_sql = f"INSERT INTO {config['destination']['table_name']} ({fields_sql}) VALUES ({placeholders_sql}) ON DUPLICATE KEY UPDATE {on_duplicate_key_update}"
                values = [mapped_row[field] for field in config['destination']['fields_mapping'].values()]
                cursor.execute(insert_update_sql, values)

        if sync_deletion and existing_records:
            # Delete records not present in SeaTable
            records_to_delete = existing_records - {row[config['source']['relation_field']] for row in seatable_data}
            if records_to_delete:
                # 注意这里使用 tuple(records_to_delete) 来确保传递的是元组格式
                placeholders = ', '.join(['%s' for _ in records_to_delete])  # 为每个要删除的记录生成一个占位符
                delete_sql = f"DELETE FROM {config['destination']['table_name']} WHERE {config['destination']['relation_field']} IN ({placeholders})"
                # 使用 *records_to_delete 来解包集合，确保每个元素都被单独传递
                cursor.execute(delete_sql, tuple(records_to_delete))

        connection.commit()
    except Exception as e:
        print(f"Error syncing data: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

    print("Data sync from SeaTable to MySQL completed.")

if __name__ == '__main__':
    sync_seatable_to_mysql()
