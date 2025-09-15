import logging
import mariadb
import threading

from scripts.lib.utils.configuration import Configuration


_pool: mariadb.ConnectionPool = None
_id: int = 0
_lock: threading.Lock = threading.Lock()


class MariaDBTransaction():
    def __init__(self, logger: logging.Logger | None = None):
        global _id
        global _lock
        
        with _lock:
            self.id = _id + 1
            _id += 1
        self._connection = _get_connection()
        self.cursor = self._connection.cursor(dictionary=True) # Sets the results of que queries as dictionaries
        self.logger = logger or logging.getLogger(__name__)
    

    def __enter__(self):
        self.logger.info(f"TRANSACTION {self.id}: Initialized.")
        self.cursor.execute(f"SET @@MAX_STATEMENT_TIME={Configuration.get()['MARIADB']['query_timeout']}", [])
        return self
    

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        if self._connection:
            self._connection.close()
        self.logger.info(f"TRANSACTION {self.id}: Closed.")

    
    def execute_query(self, sql, parameters):
        self.logger.debug(f"Executing MariaDBTransaction [{self.id}]: {sql}")
        if self._connection is None:
            raise ConnectionError(f"Couldn't connect to MariaDB.")
        if self.cursor is None:
            raise ConnectionError("Couldn't execute the statement.")

        self.cursor.execute(sql, parameters)

        return self.cursor.fetchall()


    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    
def _get_connection():
    global _pool
    global _lock
    with _lock:
        config = Configuration.get()
        if _pool is None:
            _pool = mariadb.ConnectionPool(
                database = config['MARIADB']['database'],
                host = config['MARIADB']['host'],
                port = int(config['MARIADB']['port']),
                user = config['MARIADB']['user'],
                password = config['MARIADB']['password'],
                pool_name = config['MARIADB']['pool_name'],
                pool_size = config['MARIADB']['pool_size'],
                pool_validation_interval = config['MARIADB']['pool_validation_interval'])
            
    return _pool.get_connection()
