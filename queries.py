CREATE_TABLE_CONSTANTS = (
    "CREATE TABLE constants ("
    "    id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "    name TEXT UNIQUE,"
    "    value TEXT"
    ")"
)

CREATE_TABLE_FILE_DATA = (
    "CREATE TABLE file_data ("
    "    id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "    file_name TEXT UNIQUE,"
    "    file_type TEXT"
    ")"
)

CREATE_TABLE_OBJECT_DATA = (
    "CREATE TABLE object_data ("
    "    id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "    file_id INTEGER,"
    "    object_index INTEGER,"
    "    object_name TEXT UNIQUE,"
    "    FOREIGN KEY(file_id) REFERENCES file_data(id)"
    ")"
)

INSERT_INTO_CONSTANTS = "INSERT INTO constants(name, value) VALUES(?, ?)"

GET_TABLES_INFO = "SELECT sql FROM sqlite_master WHERE name = ?"

GET_CONSTANT = "SELECT value FROM constants WHERE name = ?"

GET_ALL_FILE_ENTRIES = "SELECT file_name FROM file_data WHERE file_type = ? ORDER BY id"
