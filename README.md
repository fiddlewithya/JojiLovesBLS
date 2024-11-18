# JojiLovesBLS

JojiLovesBLS is a Telegram bot that dynamically fetches data from the Bureau of Labor Statistics (BLS) and presents it in an easy-to-read format. While the bot is functional, it is still a **work in progress**, and there are known issues that need to be resolved.

---

## Features

1. **Dynamic Data**:
   - Uses the BLS Public Data API to fetch live data.
   - Displays published reports for the current month (`/past`).
   - Lists upcoming reports for the remainder of the month (`/upcoming`).

2. **User-Friendly Commands**:
   - `/start`: Provides a welcome message and instructions.
   - `/past`: Lists reports published for the current month or the most recent available data.
   - `/upcoming`: Shows upcoming reports based on predefined schedules.

3. **Detailed Reports**:
   - Provides report names, release dates, values, and links to official BLS pages.

---

## Known Issues

1. **Incorrect Date or Report Name in `/upcoming`**:
   - The predefined schedule for upcoming reports may not align with actual BLS schedules.
   - Integration with live scraping or an official schedule API is needed to address this.

2. **`/past` Not Working as Intended**:
   - The bot does not properly filter reports for the current month.
   - Debugging is required to ensure the bot handles BLS API responses correctly.

---

## Prerequisites

To run this project, you need the following:
- **Python 3.8 or higher** installed.
- A Telegram bot token. Create one via [BotFather](https://core.telegram.org/bots#botfather).
- A valid BLS API key. Register for free at the [BLS Developer Portal](https://www.bls.gov/developers/).

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/JojiLovesBLS.git
   cd JojiLovesBLS

2. Install dependencies:
    pip install -r requirements.txt

3. Create a .env file in the root directory to store your API keys:
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    BLS_API_KEY=your_bls_api_key

4. Run the bot:
    python bot_script.py

---

## Commands
- /start: Provides a welcome message and guides users on available commands.
- /upcoming: Lists all upcoming reports for the current month.
- /past: Lists all reports already published for the current month. If no reports have been published yet, it provides the latest available data.

---

## How It Works
1. API Integration:
Fetches live data from the BLS Public Data API using series IDs like CPI, Unemployment Rate, and Wages.

2. Dynamic Data Display:
Displays report names, release dates, values, and links to their respective BLS pages.

3. Simulated Schedule:
Uses predefined schedules for upcoming reports, which can be improved with dynamic scraping.

---

# #Contributing
This bot is not yet complete, and contributions are welcome. Areas needing improvement:

- Correct integration of /past logic to handle API data accurately.
- Integration of dynamic scraping for /upcoming to ensure real-time accuracy.

Feel free to fork this repository, make improvements, and open a pull request.