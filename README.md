# Michael Business Analyst Modular

## Overview

Michael Business Analyst Modular is an AI-powered analytics platform designed to provide actionable business insights from your sales and customer data. The system is built with a modular Python backend, integrated database, and a flexible architecture for easy extension.

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for dependency management

### Installation & Setup

1. Install dependencies:

```bash
uv sync
```

2. Initialize the database:

```bash
uv run -m michael.db_init
```

3. Launch the application:

```bash
uv run -m michael.app
```

4. Create a `.env` file in the project root to store environment variables (such as secret keys, database URLs, etc.). Example:

```env
DEBUG=True
GROQ_API_KEY=your_groq_key_here
DATABASE_URL=sqlite:///michael.db
```

**Note**: For production deployments, set DEBUG=False in your .env file to disable debug mode and enhance security.

The API will be available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Architecture

The project follows a modular structure:

- **Backend**: Built with Flask, organized in the `michael/` package.
- **Database**: SQLite, initialized and managed via `db_init.py` and `db.py`.
- **Models**: Defined in `models.py` for products, customers, sales, etc.
- **Routes**: API endpoints in `routes/api.py` and `routes/views.py`.
- **NLP Parser**: Handles natural language queries in `nlp_parser.py`.

## Workflow

1. User submits a query (e.g., "Top 5 products sold last month").
2. The NLP parser interprets the query and determines the required data.
3. The backend retrieves and processes data from the database.
4. Results are returned via the API for visualization or further analysis.

## Features

- Product sales and revenue analysis
- Customer activity tracking
- Business trend insights

## Extending the System

- Add new models to `models.py` for additional data types.
- Create new API endpoints in `routes/` for custom analytics.
- Enhance the NLP logic in `nlp_parser.py` for broader query support.

## Support & Contribution

For questions, feature requests, or contributions, please open an issue or submit a pull request.
