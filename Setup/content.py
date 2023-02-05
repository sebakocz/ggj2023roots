from datetime import datetime

from Database.Models.node import Node
from constants import timeout


async def cleanup_all_content():
    nodes = await Node.all()

    for node in nodes:
        if node.content != {}:
            try:
                if node.content[list(node.content.keys())[0]]["created_at"] + timeout < datetime.utcnow().timestamp():
                    node.content = {}
                    await node.save()
            except KeyError:
                pass