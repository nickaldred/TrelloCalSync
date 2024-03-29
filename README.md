# Calendar Sync Service

This project is a calendar synchronization service that synchronizes events between a board (like Trello) and a calendar (like Google Calendar).

## Project Structure

### Key Components

- `cal_sync_api.py`: Sets up the API for the calendar sync service.
- `sync_processor.py`: Syncs the board and calendar.
- `google_calendar_handler.py`: Handles requests to the Google Calendar API.
- `calendar_handler.py`: Interface for calendar handlers.
- `mongodb_handler.py`: Handles requests to the MongoDB database.
- `trello_handler.py`: Handles requests to the Trello API.
- `factorys.py`: Contains factory functions for creating calendar and database handlers.
- `config.py`: Handles configuration settings for the application.
- `data_models.py`: Contains data models for the application.
- `exceptions.py`: Contains custom exceptions for the application.
- `logging_funcs.py`: Contains logging functions for the application.

## Setup

1. Clone the repository.
2. Install the requirements using pip: `pip install -r requirements.txt`.
3. Copy `.env.template` to `.env` and fill in your environment variables.
4. Run the application: `python src/cal_sync_api.py`.

## Usage

The API has the following endpoints:

- `POST /add_event`: Add an event to the calendar and database.
- `GET /get_event/{event_id}`: Get an event from the database.
- `DELETE /delete_event/{event_id}`: Delete an event from the calendar and database.
- `PUT /update_event/{event_id}`: Update an event in the calendar and database.

## Testing

Tests are located in the `tests/` directory. Run them using your preferred test runner.

## Docker

A Dockerfile and a docker-compose.yml file are included for running the application in a Docker container. Build the Docker image and start the container with `docker-compose up`.

## Designs

Design documents are located in the `designs/` directory. They include a draw.io diagram and a markdown file.

## Logging

Logs are written to the `logs/` directory. The logging configuration is located in `config/logging.conf`.

## Contributing

Contributions are welcome. Please open a pull request with your changes.

## License

This project is licensed under the terms of the MIT license.
