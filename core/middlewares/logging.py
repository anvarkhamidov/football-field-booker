import logging

logger = logging.getLogger("django")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request details
        logger.info(
            f"Request: {request.method} {request.get_full_path()} "
            f"Headers: {request.headers} "
            f"Body: {request.body.decode('utf-8') if request.body else 'No Body'}"
        )

        response = self.get_response(request)

        # Optionally, log the response details
        logger.info(
            f"Response: {response.status_code} for {request.method} {request.get_full_path()}"
        )

        return response
