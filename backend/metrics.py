import time
from collections import deque


class Metrics:

    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.visualization_requests = 0
        self.total_response_time = 0.0
        self.last_queries = deque(maxlen=5)

    def record_request(self, question: str):
        self.total_requests += 1
        self.last_queries.append(question)

    def record_success(self, response_time: float, is_visual: bool):
        self.successful_requests += 1
        self.total_response_time += response_time
        if is_visual:
            self.visualization_requests += 1

    def record_failure(self):
        self.failed_requests += 1

    def get_metrics(self):
        avg_time = (
            self.total_response_time / self.successful_requests
            if self.successful_requests > 0
            else 0
        )

        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "visualization_requests": self.visualization_requests,
            "average_response_time_seconds": round(avg_time, 3),
            "last_5_queries": list(self.last_queries),
        }