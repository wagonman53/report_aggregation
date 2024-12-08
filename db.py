import os
import psycopg2
import pandas as pd
from typing import Union, List
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

#テーブルをdfとして取得する関数
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
    
    # SQLAlchemyエンジンを作成
    engine_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(engine_url)

    schema_name = 'public'  # 必要なら変更

    # インスペクタを使用してカラム情報を取得
    insp = inspect(engine)
    columns = insp.get_columns(table_name, schema=schema_name)
    
    if not columns:
        raise ValueError(f"Table '{schema_name}.{table_name}' does not exist or has no columns.")

    # pandasでテーブル読み込み
    df = pd.read_sql_table(table_name, con=engine, schema=schema_name)
    
    return df


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