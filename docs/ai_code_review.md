# AI Code Review

The ingestion pipeline was reviewed using an AI assistant to check if the code could be improved.

## Suggestions from AI

The AI assistant suggested a few improvements:

1. Add validation checks for latitude and longitude values.
2. Avoid using hardcoded file paths in the script.
3. Add logging to track ingestion runs.
4. Use a configuration file to manage dataset paths.

## Improvements Implemented

After reviewing the suggestions, the following changes were made:

* Validation was added to ensure latitude values are between **-90 and 90** and longitude values are between **-180 and 180**.
* Hardcoded file paths were removed from the code.
* Dataset paths were moved to a **configuration file (`config.yaml`)**.
* Logging was added to record ingestion runs and track the number of processed records.

These changes make the ingestion pipeline easier to maintain and more reliable.
