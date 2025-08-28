from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
import os
import uuid
import asyncio

from crewai import Crew, Process
from sqlalchemy.orm import Session
from db import init_db, get_db
from models import Analysis
from agents import doctor
from task import help_patients

app = FastAPI(title="Blood Test Report Analyser")

@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/analyses")
def list_analyses(db: Session = Depends(get_db)):
    rows = db.query(Analysis).order_by(Analysis.id.desc()).limit(50).all()
    return [
        {
            "id": r.id,
            "file_name": r.file_name,
            "query": r.query,
            "created_at": r.created_at.isoformat()
        }
        for r in rows
    ]


@app.get("/analyses/{analysis_id}")
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    row = db.get(Analysis, analysis_id)
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {
        "id": row.id,
        "file_name": row.file_name,
        "query": row.query,
        "analysis": row.analysis,
        "created_at": row.created_at.isoformat()
    }

def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew"""
    medical_crew = Crew(
        agents=[doctor],
        tasks=[help_patients],
        process=Process.sequential,
    )
    
    result = medical_crew.kickoff({'query': query})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report"),
    db: Session = Depends(get_db)
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if query=="" or query is None:
            query = "Summarise my Blood Test Report"
            
        # Process the blood report with all specialists
        response = run_crew(query=query.strip(), file_path=file_path)
        
        # Persist analysis
        record = Analysis(
            file_name=file.filename,
            query=query.strip(),
            analysis=str(response)
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "status": "success",
            "id": record.id,
            "query": query,
            "analysis": record.analysis,
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)