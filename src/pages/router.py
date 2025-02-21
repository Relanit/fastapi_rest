from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from companies.router import get_companies

router = APIRouter(prefix="/pages", tags=["Pages"])


templates = Jinja2Templates(directory="templates")


@router.get("/companies")
def get_companies_page(request: Request, companies=Depends(get_companies)):
    return templates.TemplateResponse("companies.html", {"request": request, "companies": companies})
