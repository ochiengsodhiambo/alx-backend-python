import asyncio
import aiosqlite

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("[ALL USERS]", rows)
            return rows

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            print("[OLDER USERS > 40]", rows)
            return rows

# Run both queries concurrently
async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

# Entry point
if __name__ == "__main__":
    users, older_users = asyncio.run(fetch_concurrently())
    print("\nFinal Results:")
    print("Users:", users)
    print("Older Users:", older_users)
