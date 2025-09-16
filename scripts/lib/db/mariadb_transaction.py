import logging
import mariadb
import threading

from scripts.lib.utils.configuration import Configuration


_pool: mariadb.ConnectionPool = None
_id: int = 1
_lock: threading.Lock = threading.Lock()


class MariaDBTransaction():
    def __init__(self, logger: logging.Logger | None = None):
        global _id, _lock
        
        with _lock:
            self.id = _id
            _id += 1

        self.logger = logger or logging.getLogger(__name__)
        self.logger.info(f"TRANSACTION {self.id}: Initialized.")

        self._connection = _get_connection()
        self.cursor = self._connection.cursor(dictionary=True) # Sets the results of que queries as dictionaries
    
        try:
            timeout = Configuration.get()['MARIADB']['query_timeout']
            self.cursor.execute(f"SET @@MAX_STATEMENT_TIME={timeout}")
            self.logger.debug(f"TRANSACTION {self.id}: MAX_STATEMENT_TIME set to {timeout}s.")

        except Exception as e:
            self.logger.error(f"TRANSACTION {self.id}: Critical error configuring session: {e}")
            self.close()
            raise
    
    
    def execute_query(self, sql, parameters):
        self.logger.debug(f"Executing Query. MariaDBTransaction [{self.id}]:\n{sql}")
        self.check_connections()
        self.cursor.execute(sql, parameters)

        return self.cursor.fetchall()
    

    def execute_insert(self, sql, parameters):
        self.logger.debug(f"Executing Insert. MariaDBTransaction [{self.id}]:\n{sql}")
        self.check_connections()
        self.cursor.execute(sql, parameters)

        return self.cursor.lastrowid


    def check_connections(self):
        if self._connection is None:
            raise ConnectionError(f"Couldn't connect to MariaDB.")
        if self.cursor is None:
            raise ConnectionError("Couldn't execute the statement.")


    def close(self):
        self.cursor.close()
        if self._connection:
            self._connection.close()
            self.logger.info(f"TRANSACTION {self.id}: Connection returned to pool.")


    def commit(self):
        self.logger.info(f"TRANSACTION {self.id}: Succeeded. Executing Commit.")
        if self._connection:
            self._connection.commit()


    def rollback(self):
        self.logger(f"TRANSACTION {self.id}: An exception occurred. Executing Rollback.")
        if self._connection:
            self._connection.rollback()

    
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
