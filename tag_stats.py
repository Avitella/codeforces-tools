#!/usr/bin/env python3

import argparse
import functools
import json
import logging
import requests
import time
import collections

def get_logger():
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)-15s %(levelname)-6s %(message)s"))

    log = logging.getLogger(__name__)
    log.addHandler(ch)
    log.setLevel(logging.DEBUG)

    return log

log = get_logger()
log.debug("Start")

def send_request(query):
    while True:
        request = None

        try:
            request = requests.get(query, timeout=5.0)
        except requests.exceptions.Timeout:
            log.warning("Timed out, retry...")
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


def get_args():
    parser = argparse.ArgumentParser(description="Compute some codeforces statistics")
    parser.add_argument("--handler", type=str, help="codeforces handler", required=True)
    return parser.parse_args()


def get_contests():
    return send_request("http://codeforces.com/api/contest.list")["result"]


def get_standings(handler, contest_id):
    query = "http://codeforces.com/api/contest.standings?contestId={}&showUnofficial=true&handles={}".format(contest_id, handler)
    return send_request(query)["result"]


def is_valid_contest(contest):
    if contest["phase"] != "FINISHED":
        return False

    if "trial contest" in contest["name"]:
        return False

    return True


def is_valid_party(party):
    return party["participantType"] == "VIRTUAL" or party["participantType"] == "CONTESTANT"


args = get_args()
contests = get_contests()

unsolved_tags = collections.defaultdict(int)
all_tags = collections.defaultdict(int)

for contest in contests:
    if not is_valid_contest(contest):
        continue

    standings = get_standings(args.handler, contest["id"])

    solved = []
    for row in standings["rows"]:
        if not is_valid_party(row["party"]):
            continue

        results = row["problemResults"]
        for i in range(len(results)):
            if results[i]["points"] > 0.0:
                solved.append(i)
        break

    for problem in standings["problems"]:
        for tag in problem["tags"]:
            all_tags[tag] += 1

    if not solved:
        continue

    log.info("Prepare contest: {}, solved: {}, all: {}".format(contest["id"], len(solved), len(standings["problems"])))

    barriers = set()
    for i in range(solved[-1]):
        if i not in solved:
            barriers.add(i)
    barriers.add(solved[-1] + 1)

    problems = standings["problems"]
    for i in range(len(problems)):
        t = problems[i]["tags"]
        for tag in t:
            if i in barriers:
                unsolved_tags[tag] += 1

tag_ratio = {}
for tag in unsolved_tags:
    tag_ratio[tag] = unsolved_tags[tag] * 1.0 / all_tags[tag]

sorted_tags = []
for k in unsolved_tags:
    sorted_tags.append(k)

sorted_tags.sort(key=lambda x: tag_ratio[x])
sorted_tags.reverse()

print("# Unsolved statistics:")
for tag in sorted_tags:
    print('"{}" -- ratio: {}, unsolved_count: {}, total_count: {}'.format(tag, tag_ratio[tag], unsolved_tags[tag], all_tags[tag]))

print("# Tags statistics:")
for tag in all_tags:
    print("{} -- count: {}".format(tag, all_tags[tag]))
