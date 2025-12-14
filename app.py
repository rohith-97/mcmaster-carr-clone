import json
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

def cached_response(html, max_age=3600):
    response = HTMLResponse(content=html)
    response.headers["Cache-Control"] = f"public, max-age={max_age}"
    return response

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

with open("data/catalog.json") as f:
    DATA = json.load(f)

@app.get("/")
def home(request: Request):
    html = templates.get_template("home.html").render(
    request=request,
    categories=DATA["categories"].keys()
)
    return cached_response(html, max_age=3600)

  

@app.get("/category/{name}")
def category(request: Request, name: str):
    products = DATA["categories"].get(name, [])
    html = templates.get_template("category.html").render(
    request=request,
    category=name,
    products=products
)
    return cached_response(html, max_age=3600)

    

@app.get("/product/{pid}")
def product(request: Request, pid: str):
    for products in DATA["categories"].values():
        for p in products:
            if p["id"] == pid:
                html = templates.get_template("product.html").render(
                    request=request,
                    product=p
                )
                return cached_response(html, max_age=86400)  # 24 hours

    
            
@app.get("/search")
def search(request: Request, q: str = ""):
    results = []

    if q:
        query = q.lower()
        for category, products in DATA["categories"].items():
            for p in products:
                text = f"{p['name']} {p['keywords']}".lower()
                if query in text:
                    results.append(p)

    html = templates.get_template("search.html").render(
        request=request,
        query=q,
        results=results
    )

    return cached_response(html, max_age=60)  # 1 minute cache
