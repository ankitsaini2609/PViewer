import pytest
import json
from pviewer.__main__ import conflicting_policy


def isConflicting(conflict_tracker):
    for policy in conflict_tracker.keys():
        if len(conflict_tracker[policy]) != 0:
            return True
    return False


def test_policy():
    with open("policies/IAMFullAccess", "r") as f:
        IAM_policy = json.load(f)

    with open("policies/EC2ReadOnlyAccess", "r") as f:
        EC2_policy = json.load(f)

    with open("policies/RDSReadOnlyAccess", "r") as f:
        RDS_policy = json.load(f)

    first_test_case = list()
    first_test_case.append({"policyname": "RDSReadOnlyAccess", "statement": RDS_policy["Statement"]})
    first_test_case.append({"policyname": "EC2ReadOnlyAccess", "statement": EC2_policy["Statement"]})

    second_test_case = list()
    second_test_case.append({"policyname": "IAMFullAccess", "statement": IAM_policy["Statement"]})
    second_test_case.append({"policyname": "RDSReadOnlyAccess", "statement": RDS_policy["Statement"]})

    assert isConflicting(conflicting_policy(first_test_case)) == True
    assert isConflicting(conflicting_policy(second_test_case)) == False