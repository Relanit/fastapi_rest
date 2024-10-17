from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from authors.router import get_authors

router = APIRouter(prefix="/pages", tags=["Pages"])


templates = Jinja2Templates(directory="templates")


@router.get("/authors")
def get_search_page(request: Request, authors=Depends(get_authors)):
    return templates.TemplateResponse("authors.html", {"request": request, "authors": authors["data"]})
