#!/usr/bin/env python
import sys
import os
from src.prep_for_meeting.crew import PrepForMeetingCrew

def run():
    inputs = {
        "participants": ['Jensen Huang <jensen.huang@nvidia.com>', 'Mark Zuckerberg <mark.zuckerberg@meta.com>', 'Elon Musk <elon.musk@tesla.coom>'],
        "company": "Future AI News",
        "context": "Sharing the latest AI news from the recent two weeks",
        "objective": "Summarize the latest AI news and creating working action points",
        "prior_interactions": "providing latest roadmap in each company",
    }
    
    print(f"Running with inputs: {inputs}")
    PrepForMeetingCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
