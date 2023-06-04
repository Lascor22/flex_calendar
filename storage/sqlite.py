import sqlite3

from storage.storage import BaseStorage

database_version = 1

configure_db_sql = """
pragma encoding = 'UTF-8';
pragma locking_mode = EXCLUSIVE;
pragma synchronous = OFF;
pragma temp_store = MEMORY;
pragma journal_mode = WAL;
pragma page_size = 4096;
pragma cache_size = 40000;
"""

create_db_sql = f"""
begin;
create table if not exists events(
    id integer primary key,
    user_id integer not null,
    name text not null,
    date text not null
);
create index if not exists event_user_data on events(user_id, name, date);

pragma user_version = {database_version};
commit;
"""

remove_db_sql = """
begin;
drop table if exists events;
commit;
"""

check_empty_sql = 'select * from sqlite_master'
get_db_version = 'pragma user_version'

select_user_event_count_sql = 'select count(id) as event_count from events where user_id = :user_id'

insert_event_sql = 'insert into events(user_id, name, date) values(:user_id, :name, :date)'

select_user_events_sql = 'select id, name, date from events where user_id = :user_id'

delete_user_event_sql = 'delete from events where user_id = :user_id and id = :event_id'


class SQLiteStorage(BaseStorage):

    def __init__(self, storage_file):
        self.connection = sqlite3.connect(storage_file, timeout=5.0, detect_types=0, isolation_level='EXCLUSIVE',
                                          check_same_thread=False, factory=sqlite3.Connection, cached_statements=128,
                                          uri=False)
        self.cursor = self.connection.cursor()
        tables = self.cursor.execute(check_empty_sql).fetchall()
        # database update scenario logic
        if len(tables) > 0:
            version = self.cursor.execute(get_db_version).fetchone()[0]
            if database_version < version:
                raise Exception(
                    f'Database error: database version {version} greater than expected {database_version}')
            elif database_version > version:
                self.cursor.executescript(remove_db_sql)
            else:
                return
        else:
            self.cursor.executescript(create_db_sql)

    def is_known_user(self, user_id):
        events_count = self.cursor.execute(select_user_event_count_sql,  {
                                           'user_id': user_id}).fetchone()[0]
        return events_count > 0

    def save_event(self, user_id, event):
        with self.connection:
            event['user_id'] = user_id
            self.cursor.execute(insert_event_sql, event)

    def get_user_events(self, user_id):
        return self.cursor.execute(select_user_events_sql, {'user_id': user_id}).fetchall()

    def delete_event(self, user_id, event_id):
        return self.cursor.execute(delete_user_event_sql, {'user_id': user_id, 'event_id': event_id})

    def close(self):
        self.cursor.close()
        self.connection.close()
