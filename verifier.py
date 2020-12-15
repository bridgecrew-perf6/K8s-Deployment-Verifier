import argparse
import sys
import subprocess
import time

TIME_TO_WAIT = 10


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def parse_command_line_args():
    parser = argparse.ArgumentParser(
        description="Simple tool to verify kubernetes deployments"
    )

    parser.add_argument(
        '--deployment',
        '-d',
        required=True,
        default=None,
        help='Deployment Name'
    )

    parser.add_argument(
        '--namespace',
        '-n',
        required=False,
        default=None,
        help='Namespace name'
    )

    parser.add_argument(
        '--project',
        '-p',
        required=False,
        default=None,
        help='GCP Project ID'
    )

    parser.add_argument(
        '--zone',
        '-z',
        required=False,
        default=None,
        help='GKE Cluster Zone'
    )

    parser.add_argument(
        '--cluster',
        '-c',
        required='--get-credentials' in sys.argv,
        help='Cluster Name'
    )

    parser.add_argument(
        '--get-credentials',
        required=False,
        default=False,
        type=str2bool,
        help='Fetch GKE Kubectl credentials.'
    )

    return parser.parse_args()


def get_credentials(cluster_name, project_id=None, zone=None):
    print("---FETCHING CREDENTIALS---")
    command = ['gcloud', 'container', 'clusters', 'get-credentials', cluster_name]

    if project_id is not None:
        command.append('--project')
        command.append(project_id)

    if zone is not None:
        command.append('--zone')
        command.append(zone)

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode:
        exit(process.returncode)
    else:
        print("---CREDENTIALS FETCHED---")


def get_deployment_status(deployment_name, namespace=None):
    command = ['kubectl', 'get', 'deployment', deployment_name]

    if namespace:
        command.append('--namespace')
        command.append(namespace)

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode:
        exit(process.returncode)
    else:
        if stdout != "":
            status = stdout.decode('utf-8').split('\n')[1]
        else:
            status = stderr.decode('utf-8').split('\n')[1]
        statusline = " ".join(status.split()).split()
        ready = statusline[1]
        return ready


def check_deployment(deployment_name, namespace=None):
    print("---CHECKING DEPLOYMENT STATUS---")
    for i in range(TIME_TO_WAIT):
        ready = get_deployment_status(deployment_name=deployment_name, namespace=namespace)
        available = ready.split("/")[0]
        total = ready.split("/")[1]

        print("{} out of {} pods available.".format(available, total))

        if available == total:
            print("{} is ready!".format(deployment_name))
            return True

        time.sleep(1)
    print("{} is not ready!".format(deployment_name))
    return False


if __name__ == '__main__':
    args = parse_command_line_args()

    if args.get_credentials:
        get_credentials(
            cluster_name=args.cluster,
            project_id=args.project,
            zone=args.zone
        )

    status = check_deployment(deployment_name=args.deployment, namespace=args.namespace)

    print("---DONE---")

    if status:
        exit(0)
    else:
        exit(1)
