# Healthcare Search Assistant Chat UI

A modern, responsive chat interface for searching healthcare data using semantic search and OpenSearch.

## 🚀 Quick Start

### Prerequisites
- Python 3.13.3+
- Virtual environment activated
- OpenSearch Docker container running
- Gemini API key configured

### Start the Chat UI

```bash
# From the chat_ui directory
./start.sh

# Or manually
source ../venv/bin/activate
python start_server.py
```

The chat interface will be available at:
- **Frontend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 🎯 Features

### Chat Interface
- **Real-time Chat**: Interactive conversation with the healthcare search assistant
- **Quick Queries**: Pre-defined query buttons for common searches
- **Message History**: Persistent chat history during session
- **Auto-scroll**: Automatic scrolling to latest messages

### Search Results
- **Document Cards**: Rich display of search results with key information
- **Multiple Data Types**: Support for claims, providers, procedures, and members
- **Export Functionality**: Download results as CSV
- **Load More**: Pagination for large result sets

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark/Light Theme**: Toggle between themes with system preference detection
- **Keyboard Shortcuts**: Quick navigation and actions
- **Connection Status**: Real-time connection monitoring
- **Error Handling**: Graceful error handling with user-friendly messages

## 🏗️ Architecture

### Frontend (Static Files)
```
chat_ui/
├── index.html              # Main HTML structure
├── styles/
│   ├── main.css           # Core styles and layout
│   ├── components.css     # Component-specific styles
│   └── responsive.css     # Responsive design
├── scripts/
│   ├── app.js            # Main application logic
│   ├── chat.js           # Chat functionality
│   └── api.js            # API client and utilities
└── assets/
    ├── icons/            # SVG icons
    └── images/           # Images and graphics
```

### Backend (FastAPI)
```
chat_ui/backend/
└── app.py                # FastAPI application with all endpoints
```

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - Serve the chat UI frontend
- `GET /api/health` - Health check and system status
- `POST /api/search` - Search healthcare data
- `POST /api/chat` - Chat with the assistant
- `GET /api/indices` - List available OpenSearch indices
- `GET /api/suggestions` - Get quick query suggestions

### Request/Response Examples

#### Search Request
```json
{
  "query": "Find claims for John Smith",
  "index_name": "healthcare_claims_index",
  "max_results": 20
}
```

#### Search Response
```json
{
  "success": true,
  "index_name": "healthcare_claims_index",
  "total_hits": 15,
  "documents": [...],
  "execution_time_ms": 45,
  "metadata": {
    "query": "Find claims for John Smith",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

#### Chat Request
```json
{
  "message": "Show me recent claims",
  "conversation_history": [...]
}
```

#### Chat Response
```json
{
  "response": "I found 12 recent claims...",
  "search_results": {...},
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🎨 UI Components

### Layout
- **Left Panel**: Search results display with document cards
- **Right Panel**: Chat interface with message history
- **Header**: Application title, connection status, and settings
- **Footer**: Quick query buttons and input area

### Document Cards
Each search result is displayed as a rich card showing:
- **Document Type**: Claims, Provider, Procedure, or Member
- **Key Fields**: Most relevant information for each data type
- **Actions**: View details and export options
- **Status Indicators**: Visual status representations

### Chat Messages
- **User Messages**: Right-aligned with user avatar
- **Assistant Messages**: Left-aligned with bot avatar
- **Welcome Message**: Initial guidance and feature overview
- **Error Messages**: User-friendly error handling

## ⌨️ Keyboard Shortcuts

- `Ctrl/Cmd + K` - Focus search input
- `Ctrl/Cmd + /` - Show keyboard shortcuts help
- `Enter` - Send message
- `Shift + Enter` - New line in input
- `Escape` - Close modals

## 🔧 Configuration

### Settings
Access settings via the settings button in the header:

- **Theme**: Light, Dark, or Auto (system preference)
- **Results Per Page**: Number of results to display (10-100)
- **Auto-save**: Automatically save settings every 30 seconds
- **Notifications**: Enable/disable toast notifications

### Environment Variables
The backend automatically uses the same configuration as the main application:
- `GEMINI_API_KEY` - Required for LLM integration
- Configuration files in `../configurations/`

## 🚨 Troubleshooting

### Common Issues

1. **Connection Failed**
   - Ensure OpenSearch Docker container is running
   - Check if port 8000 is available
   - Verify API key configuration

2. **No Search Results**
   - Verify OpenSearch indices have data
   - Check if the query is properly formatted
   - Ensure the backend components are initialized

3. **UI Not Loading**
   - Check browser console for JavaScript errors
   - Ensure all CSS and JS files are accessible
   - Try clearing browser cache

### Debug Mode
Enable debug logging by setting the log level to debug in `start_server.py`:
```python
uvicorn.run(app, log_level="debug")
```

## 🔒 Security

- **CORS**: Configured for development (allow all origins)
- **API Key**: Securely handled via environment variables
- **Input Validation**: All user inputs are validated and sanitized
- **Error Handling**: No sensitive information exposed in error messages

## 📱 Browser Support

- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS Safari 14+, Chrome Mobile 90+
- **Features**: CSS Grid, Flexbox, ES6+, Fetch API

## 🎯 Performance

- **Caching**: API responses cached for 5 minutes
- **Lazy Loading**: Components loaded as needed
- **Request Queuing**: Max 3 concurrent requests
- **Retry Logic**: Automatic retry for failed requests
- **Optimized Assets**: Minified CSS and JavaScript

## 🚀 Deployment

### Development
```bash
./start.sh
```

### Production
```bash
# Use production WSGI server
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker
```dockerfile
FROM python:3.13-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📊 Monitoring

The application provides several monitoring endpoints:
- `/api/health` - System health and component status
- `/api/stats` - Application statistics (if implemented)
- Browser console logging for debugging

## 🤝 Contributing

1. Follow the existing code style and patterns
2. Add appropriate error handling
3. Update documentation for new features
4. Test on multiple browsers and devices
5. Ensure accessibility standards are met

## 📄 License

This project is part of the Healthcare Semantic Search system.
