import re
from dataclasses import dataclass
from typing import Dict
from typing import Iterable
from typing import Optional

# Borrowed from mysql-connector-python
REGEX_PARAM = re.compile(r"""\?(?=(?:[^"'`]*["'`][^"'`]*["'`])*[^"'`]*$)""")


@dataclass
class PreparedStatement:
    stmt_id: int
    sql: str
    num_params: int
    param_buffers: Optional[Dict[int, bytearray]] = None
    cursor: Optional[Iterable] = None
