import requests
import time

import libs.logging


log = libs.logging.logger("api")


def get(raw_query, retry_count = 4):
    query = "http://codeforces.com/api/" + raw_query
    remaining_attempts_number = retry_count

    while True:
        request = None

        try:
            request = requests.get(query, timeout=5.0)
        except requests.exceptions.Timeout:
            log.warning("Connection timeout, retry...")
            continue
        except requests.RequestException as e:
            log.error("Unexpected error: {}".format(e))
            if remaining_attempts_number <= 0:
                raise
            to_sleep = 1.0
            log.warning("Remaining attempts number: {}, sleep({}) and retry...".format(remaining_attempts_number, to_sleep))
            remaining_attempts_number -= 1
            time.sleep(to_sleep)
            continue

        json = request.json()

        if request.status_code == 429:
            to_sleep = 0.5
            log.debug("Call limit exceeded, sleep({})".format(to_sleep))
            time.sleep(to_sleep)
            continue

        if request.status_code != 200 or json["status"] != "OK":
            reason = "unknown"
            if "comment" in json:
                reason = json["comment"]

            raise RuntimeError("Can't send request: {}, reason: {}, code: {}".format(query, reason, request.status_code))

        return json
