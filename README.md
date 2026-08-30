# STOCKLAB

STOCKLAB is a Python ETL project that downloads Vietnamese market price data
with `vnstock`, transforms it with pandas, and stores it in PostgreSQL. It also
contains basic return and correlation calculations.

## What the project does

1. Reads the symbols and extraction settings from `stock_config.py`.
2. Downloads OHLCV price data through `vnstock`.
3. Cleans and sorts the returned data.
4. Stores symbols in the `stocks` table.
5. Stores daily candles in the `daily_prices` table.

The inserts use PostgreSQL conflict handling, so an existing symbol or an
existing `(stock_id, trading_date)` pair is not inserted twice.

## Requirements

- Python 3.12
- PostgreSQL
- Internet access for `vnstock`
- Git

Docker is optional. The included `docker-compose.yml` can run PostgreSQL
locally, while a hosted PostgreSQL service such as Neon can be used instead.

## Project structure

```text
STOCKLAB/
├── ETL/                    # Download and transform market data
├── analytics/              # Return and correlation calculations
├── database/
│   ├── connection.py       # PostgreSQL connection configuration
│   ├── migrate.py          # Applies database/schema.sql
│   ├── repository_price.py
│   ├── repository_stock.py
│   └── schema.sql
├── .env.example            # Safe configuration template
├── docker-compose.yml      # Optional local PostgreSQL
├── main.py                 # ETL entry point
├── requirements.txt
└── stock_config.py         # Symbols and extraction settings
```

## First-time setup

### 1. Clone the repository

```bash
git clone https://github.com/huhoccodebui33/STOCKLAB.git
cd STOCKLAB
```

### 2. Create a virtual environment

Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create your private environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Open `.env` and enter your own PostgreSQL details:

```dotenv
DB_HOST=your-postgresql-host
DB_PORT=5432
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
PGSSLMODE=require
PGCHANNELBINDING=require
PGCONNECT_TIMEOUT=10
```

For Neon, copy the host, database, role, and password from the Neon connection
details. Do not place a complete connection URL in source code. Do not commit
`.env`.

Each contributor should use their own database credential. Do not share a
database owner password through GitHub, chat, screenshots, or documentation.

### 5. Test the connection without changing data

```bash
python -c 'from database.connection import getConnection; c=getConnection(); x=c.cursor(); x.execute("SELECT current_database(), current_user"); print(x.fetchone()); c.rollback(); x.close(); c.close()'
```

Expected output contains the configured database and user:

```text
('your-database-name', 'your-database-user')
```

### 6. Create the tables

Run this only for a new database, or when the project owner tells you to apply
the current schema:

```bash
python -m database.migrate
```

This creates:

- `stocks`
- `daily_prices`

The migration changes the configured database. Confirm that `.env` points to
the intended database before running it.

### 7. Run the ETL pipeline

Review `STOCKS` and `CONFIG` in `stock_config.py`, then run:

```bash
python main.py
```

The default configuration requests many symbols and waits between requests to
reduce API rate-limit errors. For a first test, temporarily use only one symbol
and a smaller limit in your own branch.

## Using local PostgreSQL with Docker

The existing Compose configuration exposes PostgreSQL on local port `5433`.
Start it with:

```bash
docker compose up -d postgres
docker compose ps
```

Configure `.env` with the same username, password, and database shown in
`docker-compose.yml`:

```dotenv
DB_HOST=127.0.0.1
DB_PORT=5433
DB_NAME=vnstock
DB_USER=postgres
DB_PASSWORD=the-password-from-docker-compose
PGSSLMODE=disable
PGCHANNELBINDING=disable
PGCONNECT_TIMEOUT=10
```

Then initialize and run the project:

```bash
python -m database.migrate
python main.py
```

To stop PostgreSQL while keeping its data:

```bash
docker compose stop
```

Do not run `docker compose down -v` unless you intentionally want to delete the
local database volume and all of its data.

## Configuration

`stock_config.py` supports two extraction modes.

Limit mode:

```python
CONFIG = {
    "mode": "limit",
    "interval": "1D",
    "limit": 1250,
}
```

Date mode:

```python
CONFIG = {
    "mode": "date",
    "interval": "1D",
    "start_date": "2021-07-26",
    "end_date": "2026-07-26",
}
```

## Common problems

### `relation "stocks" does not exist`

The connection works, but the schema has not been applied:

```bash
python -m database.migrate
```

### Connection timeout or hostname error

Check `DB_HOST`, internet access, and `PGCONNECT_TIMEOUT`. For hosted
PostgreSQL, make sure TLS settings match the provider.

### Authentication failed

Check `DB_USER` and `DB_PASSWORD`. Ask the database owner for a new restricted
credential rather than using another person's owner account.

### No module named `psycopg2`, `pandas`, or `vnstock`

Activate the virtual environment and reinstall dependencies:

```bash
python -m pip install -r requirements.txt
```

## Collaboration workflow

Before starting work:

```bash
git switch main
git pull --ff-only
git switch -c feature/short-description
```

After making and testing changes:

```bash
git status
git diff
git add path/to/changed-file
git commit -m "Describe the change"
git push -u origin feature/short-description
```

Open a pull request on GitHub instead of pushing experimental work directly to
`main`.

Never commit:

- `.env` or database connection URLs
- passwords, API keys, or tokens
- `.venv/`
- generated Python cache files
- exported database dumps containing private data

## Database safety

- Use separate credentials for separate contributors.
- Give application users only the permissions they need.
- Keep owner credentials for administration and migrations.
- Confirm the target database before running migrations.
- Back up important data before changing the schema.
- Rotate a credential immediately if it appears in Git, chat, or a screenshot.
