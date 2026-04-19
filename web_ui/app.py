"""
FastAPI Web Application for Travel Planning Agents
Provides a user-friendly interface for trip planning
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime, date
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from travel_agents.intelligent_orchestrator import TravelPlanningOrchestrator

# Initialize FastAPI app
app = FastAPI(title="Travel Planning Agent", description="AI-Powered Travel Planning")

# Setup templates directory
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))

# Setup static files directory
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
try:
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
except:
    pass

# Initialize orchestrator
orchestrator = TravelPlanningOrchestrator(use_google_api=False)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with travel planning form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/plan-trip", response_class=HTMLResponse)
async def plan_trip(
    request: Request,
    destinations: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    budget: int = Form(...),
    travel_style: str = Form(...),
    interests: str = Form(...),
    travelers: int = Form(...)
):
    """Process trip planning request with agents"""
    try:
        # Parse inputs
        destination_list = [d.strip() for d in destinations.split(",") if d.strip()]
        interest_list = [i.strip() for i in interests.split(",") if i.strip()]
        
        # Parse dates
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        # Validate
        if not destination_list:
            return templates.TemplateResponse(
                "error.html", 
                {"request": request, "error": "Please enter at least one destination"},
                status_code=400
            )
        
        if not interest_list:
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error": "Please enter at least one interest"},
                status_code=400
            )
        
        if start >= end:
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error": "Start date must be before end date"},
                status_code=400
            )
        
        if budget <= 0:
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error": "Budget must be greater than 0"},
                status_code=400
            )
        
        # Call orchestrator to plan trip
        trip_plan = orchestrator.plan_trip(
            destinations=destination_list,
            start_date=start,
            end_date=end,
            budget=budget,
            travel_style=travel_style,
            interests=interest_list,
            number_of_travelers=travelers
        )
        
        # Format results for display
        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "trip": trip_plan,
                "total_days": (end - start).days,
                "avg_daily_budget": budget / ((end - start).days or 1)
            }
        )
        
    except ValueError as ve:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": f"Invalid input: {str(ve)}"},
            status_code=400
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": f"Error planning trip: {str(e)}"},
            status_code=500
        )

@app.api_route("/api/plan-trip", methods=["POST"])
async def api_plan_trip(request: Request):
    """API endpoint for trip planning (returns JSON)"""
    try:
        data = await request.json()
        
        destination_list = data.get("destinations", [])
        if isinstance(destination_list, str):
            destination_list = [d.strip() for d in destination_list.split(",")]
        
        start = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
        end = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()
        
        trip_plan = orchestrator.plan_trip(
            destinations=destination_list,
            start_date=start,
            end_date=end,
            budget=int(data.get("budget")),
            travel_style=data.get("travel_style", "comfort"),
            interests=data.get("interests", []),
            number_of_travelers=int(data.get("travelers", 1))
        )
        
        return JSONResponse({"status": "success", "trip": trip_plan})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Travel Planning Agent API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
