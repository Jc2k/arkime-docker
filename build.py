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

for line in lines:
    if not line:
        continue

    _, ref = line.split("\t")

    if not ref.startswith("refs/tags/v"):
        continue

    ref = ref[11:]

    if "-" in ref:
        print(f"Ignoring {ref} because it contains a '-'")
        continue

    if LooseVersion(ref) < LooseVersion("3"):
        print(f"Ignoring {ref} as too old")
        continue

    resp = session.get("https://quay.io/v2/jc2k/arkime/manifests/{ref}")
    if resp.status_code == 200:
        print(f"Ignoring {ref} as already on quay.io")
        continue

    subprocess.check_call(
        ["docker", "build", "-t", f"quay.io/jc2k/arkime:{ref}", "--build-arg", f"VERSION={ref}", "."]
    )

    subprocess.check_call(
        ["docker", "push", f"quay.io/jc2k/arkime:{ref}"]
    )

    raise RuntimeError("Forcing stop")
