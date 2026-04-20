# Web UI for Travel Planning Agent

A beautiful, responsive web interface for the Travel Planning Agent System using FastAPI and Bootstrap.

## Features

✨ **Responsive Design**
- Mobile-friendly interface with Bootstrap 5
- Beautiful gradient backgrounds and modern UI
- Intuitive form layout

🚀 **FastAPI Backend**
- High-performance async API
- Form-based trip planning
- JSON API endpoint for integrations
- Health check endpoint

📱 **User-Friendly Forms**
- Destination input with comma separation
- Date picker with validation
- Budget and travel style selection
- Interest selection
- Traveler count selection

📊 **Results Display**
- Ranked destinations with match scores
- Daily itinerary with activities
- Budget breakdown and recommendations
- AI insights and suggestions
- Statistics dashboard

## Installation

### 1. Install Dependencies

```bash
cd web_ui
pip install -r requirements.txt
```

### 2. Required Dependencies

- FastAPI>=0.100.0
- uvicorn>=0.23.0
- jinja2>=3.0.0

### 3. From Project Root

All travel agent dependencies should already be installed. If not:

```bash
pip install -r ../requirements.txt
```

## Running the Application

### Option 1: Direct Python

```bash
python app.py
```

The app will start on `http://localhost:8000`

### Option 2: Using Uvicorn

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Using Shell Script

```bash
chmod +x run.sh
./run.sh
```

## Access the Web UI

Once running, open your browser and navigate to:

```
http://localhost:8000
```

Or if running on a server:
```
http://your-server-ip:8000
```

## Project Structure

```
web_ui/
├── app.py                    # FastAPI application
├── requirements.txt          # Python dependencies
├── run.sh                   # Startup script
├── templates/
│   ├── index.html           # Trip planning form
│   ├── results.html         # Trip results display
│   └── error.html           # Error page
└── static/                  # CSS/JS (optional)
```

## API Endpoints

### GET `/`
Home page with trip planning form

### POST `/plan-trip`
Submit form to generate trip plan
- Redirects to results page with HTML rendering

### POST `/api/plan-trip`
JSON API endpoint
- Request: JSON with trip parameters
- Response: JSON with trip plan

### GET `/health`
Health check endpoint

## Form Parameters

| Parameter | Type | Required | Notes |
|-----------|------|----------|-------|
| destinations | string | ✓ | Comma-separated list |
| start_date | date | ✓ | YYYY-MM-DD format |
| end_date | date | ✓ | YYYY-MM-DD format |
| budget | integer | ✓ | USD amount |
| travel_style | string | ✓ | budget, comfort, luxury |
| interests | string | ✓ | Comma-separated list |
| travelers | integer | ✓ | Number of travelers (1-20) |

## Features Demonstrated

### 1. Intelligent Trip Planning
- Uses all 3 agents (Destination, Itinerary, Budget)
- LLM-based reasoning
- Google API integration
- Machine Learning personalization

### 2. User Experience
- Step-by-step form guidance
- Real-time validation
- Beautiful results display
- Error handling with helpful messages

### 3. Web Integration
- RESTful API design
- JSON support for integrations
- HTML template rendering
- Bootstrap responsive design

## Deployment Options

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker (if available)
```bash
docker build -t travel-agent-ui .
docker run -p 8000:8000 travel-agent-ui
```

### Deploy on Heroku
```bash
git add .
git commit -m "Add web UI"
git push heroku main
```

## Configuration

### Environment Variables
```bash
GOOGLE_MAPS_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
LOG_LEVEL=INFO
```

### Customization
Edit `templates/` files to customize appearance
Edit `app.py` to modify backend logic

## Troubleshooting

### Port 8000 Already in Use
```bash
python app.py --port 8001
```

### Template Not Found Error
Ensure you're running from the `web_ui/` directory or adjust the templates path

### Import Errors
Make sure parent directory is in PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:../"
python app.py
```

## Next Steps

1. **Add Authentication** - User login/registration
2. **Add Payment Integration** - Stripe/PayPal for bookings
3. **Add Email Notifications** - Send trip plans via email
4. **Add Database** - Store user preferences and trips
5. **Add Charts** - Visualize budget and activities
6. **Add Real-time Updates** - WebSocket for live planning

## Technologies Used

- **Backend**: FastAPI, Python 3.8+
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Agents**: Travel Planning Intelligence
- **APIs**: Google Maps, OpenAI GPT
- **UI Framework**: Jinja2 Templates

## License

Same as parent project

## Support

For issues or questions, refer to the main project documentation.
