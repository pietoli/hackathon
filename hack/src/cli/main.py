import argparse as ap
from pprint import pprint
import logging
from src.cli.chat import check_fact, prepare_query
from src.cli.utils import get_human_template, get_system_template
from src.cli.download_context import get_context
parser = ap.ArgumentParser()
parser.add_argument("--input")
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)

def main(query: str) -> str:
    logging.debug("User query %s", query)
    logging.debug("Query preprocessing")
    keywords = prepare_query(query)

    logging.debug("Getting context")
    context = get_context(query=query)
    logging.debug("Context prepared")

    logging.debug("Checking fact")
    info = check_fact(
        query,
        context_data=' '.join(context.values()),
        user_prompt_template=get_human_template(),
        system_prompt_template=get_system_template(),
    )
    logging.debug("Fact checked")



    return keywords, info


if __name__ == "__main__":
    pprint(main(args.input))
