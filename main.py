from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from exceptions.schedule_exceptions import ScheduleNotFoundError, InvalidDayNameError, FirestoreConnectionError, \
    ActivityParsingError
from routes.schedule_route import router

app: FastAPI = FastAPI(title="WAT Schedule API")
app.include_router(router)

@app.exception_handler(FirestoreConnectionError)
async def firestore_error_handler(_request: Request, _exc: FirestoreConnectionError):
    """
    Handles Firestore connection errors.

    Returns:
        JSONResponse: 503 Service Unavailable with an appropriate error message.
    """
    return JSONResponse(
        status_code=503,
        content={"error": "Failed to connect to Firestore. Please try again later."}
    )


@app.exception_handler(ScheduleNotFoundError)
async def not_found_handler(_request: Request, _exc: ScheduleNotFoundError):
    """
    Handles cases where the requested schedule is not found.

    Returns:
        JSONResponse: 404 Not Found with an appropriate error message.
    """
    return JSONResponse(
        status_code=404,
        content={"error": "Schedule not found for the given week."}
    )


@app.exception_handler(InvalidDayNameError)
async def invalid_day_handler(_request: Request, _exc: InvalidDayNameError):
    """
    Handles unsupported day names in Firestore documents.

    Returns:
        JSONResponse: 422 Unprocessable Entity with an appropriate error message.
    """
    return JSONResponse(
        status_code=422,
        content={"error": "Unsupported day name found in schedule data."}
    )


@app.exception_handler(ActivityParsingError)
async def parsing_error_handler(_request: Request, _exc: ActivityParsingError):
    """
    Handles errors during parsing of activity strings.

    Returns:
        JSONResponse: 400 Bad Request with an appropriate error message.
    """
    return JSONResponse(
        status_code=400,
        content={"error": "Failed to parse an activity entry."}
    )


@app.exception_handler(Exception)
async def generic_error_handler(_request: Request, _exc: Exception):
    """
    Handles all unexpected internal server errors.

    Returns:
        JSONResponse: 500 Internal Server Error with a generic message.
    """
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected server error occurred."}
    )

