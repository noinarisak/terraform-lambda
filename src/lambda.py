# -*- coding: utf-8 -*-

import os
import subprocess
import urllib

import boto3


def check_call(args):
    """Wrapper for subprocess that checks if a process runs correctly,
    and if not, prints stdout and stderr.
    """
    proc = subprocess.Popen(args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd='/tmp',
        universal_newlines=True)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        print(stdout)
        print(stderr)
        raise subprocess.CalledProcessError(
            returncode=proc.returncode,
            cmd=args)

    print(stdout)

def apply_terraform_plan(s3_bucket, path):
    """Download a Terraform plan from S3, decompress zip run a 'terraform' steps.

    :param s3_bucket: Name of the S3 bucket where the plan is stored.
    :param path: Path to the Terraform planfile in the S3 bucket.

    """
    # Although the /tmp directory may persist between invocations, we always
    # download a new copy of the tf_bundle_file, as it may have changed externally.
    s3 = boto3.resource('s3')
    tf_bundle_file = s3.Object(s3_bucket, path)
    tf_bundle_file.download_file('/tmp/tf-example.zip')

    # Flags:
    #   '-o' = overwrite existing files without prompting
    #   '-d' = output directory
    check_call(['unzip', '-o', '/tmp/tf-example.zip', '-d', '/tmp/'])

    TERRAFORM_DIR = '/tmp/build/tf-example/terraform_bundle/'
    TERRAFORM_PATH = os.path.join(TERRAFORM_DIR, 'terraform')

    check_call(['ls', '-la', '/tmp'])

    AWS_ACCESS_KEY = "access_key={}".format(os.environ['aws_access_key_id'])
    AWS_SECRET_EKY = "secret_key={}".format(os.environ['aws_secret_access_key'])

    print("AWS_ACCESS_KEY: " + AWS_ACCESS_KEY)
    print("AWS_SECRET_KEY: " + AWS_SECRET_KEY)

    # check_call([TERRAFORM_PATH, '--version'])
    # check_call([TERRAFORM_PATH, 'init', '-input=false', '-plugin-dir=/tmp/build/tf-example/terraform_bundle/', '/tmp/build/tf-example' ])
    # check_call([TERRAFORM_PATH, 'plan', '-input=false', '-lock=false', '-out=/tmp/build/tf-example/tfplan', '-var', AWS_ACCESS_KEY,  '-var', AWS_SECRET_KEY, '/tmp/build/tf-example'])
    # check_call([TERRAFORM_PATH, 'apply', '-input=false', '-auto-approve', '/tmp/build/tf-example/tfplan'])

def handler(event, context):
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    path = event['Records'][0]['s3']['object']['key']

    print("path: " + path)
    print("s3_bucket: " + s3_bucket)

    apply_terraform_plan(s3_bucket=s3_bucket, path=path)
