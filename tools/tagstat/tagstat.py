#!/usr/bin/env python3

import argparse
import functools
import json
import logging
import requests
import time
import collections
import coloredlogs

def setup_logger():
    logging.getLogger("requests").setLevel(logging.ERROR)
    coloredlogs.install(level="DEBUG")
    log = logging.getLogger("tagstat")
    return log

log = setup_logger()
log.debug("Start")

def send_request(raw_query):
    query = "http://codeforces.com/api/" + raw_query

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
    return send_request("contest.list")["result"]


def get_standings(handler, contest_id):
    query = "contest.standings?contestId={}&showUnofficial=true&handles={}".format(contest_id, handler)
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

participated_unsolved_tags = collections.Counter()
participated_tags = collections.Counter()
all_tags = collections.Counter()

for contest in contests:
    if not is_valid_contest(contest):
        continue

    contest_id = contest["id"]

    standings = get_standings(args.handler, contest_id)

    solved = set()
    participated = False
    for row in standings["rows"]:
        if not is_valid_party(row["party"]):
            continue

        results = row["problemResults"]
        for i in range(len(results)):
            if results[i]["points"] > 0.0:
                solved.add(i)

        if participated:
            log.warning("Participating several times in contest with id = {}".format(contest_id))

        participated = True

    for problem in standings["problems"]:
        for tag in problem["tags"]:
            all_tags[tag] += 1

    if not participated:
        continue

    log.info("Prepare contest: {}, solved: {}, all: {}".format(contest_id, len(solved), len(standings["problems"])))

    barriers = set()
    if not solved:
        barriers.add(0)
    else:
        last_solved_problem_id = max(solved)
        for i in range(last_solved_problem_id):
            if i not in solved:
                barriers.add(i)
        barriers.add(last_solved_problem_id + 1)

    problems = standings["problems"]
    for i in range(len(problems)):
        t = problems[i]["tags"]
        for tag in t:
            if i in barriers:
                participated_unsolved_tags[tag] += 1
            if (i in barriers) or (i in solved):
                participated_tags[tag] += 1

print()

print("# Unsolved statistics:")
if not participated_tags:
    print("    You must participate in at least one contest to see unsolved statistics")
else:
    tag_ratio = {}
    for tag in participated_unsolved_tags:
        tag_ratio[tag] = participated_unsolved_tags[tag] / participated_tags[tag]

    for tag in sorted(tag_ratio, key=lambda x: tag_ratio[x]):
        print('    %-30s ratio = %-6.3f participated_unsolved_count = %-6d participated_total_count = %d' %\
            (tag, tag_ratio[tag], participated_unsolved_tags[tag], participated_tags[tag]))

print()

print("# Tags statistics:")
for tag in sorted(all_tags, key=lambda x: all_tags[x]):
    print("    %-30s count = %d" % (tag, all_tags[tag]))