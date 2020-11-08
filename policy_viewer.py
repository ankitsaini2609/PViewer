import argparse
import boto3, boto3.session
from collections import defaultdict
from graphviz import Graph
import os
import sys

AWS_PROFILE = os.getenv('AWS_PROFILE')
session = boto3.session.Session(profile_name=AWS_PROFILE)
iam_client = session.client('iam')
iam_resource = session.resource('iam')


def check(conflict_tracker, policy1, policy2):  # This function will check if those two policy already conflicting.
    for policy in conflict_tracker[policy1['policyname']]:
        if policy == policy2['policyname']:
            return False
    return True


def conflicting_policy(policy_statements):
    conflict_tracker = defaultdict(list)  # It will track which policy is conflicting to others.
    for policy1 in policy_statements:
        for statement1 in policy1['statement']:
            if statement1['Effect'] == 'Allow':
                if type(statement1['Action']) == unicode:
                    actions = [action for action in statement1['Action'].split()]
                else:
                    actions = statement1['Action']
                for action1 in actions:
                    service1, permission1 = action1.split(':', 1)
                    for policy2 in policy_statements:
                        flag = False
                        if policy1 != policy2 and check(conflict_tracker, policy1, policy2):
                            for statement2 in policy2['statement']:
                                if statement2['Effect'] == 'Allow':
                                    if type(statement2['Action']) == unicode:
                                        actions = [action for action in statement2['Action'].split()]  
                                    else:
                                        actions = statement2['Action']
                                    for action2 in actions:
                                        service2, permission2 = action2.split(':', 1)
                                        if (service1 == service2) and (permission1 == permission2 or permission2 == '*' or permission1 == '*') and (statement1['Resource'] == '*' or statement2['Resource'] == '*' or statement1['Resource'] == statement2['Resource']):
                                            conflict_tracker[policy1['policyname']].append(policy2['policyname'])
                                            conflict_tracker[policy2['policyname']].append(policy1['policyname'])
                                            flag = True
                                        if flag:
                                            break
                                    if flag:
                                            break
                            if flag:
                                continue
    return conflict_tracker


def plot(overlapping_policies):
    g = Graph('G', filename='Overlapping_policies', engine='sfdp')
    for key in overlapping_policies.keys():
        for value in overlapping_policies[key]:
            g.edge(key, value)
            overlapping_policies[value].remove(key)
    g.view()


def main():
    # Argument Parsing
    parser = argparse.ArgumentParser(usage='%(prog)s -u username')
    parser.add_argument('-u', '--username', help='User Name')
    args = parser.parse_args() 
    username = args.username
    policy_statements = list()
    # fetching managed policies
    try:
        user = iam_resource.User(username)
        policies = user.attached_policies.all()
        for policy in policies:
            policyname = policy.arn.split('/')[-1]
            policy_statements.append({'policyname':policyname, 'statement':policy.default_version.document['Statement']})
    except Exception as e:
        print(e)
    # fetching inline policies
    try:    
        response = iam_client.list_user_policies(UserName=username)
        list_of_policies = response['PolicyNames']
        for policy in list_of_policies:
            response = iam_client.get_user_policy(UserName=username, PolicyName=policy)
            policy_statements.append({'policyname':policy, 'statement':response['PolicyDocument']['Statement']})
    except Exception as e:
        print(e)
    
    overlapping_policies = conflicting_policy(policy_statements)
    plot(overlapping_policies)


if __name__ == "__main__":
    main()
