import asyncio
import datetime
import json
import logging
import psutil
import platform
import sys
from pathlib import Path
from typing import Any

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types  # Used for constructing user messages

logging.basicConfig(level=logging.WARNING)  
LOG_FILE = Path("agent_logs.json")


def write_log(tool_used: str, user_input: str, response: str):
    """Write a log entry to the JSON log file."""
    try:
        logs = []
        if LOG_FILE.exists():
            try:
                with open(LOG_FILE, 'r') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
        
        log_entry = {
            "TOOL_USED": tool_used,
            "TIMESTAMP": datetime.datetime.now().isoformat(),
            "USER_INPUT": user_input,
            "RESPONSE": response
        }
        
        logs.append(log_entry)
        
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to write log: {e}")

#tools
def gettime() -> str:
    """
    Returns the current server time in a structured JSON format.
    Use this tool when the user asks for the current time, date, or timestamp.
    
    Returns:
        str: JSON string with current time information
    """
    now = datetime.datetime.now()
    result = {
        "timestamp": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day_of_week": now.strftime("%A"),
        "timezone": "Local"
    }
    return json.dumps(result)


def get_system_metrics() -> str:
    """
    Returns current system metrics in a structured JSON format.
    Use this tool when the user asks about system performance, resource usage, or system status.
    
    Returns:
        str: JSON string containing system metrics
    """
    try:
        # Quick CPU check (no interval for speed)
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)
        
        # Memory Information
        memory = psutil.virtual_memory()
        
        # Disk Information
        disk = psutil.disk_usage('/')
        
        # System Information
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime_seconds = (datetime.datetime.now() - boot_time).total_seconds()
        
        metrics = {
            "status": "success",
            "system": {
                "platform": platform.system(),
                "hostname": platform.node(),
                "uptime_hours": round(uptime_seconds / 3600, 2)
            },
            "cpu": {
                "usage_percent": round(cpu_percent, 1),
                "cores": cpu_count_logical,
                "physical_cores": cpu_count_physical
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "usage_percent": round(memory.percent, 1)
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "usage_percent": round(disk.percent, 1)
            }
        }
        
        return json.dumps(metrics)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": str(e)
        })
