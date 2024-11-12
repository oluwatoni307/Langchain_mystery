# app.py
from flask import Flask, Response, render_template, jsonify
import json
import time
import threading
from graph import message_queue, runcov

app = Flask(__name__)

# Add these at the top of app.py
import threading
from typing import Optional
import ctypes

class ThreadController:
    def __init__(self):
        self.current_thread: Optional[threading.Thread] = None
        self._thread_lock = threading.Lock()
    
    def set_current_thread(self, thread: threading.Thread) -> None:
        """Safely set the current thread"""
        with self._thread_lock:
            self.current_thread = thread
    
    def clear_current_thread(self) -> None:
        """Safely clear the current thread reference"""
        with self._thread_lock:
            self.current_thread = None
    
    def terminate_thread(self) -> bool:
        """Terminate the currently running thread if it exists"""
        with self._thread_lock:
            if self.current_thread is None or not self.current_thread.is_alive():
                return False
            
            # Get the thread identifier
            thread_id = self.current_thread.ident
            
            if thread_id is None:
                return False
                
            # Raise SystemExit exception in the thread
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(thread_id), 
                ctypes.py_object(SystemExit)
            )
            
            if res > 1:
                # Something went wrong, clear the exception state
                ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), None)
                return False
                
            return True

# Create a global thread controller
thread_controller = ThreadController()

def run_background_task():
    """Run the coverage task in background"""
    try:
        runcov()
    except (SystemExit, Exception) as e:
        if isinstance(e, SystemExit):
            message_queue.put({"type": "info", "message": "Coverage task terminated"})
        else:
            message_queue.put({"type": "error", "message": str(e)})
    finally:
        thread_controller.clear_current_thread()

@app.route("/stream")
def stream():
    def generate():
        # Terminate any existing thread first
        thread_controller.terminate_thread()
        
        # Start new thread
        thread = threading.Thread(target=run_background_task)
        thread.daemon = True
        thread_controller.set_current_thread(thread)
        thread.start()

        while True:
            if not message_queue.empty():
                msg = message_queue.get()
                yield f"data: {json.dumps(msg)}\n\n"
            time.sleep(1.5)

    return Response(generate(), mimetype="text/event-stream")

@app.route("/terminate", methods=["POST"])
def terminate_coverage():
    """Endpoint to terminate the running coverage task"""
    success = thread_controller.terminate_thread()
    return {
        "success": success,
        "message": "Coverage task terminated" if success else "No running coverage task found"
    }

@app.route("/")
def index():
    return render_template("frontend.html")

@app.route('/keep-awake', methods=['GET'])
def keep_awake():
    return jsonify(message="Server is awake"), 200





from phases.blueprint import update_api
from phases.prompt import *

from phases.Kouhei import kouhei_backstory
from phases.masami import masami_backstory
from phases.susumu import susumu_backstory
from phases.cues import *

app.register_blueprint(
    update_api, url_prefix="/api"
)  # You can change the URL prefix as needed


@app.route("/backstory")
def backstory():
    return render_template(
        "backstories_nd_clues.html",
        kouhei_backstory=kouhei_backstory,
        susumu_backstory=susumu_backstory,
        masami_backstory=masami_backstory,
        general_clues=cue,
        personal_clues=personal_cues,
    )


@app.route("/phases")
def Phase_prompt():
    return render_template(
        "phases.html",
        phase_1_prompt=phase_1_prompt,
        phase_2_prompt=phase_2_prompt,
        phase_3_prompt=phase_3_prompt,
        phase_4_prompt=phase_4_prompt,
        phase_5_prompt=phase_5_prompt,
    )


if __name__ == "__main__":
    app.run(debug=True)
