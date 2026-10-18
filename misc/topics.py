from html import escape

from infrastructure.database.models import Topic
from misc import texts


def render_topic(topic: Topic) -> str:
    lines = [texts.TOPIC_HEADER.format(base=escape(topic.base), title=escape(topic.title), free=topic.free_slots)]
    for slot in topic.slots:
        line = texts.TOPIC_SLOT.format(position=slot.position, price=slot.price)
        lines.append(line + (texts.TOPIC_SOLD if slot.sold else ""))
    return "\n".join(lines)
