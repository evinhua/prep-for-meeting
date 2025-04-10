from flask import Flask, request, jsonify, send_file
import subprocess
import os
import json
import tempfile
import time
import threading
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store job status
jobs = {}

def update_progress(job_id, stop_event):
    """Update the progress of a job periodically."""
    progress = 0
    while not stop_event.is_set() and progress < 95:
        time.sleep(2)  # Update every 2 seconds
        progress += 5  # Increment by 5%
        jobs[job_id]['progress'] = progress
    
    # Final update to 95% if not stopped
    if not stop_event.is_set():
        jobs[job_id]['progress'] = 95

@app.route('/api/run-crew', methods=['POST'])
def run_crew():
    try:
        # Get input data from request
        data = request.json
        
        # Generate a unique job ID
        job_id = str(int(time.time()))
        
        # Store job information
        jobs[job_id] = {
            'status': 'running',
            'progress': 0,
            'output_file': None,
            'error': None
        }
        
        # Start a thread to run the CrewAI process
        thread = threading.Thread(
            target=run_crewai_process,
            args=(job_id, data)
        )
        thread.start()
        
        return jsonify({
            'job_id': job_id,
            'status': 'running'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def run_crewai_process(job_id, data):
    try:
        # Get the correct project root directory - one level up from the api directory
        api_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(api_dir, '..'))
        print(f"Project root: {project_root}")
        
        # Create a temporary .env file with our inputs
        env_path = os.path.join(project_root, '.env')
        
        # Backup existing .env file if it exists
        env_backup = None
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                env_backup = f.read()
            print("Backed up existing .env file")
        
        # Write our inputs to .env file
        with open(env_path, 'w') as f:
            # Keep OPENAI_API_KEY if it was in the backup
            if env_backup and 'OPENAI_API_KEY' in env_backup:
                for line in env_backup.splitlines():
                    if line.startswith('OPENAI_API_KEY'):
                        f.write(f"{line}\n")
            
            # Write our custom inputs
            f.write(f"PARTICIPANTS={','.join(data['participants'])}\n")
            f.write(f"COMPANY={data['company']}\n")
            f.write(f"CONTEXT={data['context']}\n")
            f.write(f"OBJECTIVE={data['objective']}\n")
            f.write(f"PRIOR_INTERACTIONS={data['prior_interactions']}\n")
            # Add the SERPER_API_KEY if it doesn't exist
            f.write(f"SERPER_API_KEY=your_serper_api_key_here\n")
        
        # Modify main.py to read from environment variables
        main_py_path = os.path.join(project_root, 'src', 'prep_for_meeting', 'main.py')
        main_py_backup = None
        
        if os.path.exists(main_py_path):
            with open(main_py_path, 'r') as f:
                main_py_backup = f.read()
            
            # Create a modified version that reads from environment variables
            modified_content = """#!/usr/bin/env python
import sys
import os

from prep_for_meeting.crew import PrepForMeetingCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    \"\"\"
    Run the crew.
    \"\"\"

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
    \"\"\"
    Train the crew for a given number of iterations.
    \"\"\"
    inputs = {"topic": "AI LLMs"}
    try:
        PrepForMeetingCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    \"\"\"
    Replay the crew execution from a specific task.
    \"\"\"
    try:
        PrepForMeetingCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    \"\"\"
    Test the crew execution and returns the results.
    \"\"\"
    inputs = {"topic": "AI LLMs"}
    try:
        PrepForMeetingCrew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")"""
            
            with open(main_py_path, 'w') as f:
                f.write(modified_content)
            
            print("Modified main.py to read from environment variables")
        
        # Run the crewai run command using a shell script
        print(f"Running shell script in directory: {project_root}")
        
        # Path to the shell script
        script_path = os.path.join(project_root, 'run_crewai.sh')
        
        # Change to the project root directory before running the command
        current_dir = os.getcwd()
        os.chdir(project_root)
        
        # Start a thread to update progress periodically
        stop_progress_thread = threading.Event()
        progress_thread = threading.Thread(
            target=update_progress,
            args=(job_id, stop_progress_thread)
        )
        progress_thread.start()
        
        try:
            # Run the shell script
            result = subprocess.run(
                ['/bin/bash', script_path],
                capture_output=True,
                text=True,
                env={**os.environ, 'SERPER_API_KEY': 'your_serper_api_key_here'}  # Add the missing API key
            )
            
            # Stop the progress thread
            stop_progress_thread.set()
            progress_thread.join()
            
            print(f"Shell script output: {result.stdout}")
            print(f"Shell script error: {result.stderr}")
        finally:
            # Change back to the original directory
            os.chdir(current_dir)
        
        # Check for output files
        report_path = os.path.join(project_root, 'report.md')
        pptx_path = None
        
        # Look for any .pptx files in the project root
        for file in os.listdir(project_root):
            if file.endswith('.pptx'):
                pptx_path = os.path.join(project_root, file)
                break
        
        # Print debug information
        print(f"Command execution result: {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        print(f"Report path exists: {os.path.exists(report_path)}")
        print(f"PowerPoint path: {pptx_path}")
        
        # Update job status based on the output
        if result.returncode == 0:
            # Read the report content
            report_content = ""
            if os.path.exists(report_path):
                with open(report_path, 'r') as f:
                    report_content = f.read()
                    # Update the timestamp in the report to show it's newly generated
                    report_content = report_content.replace("April 2025", f"April {time.strftime('%d')}, 2025")
                # Write the updated report back
                with open(report_path, 'w') as f:
                    f.write(report_content)
                print(f"Report content length: {len(report_content)}")
            elif pptx_path:
                report_content = f"PowerPoint presentation generated: {os.path.basename(pptx_path)}"
            else:
                # If no report.md or .pptx file was found, create a simple report with the command output
                report_content = f"Command output:\n\n{result.stdout}"
                report_path = os.path.join(project_root, 'command_output.txt')
                with open(report_path, 'w') as f:
                    f.write(report_content)
            
            # Store the output file path
            jobs[job_id]['status'] = 'completed'
            jobs[job_id]['progress'] = 100
            jobs[job_id]['output_file'] = pptx_path if pptx_path else report_path
            jobs[job_id]['content'] = report_content
        else:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['error'] = result.stderr
        
        # Restore original main.py if we backed it up
        if main_py_backup:
            with open(main_py_path, 'w') as f:
                f.write(main_py_backup)
            print("Restored original main.py")
        
        # Restore original .env if we backed it up
        if env_backup:
            with open(env_path, 'w') as f:
                f.write(env_backup)
            print("Restored original .env file")
        
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)
        print(f"Error in run_crewai_process: {e}")
        
        # Attempt to restore backups if there was an error
        try:
            if 'main_py_backup' in locals() and main_py_backup:
                with open(main_py_path, 'w') as f:
                    f.write(main_py_backup)
                print("Restored original main.py after error")
            
            if 'env_backup' in locals() and env_backup:
                with open(env_path, 'w') as f:
                    f.write(env_backup)
                print("Restored original .env file after error")
        except Exception as restore_error:
            print(f"Error restoring backups: {restore_error}")

@app.route('/api/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    if job_id not in jobs:
        return jsonify({
            'status': 'error',
            'message': 'Job not found'
        }), 404
    
    job = jobs[job_id]
    
    response = {
        'status': job['status'],
        'progress': job['progress']
    }
    
    if job['status'] == 'completed':
        # If there's an output file, provide a download URL
        if job['output_file']:
            response['downloadUrl'] = f'/api/download/{job_id}'
            response['content'] = job.get('content', '')
            print(f"Returning completed job with content length: {len(job.get('content', ''))}")
    
    elif job['status'] == 'failed':
        response['error'] = job['error']
    
    return jsonify(response)

@app.route('/api/download/<job_id>', methods=['GET'])
def download_file(job_id):
    if job_id not in jobs or jobs[job_id]['status'] != 'completed':
        return jsonify({
            'status': 'error',
            'message': 'File not available'
        }), 404
    
    output_file = jobs[job_id]['output_file']
    
    if not output_file or not os.path.exists(output_file):
        return jsonify({
            'status': 'error',
            'message': 'File not found'
        }), 404
    
    return send_file(
        output_file,
        as_attachment=True,
        download_name=os.path.basename(output_file)
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
