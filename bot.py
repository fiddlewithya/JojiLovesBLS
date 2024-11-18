import os
import telebot
import requests
import json
from datetime import datetime, timedelta

# API and Telegram Bot Tokens
BLS_API_KEY = os.getenv("BLS_API_KEY", "12312321")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "123123123")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# BLS API Endpoint and Series Definitions
BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
BLS_SERIES = {
    "CPI": {"id": "CUSR0000SA0", "name": "Consumer Price Index"},
    "Unemployment Rate": {"id": "LNS14000000", "name": "Civilian Unemployment Rate"},
    "Wages": {"id": "CES0500000003", "name": "Average Hourly Earnings"},
}

# Utility Functions
def fetch_bls_data(series_id, start_year, end_year):
    """
    Fetches data for a specific series ID from the BLS API.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "seriesid": [series_id],
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": BLS_API_KEY,
    }

    response = requests.post(BLS_API_URL, headers=headers, data=json.dumps(payload))
    print(f"Series ID: {series_id} | Response: {response.json()}")  # Debugging output
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"HTTP {response.status_code}: {response.text}"}

def get_latest_data_for_series(series_id, series_name):
    """
    Fetches the most recent data for a given series, even if it's not from the current month.
    """
    current_year = datetime.now().year
    current_month = datetime.now().month
    series_data = fetch_bls_data(series_id, current_year - 1, current_year)
    if "Results" in series_data and "series" in series_data["Results"]:
        data_points = series_data["Results"]["series"][0].get("data", [])
        if data_points:
            for data_point in data_points:
                try:
                    report_date = datetime.strptime(
                        f"{data_point['year']}-{data_point['periodName']}", "%Y-%B"
                    )
                    # If data for the current month exists, prioritize it
                    if report_date.year == current_year and report_date.month == current_month:
                        return {
                            "name": series_name,
                            "value": data_point["value"],
                            "date": report_date,
                            "url": f"https://www.bls.gov/{series_id.lower()}/",
                        }
                    # Fallback: Return the most recent data point
                    latest_data = data_points[0]
                    latest_report_date = datetime.strptime(
                        f"{latest_data['year']}-{latest_data['periodName']}", "%Y-%B"
                    )
                    return {
                        "name": series_name,
                        "value": latest_data["value"],
                        "date": latest_report_date,
                        "url": f"https://www.bls.gov/{series_id.lower()}/",
                    }
                except ValueError:
                    # Handle invalid dates in the API response
                    continue
    return None

def get_past_reports():
    """
    Fetches and displays past reports for the current month or the latest available data.
    """
    current_month = datetime.now().month
    current_year = datetime.now().year
    today = datetime.today()
    past_reports = []

    for report_name, series in BLS_SERIES.items():
        report = get_latest_data_for_series(series["id"], series["name"])
        if report:
            # Check if the report is for the current month
            if report["date"].year == current_year and report["date"].month == current_month:
                past_reports.append(report)

    if not past_reports:
        # Include the latest available data if no reports are found for the current month
        message = (
            "📋 No reports published for this month yet.\n\n"
            "Here are the most recent reports:\n\n"
        )
        for report_name, series in BLS_SERIES.items():
            report = get_latest_data_for_series(series["id"], series["name"])
            if report:
                message += (
                    f"- {report['date'].strftime('%A, %B %d, %Y')}: "
                    f"[*{report['name']}*]({report['url']}) - Value: {report['value']}\n"
                )
        return message

    # Format the past reports
    message = "📋 *Published Reports for This Month*\n\n"
    for report in past_reports:
        message += (
            f"- {report['date'].strftime('%A, %B %d, %Y')}: "
            f"[*{report['name']}*]({report['url']}) - Value: {report['value']}\n"
        )
    return message


def get_upcoming_reports():
    """
    Approximates upcoming reports for the current month based on patterns.
    """
    # Simulated upcoming dates (replace with scraped schedule if available)
    current_month = datetime.now().month
    current_year = datetime.now().year
    today = datetime.today()

    upcoming_schedule = [
        {"date": datetime(current_year, current_month, 22), "name": "Producer Price Index"},
        {"date": datetime(current_year, current_month, 30), "name": "Employment Cost Index"},
    ]

    upcoming = [r for r in upcoming_schedule if r["date"] >= today]

    if not upcoming:
        return "🎉 No upcoming reports for this month."

    # Format the upcoming reports
    message = "📅 *Upcoming Reports for This Month*\n\n"
    for report in upcoming:
        message += f"- {report['date'].strftime('%A, %B %d, %Y')}: *{report['name']}*\n"
    return message

# Bot Commands
@bot.message_handler(commands=["start"])
def welcome_message(message):
    """
    Sends a welcome message and guides the user on available commands.
    """
    bot.send_message(
        message.chat.id,
        "Welcome to JojFinance.\n"
        "/upcoming - Lists all upcoming reports for the month\n"
        "/past - Lists reports already published for the month"
    )

@bot.message_handler(commands=["upcoming"])
def send_upcoming_reports(message):
    """
    Sends a list of upcoming reports for the month.
    """
    upcoming_message = get_upcoming_reports()
    bot.send_message(message.chat.id, upcoming_message, parse_mode="Markdown")

@bot.message_handler(commands=["past"])
def send_past_reports(message):
    """
    Sends a list of reports already published for the month.
    """
    past_message = get_past_reports()
    bot.send_message(message.chat.id, past_message, parse_mode="Markdown")

# Start the bot
bot.polling()