import re


class OperationsModel:
    """opertions model"""

    def __init__(self):
        self.history_page_cursor1 = 0
        # self.history_page_cursor2 = 10

    def create_table(self, db):
        return db.execute(
            """
            CREATE TABLE IF NOT EXISTS operations 
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER NOT NULL, 
                symbol TEXT NOT NULL, 
                price NUMERIC NOT NULL,
                change NUMERIC NOT NULL,
                number_of_shares INTEGER NOT NULL DEFAULT 0, 
                owned_shares INTEGER NOT NULL DEFAULT 0,
                operation TEXT NOT NULL,
                timestamp DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )

    def get_user_ownedshares(self, db, userId):
        return db.execute(
            """
            SELECT symbol, owned_shares, MAX(timestamp) as ts, cash
            FROM operations, users
            WHERE user_id = ?
            AND operations.user_id = users.id
            GROUP BY symbol
            HAVING owned_shares > 0
            ORDER BY timestamp
            """,
            userId,
        )

    def get_user_custom_ownedshares(self, db, user_id):
        return db.execute(
            """
                SELECT symbol, owned_shares as shares, cash
                FROM operations, users
                WHERE user_id = ?
                AND operations.user_id = users.id
                GROUP BY symbol
                HAVING owned_shares > 0
                ORDER BY MAX(timestamp) DESC
            """,
            user_id,
        )

    def calc_user_ownedshares(self, db, user_id, symbol, operation1, operation2):
        return db.execute(
            """
                SELECT SUM(number_of_shares) AS bought_sum, (
                    SELECT SUM(number_of_shares) 
                    FROM operations 
                    WHERE user_id = ? 
                    AND symbol LIKE ? 
                    AND operation = ? 
                ) AS sold_sum
                FROM operations 
                WHERE user_id = ? 
                AND symbol LIKE ? 
                AND operation = ? 
                """,
            user_id,
            symbol,
            operation1,
            user_id,
            symbol,
            operation2,
        )

    def create_operation(self, db, **kwargs):
        return db.execute(
            """
            INSERT INTO operations (user_id, symbol, price, change, number_of_shares, owned_shares, operation) 
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            kwargs["user_id"],
            kwargs["symbol"],
            kwargs["price"],
            kwargs["change"],
            kwargs["number_of_shares"],
            kwargs["owned_shares"],
            kwargs["operation"],
        )

    def get_user_history(self, db, user_id):
        return db.execute(
            """
                SELECT symbol, price, change, number_of_shares as shares, operation, timestamp as date
                FROM operations
                WHERE user_id = ?
                ORDER BY timestamp DESC
            """,
            user_id,
        )

    def get_history_total_by_user(self, db, user_id):
        return db.execute(
            """
                SELECT COUNT(*) as count
                FROM operations
                WHERE user_id = ?
            """,
            user_id,
        )

    def get_paginated_user_history(
        self, db, user_id, page=1, pageSize=10, orderBy='timestamp', start=0, end=0
    ):
        # rows = db.execute(
        #     f"""
        #         SELECT id, symbol, price, change, number_of_shares as shares, operation, timestamp as date
        #         FROM operations
        #         WHERE user_id = ?
        #         AND (id > {end} OR id < {start})
        #         ORDER BY date
        #         LIMIT ?
        #     """,
        #     user_id,
        #     pageSize
        # )
        orderby = re.sub(r"[0-9]|\W|_", '', orderBy)
        rows = db.execute(
            f"""
                SELECT id, symbol, price, change, number_of_shares as shares, operation, timestamp as date
                FROM operations
                WHERE user_id = ?
                ORDER BY {orderby} DESC
                LIMIT ?
                OFFSET (
                    CASE 
                        WHEN (SELECT COUNT(*) AS ttl FROM operations WHERE user_id = ?) <= ? 
                        THEN 0
                    ELSE ?
                    END
                )
            """,
            user_id,
            pageSize,
            user_id,
            (page-1) * pageSize,
            (page-1) * pageSize
        )
        # print("rows: ", rows)
        # self.history_page_cursor1 = (
        #     rows[-1]["id"] if rows else self.history_page_cursor1
        # )

        # self.history_page_cursor2 = (int(page)+1)*pageSize
        # self.history_page_cursor2 = rows[(page*pageSize)-1]["id"] if rows and rows[(page*pageSize)-1] else self.history_page_cursor2
        # print("rows[?]['id']: ", rows, self.history_page_cursor1)
        return rows
