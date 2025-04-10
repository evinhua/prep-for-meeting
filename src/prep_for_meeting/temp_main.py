#!/usr/bin/env python
import sys

from prep_for_meeting.crew import PrepForMeetingCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """

    import os

inputs = {
        "participants": os.environ.get("PARTICIPANTS", "").split(",") if os.environ.get("PARTICIPANTS") else [
            'Jensen Huang <jensen.huang@nvidia.com>', 'Mark Zuckerberg <mark.zuckerberg@meta.com>', 'Elon Musk <elon.musk@tesla.coom>'
        ],
        "company": os.environ.get("COMPANY", "Future AI News"),
        "context": os.environ.get("CONTEXT", "Sharing the latest AI news from the recent two weeks"),
        "objective": os.environ.get("OBJECTIVE", "Summarize the latest AI news and creating working action points"),
        "prior_interactions": os.environ.get("PRIOR_INTERACTIONS", "providing latest roadmap in each company"),
    }

    PrepForMeetingCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    import os

inputs = {"topic": "AI LLMs"}
    try:
        PrepForMeetingCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        PrepForMeetingCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    import os

inputs = {"topic": "AI LLMs"}
    try:
        PrepForMeetingCrew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
