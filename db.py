import os
import psycopg2
from psycopg2 import sql
import pandas as pd
from typing import Union, List
from dotenv import load_dotenv

#テーブルをdfとして取得する関数
from psycopg2 import sql

def get_table_data(table_name: str) -> Union[pd.DataFrame, None]:
    load_dotenv()
    
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    required_vars = ["DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        schema_name = 'public'  # 必要なら変更
        with conn.cursor() as cur:
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s AND table_schema = %s
                ORDER BY ordinal_position
            """, (table_name, schema_name))
            
            columns = [col[0] for col in cur.fetchall()]
            if not columns:
                raise ValueError(f"Table '{schema_name}.{table_name}' does not exist or has no columns.")
            
            query = sql.SQL("SELECT * FROM {}.{}").format(
                sql.Identifier(schema_name),
                sql.Identifier(table_name)
            )
            df = pd.read_sql_query(query.as_string(conn), conn)
        
        conn.close()
        return df
        
    except psycopg2.Error as e:
        print(f"Database error: {e.pgcode}, {e.pgerror}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise


#テーブル名一覧を取得する関数
def get_table_names(schema: str = "public") -> List[str]:
    # .envファイルを読み込む
    load_dotenv()

    # 環境変数から接続情報を取得
    db_config = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': int(os.getenv('DB_PORT', '5432'))
    }

    try:
        # データベースに接続
        conn = psycopg2.connect(**db_config)
        
        # カーソルを作成
        cur = conn.cursor()
        
        # テーブル一覧を取得するSQLクエリ
        query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """
        
        # クエリを実行
        cur.execute(query, (schema,))
        
        # 結果を取得
        tables = [row[0] for row in cur.fetchall()]
        
        # カーソルとコネクションを閉じる
        cur.close()
        conn.close()
        
        return tables
        
    except psycopg2.Error as e:
        print(f"データベースエラーが発生しました: {e}")
        raise