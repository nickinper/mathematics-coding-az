"""FastAPI server for Mathematics-Based Coding AZ platform."""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from pathlib import Path

from .api import challenge_router, submission_router, user_router
from .database import engine, Base


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize FastAPI app
    app = FastAPI(
        title="Mathematics-Based Coding AbsoluteZero",
        description="A learning platform integrating mathematical reasoning with programming",
        version="0.1.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    app.include_router(challenge_router, prefix="/api/challenges", tags=["challenges"])
    app.include_router(submission_router, prefix="/api/submissions", tags=["submissions"])
    app.include_router(user_router, prefix="/api/users", tags=["users"])
    
    # Serve static files
    static_path = Path(__file__).parent / "static"
    if static_path.exists():
        app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    
    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Serve the main application page."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Mathematics-Based Coding AZ</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                }
                .hero {
                    text-align: center;
                    padding: 60px 0;
                }
                .hero h1 {
                    font-size: 3em;
                    margin-bottom: 20px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                .hero p {
                    font-size: 1.3em;
                    margin-bottom: 30px;
                    max-width: 600px;
                    margin-left: auto;
                    margin-right: auto;
                    opacity: 0.9;
                }
                .features {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 30px;
                    margin: 60px 0;
                }
                .feature {
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.2);
                }
                .feature h3 {
                    font-size: 1.5em;
                    margin-bottom: 15px;
                    color: #FFD700;
                }
                .api-links {
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 15px;
                    text-align: center;
                    margin: 40px 0;
                }
                .api-links a {
                    color: #FFD700;
                    text-decoration: none;
                    margin: 0 15px;
                    font-weight: bold;
                    font-size: 1.1em;
                }
                .api-links a:hover {
                    text-decoration: underline;
                }
                .math {
                    font-family: 'Times New Roman', serif;
                    font-style: italic;
                }
            </style>
        </head>
        <body>
            <div class="hero">
                <h1>🧮 Mathematics-Based Coding AZ</h1>
                <p>Where <span class="math">mathematical reasoning</span> meets <strong>computational thinking</strong></p>
                <p>A revolutionary learning platform where code correctness depends on mathematical insight</p>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>🔍 Dual-Layer Verification</h3>
                    <p>Your code must be both functionally correct AND mathematically sound. We verify your algorithms and your mathematical reasoning.</p>
                </div>
                
                <div class="feature">
                    <h3>📚 Progressive Curriculum</h3>
                    <p>From Number Theory through Abstract Algebra, each challenge builds mathematical understanding while developing coding skills.</p>
                </div>
                
                <div class="feature">
                    <h3>🎯 Intelligent Assessment</h3>
                    <p>Receive detailed feedback on mathematical rigor, proof quality, and algorithmic innovation. Learn from failure with adaptive hints.</p>
                </div>
                
                <div class="feature">
                    <h3>🚀 Real Innovation</h3>
                    <p>Derive algorithms from mathematical principles. Discover optimizations through mathematical insight. Create, don't just code.</p>
                </div>
            </div>
            
            <div class="api-links">
                <h3>🔗 API Endpoints</h3>
                <a href="/docs">API Documentation</a>
                <a href="/api/challenges">View Challenges</a>
                <a href="/redoc">Alternative Docs</a>
            </div>
        </body>
        </html>
        """
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "mathematics-coding-az"}
    
    return app


def main():
    """Run the development server."""
    app = create_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()