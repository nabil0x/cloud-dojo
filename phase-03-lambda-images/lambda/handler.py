"""Dojo Lambda handler.

Q3.1: build an image FROM the AWS base image with this file as the handler.
Q3.3: invoke with {"name": "ada"} and read back the greeting.
Q3.4: wire it to SQS/S3 and watch `event` arrive for real.
"""


def handler(event, context):
    name = (event or {}).get("name", "dojo")
    return {"ok": True, "hello": name}
