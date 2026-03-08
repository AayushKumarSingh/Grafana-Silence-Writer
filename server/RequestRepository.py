from models import db, RequestLogs


class RequestRepository:

    @staticmethod
    def create_request(timestamp: str, username: str, matchers: str, start: str, end: str, comment: str) -> int:
        req = RequestLogs(
            timestamp=timestamp,
            username=username,
            matchers=matchers,
            start=start,
            end=end,
            comment=comment
        )

        db.session.add(req)
        db.session.commit()

        return req.id

    @staticmethod
    def update_status(request_id: int, status: str, silenceID: str = "", failReason: str = "") -> RequestLogs:
        req = RequestLogs.query.get(request_id)

        if req:
            req.status = status
            req.silenceID = silenceID
            req.failReason = failReason
            db.session.commit()

        return req

    @staticmethod
    def get_all_requests_by_username(username) -> tuple[RequestLogs]:
        return (
            RequestLogs.query.filter_by(username=username)
            .order_by(RequestLogs.timestamp.desc())
            .limit(100)
        )
