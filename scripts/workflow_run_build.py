import os
import requests
import argparse

from requests.auth import HTTPBasicAuth


BUILD_WF_URL = ("https://api.github.com/repos/megacorpincorporated/hint/"
                "actions/workflows/5880406/dispatches")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Must define $GITHUB_USERNAME and $HINT_WORKFLOW_TOKEN. "
                    "The token should be a GitHub PAT with repo access."
    )
    parser.add_argument(
        "ref",
        type=str,
        help="Branch or tag name to run the workflow on."
    )
    return parser.parse_args()


args = parse_args()
gh_username = os.environ.get("GITHUB_USERNAME")
hint_wf_token = os.environ.get("HINT_WORKFLOW_TOKEN")
if gh_username is None or hint_wf_token is None:
    raise SystemError("Missing $GITHUB_USERNAME or $HINT_WORKFLOW_TOKEN")

response = requests.post(BUILD_WF_URL,
                         json={"ref": args.ref},
                         auth=HTTPBasicAuth(gh_username, hint_wf_token))

if response.status_code == 204:
    print("Workflow successfully triggered!")
else:
    print(response.text)
