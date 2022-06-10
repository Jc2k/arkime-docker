#! /usr/bin/env python

import subprocess
from distutils.version import LooseVersion
from httpx import Client

session = Client()

result = subprocess.run(
    ["git", "ls-remote", "https://github.com/arkime/arkime"],
    capture_output=True
)

if result.returncode != 0:
    raise RuntimeError("Failed to query available tags")

lines = result.stdout.decode("utf-8").split("\n")
lines = filter(lambda line: line != "", lines)
lines = map(lambda line: line.split("\t")[1], lines)
lines = filter(lambda line: line.startswith("refs/tags/v"), lines)
lines = map(lambda line: line[11:], lines)
lines = filter(lambda ref: LooseVersion(ref) >= LooseVersion("3"), lines)
lines = list(lines)
lines.sort(key=LooseVersion, reverse=True)

for ref in lines:
    if "-" in ref:
        print(f"Ignoring {ref} because it contains a '-'")
        continue

    resp = session.get(f"https://quay.io/v2/jc2k/arkime/manifests/{ref}")
    if resp.status_code == 200:
        print(f"Ignoring {ref} as already on quay.io")
        continue

    subprocess.check_call(
        ["docker", "build", "-t", f"quay.io/jc2k/arkime:{ref}", "--build-arg", f"VERSION={ref}", "."]
    )

    subprocess.check_call(
        ["docker", "push", f"quay.io/jc2k/arkime:{ref}"]
    )
