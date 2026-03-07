import os

base_dir = "/Volumes/Workspace/projects/campustab/data-service/app"
dirs = ["models", "api/routes", "schemas", "core", "services"]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

with open(os.path.join(base_dir, "models/database.py"), "w") as f:
    f.write("""from sqlalchemy.orm import declarative_base

Base = declarative_base()
""")

with open(os.path.join(base_dir, "api/routes/internal_crawl.py"), "w") as f:
    f.write("""from fastapi import APIRouter

router = APIRouter()

@router.post('/internal/crawl')
def trigger_crawl():
    # TODO: Implement crawl trigger
    return {'status': 'queued/success', 'job_id': 'temporary-id'}
""")

with open(os.path.join(base_dir, "main.py"), "w") as f:
    f.write("""from fastapi import FastAPI
from app.api.routes import internal_crawl

app = FastAPI(title="CampusTab Data Service")

app.include_router(internal_crawl.router, prefix='/api/v1')
""")

# Create init files to make them modules
for d in dirs + ["api", ""]:
    init_path = os.path.join(base_dir, d, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            pass

print("✅ FastAPI (data-service) scaffolding generated successfully.")
