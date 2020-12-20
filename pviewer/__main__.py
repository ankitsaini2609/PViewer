import argparse
import boto3, boto3.session
from collections import defaultdict
from graphviz import Graph
import os
import sys

AWS_PROFILE = os.getenv("AWS_PROFILE")
session = boto3.session.Session(profile_name=AWS_PROFILE)
iam_client = session.client("iam")
iam_resource = session.resource("iam")


def check(conflict_tracker, primary_policy, secondary_policy):
    """
        It will check if secondary policy is already in the list of primary policy.
    """
    for policy in conflict_tracker[primary_policy["policyname"]]:
        if policy == secondary_policy["policyname"]:
            return False
    return True


def compare(primary_service, secondary_service, primary_permission, secondary_permission, primary_resource, secondary_resource):
    """
        It will compare two services, permissions and resources. 
    """
    if (
        (primary_service == secondary_service)
        and (
            primary_permission == secondary_permission
            or secondary_permission == "*"
            or primary_permission == "*"
        )
        and (
            primary_resource == "*"
            or secondary_resource == "*"
            or primary_resource == secondary_resource
        )
    ):
        return True
    return False


def overlapping_action(policy_statements, conflict_tracker, primary_policy, primary_service, primary_permission, primary_resource):
    """
        It will check for overlapping actions in aws policies.
    """
    for secondary_policy in policy_statements:
        flag = False
        if primary_policy != secondary_policy and check(
            conflict_tracker, primary_policy, secondary_policy
        ):
            for secondary_statement in secondary_policy["statement"]:
                if secondary_statement["Effect"] == "Allow":
                    if type(secondary_statement["Action"]) == str:
                        actions = [action for action in secondary_statement["Action"].split()]
                    else:
                        actions = secondary_statement["Action"]
                    for action in actions:
                        secondary_service, secondary_permission = action.split(":", 1)
                        if compare(primary_service, secondary_service, primary_permission, secondary_permission, primary_resource, secondary_statement["Resource"]):
                            conflict_tracker[primary_policy["policyname"]].append(
                                secondary_policy["policyname"]
                            )
                            conflict_tracker[secondary_policy["policyname"]].append(
                                primary_policy["policyname"]
                            )
                            flag = True
                            break
                    if flag:
                        break


def conflicting_policy(policy_statements):
    '''
        Checks for conflicting policy
    '''
    conflict_tracker = defaultdict(list)
    for policy in policy_statements:
        for statement in policy["statement"]:
            if statement["Effect"] == "Allow":
                if type(statement["Action"]) == str:
                    actions = [action for action in statement["Action"].split()]
                else:
                    actions = statement["Action"]
                for action in actions:
                    service, permission = action.split(":", 1)
                    overlapping_action(policy_statements, conflict_tracker, policy, service, permission, statement["Resource"])
    return conflict_tracker


def plot(overlapping_policies):
    g = Graph("G", filename="Overlapping_policies", engine="sfdp")
    for key in overlapping_policies.keys():
        for value in overlapping_policies[key]:
            g.edge(key, value)
            overlapping_policies[value].remove(key)
    g.view()


def main():
    """
    pass username of your aws account using -u parameter
    """
    # Argument Parsing
    parser = argparse.ArgumentParser(usage="%(prog)s -u username")
    parser.add_argument("-u", "--username", help="User Name")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(parser.parse_args(['-h']))
        sys.exit(0)
    username = args.username
    policy_statements = list()
    # fetching managed policies
    try:
        user = iam_resource.User(username)
        policies = user.attached_policies.all()
        for policy in policies:
            policyname = policy.arn.split("/")[-1]
            policy_statements.append(
                {
                    "policyname": policyname,
                    "statement": policy.default_version.document["Statement"],
                }
            )
    except Exception as e:
        print(e)
    # fetching inline policies
    try:
        response = iam_client.list_user_policies(UserName=username)
        list_of_policies = response["PolicyNames"]
        for policy in list_of_policies:
            response = iam_client.get_user_policy(UserName=username, PolicyName=policy)
            policy_statements.append(
                {
                    "policyname": policy,
                    "statement": response["PolicyDocument"]["Statement"],
                }
            )
    except Exception as e:
        print(e)
    
    overlapping_policies = conflicting_policy(policy_statements)
    plot(overlapping_policies)


if __name__ == "__main__":
    main()
