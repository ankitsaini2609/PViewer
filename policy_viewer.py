import argparse
import boto3, boto3.session
import os
import sys

AWS_PROFILE = os.getenv('AWS_PROFILE')
session = boto3.session.Session(profile_name=AWS_PROFILE)
iam_client = session.client('iam')
iam_resource = session.resource('iam')


conflicting_policy(policy_statements)


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
    
    conflicting_policy(policy_statements)


    






if __name__ == "__main__":
    main()
