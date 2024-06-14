from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import base64, os
from .cf_bypass import CloudflareBypass

app = FastAPI(
    title="Backend API",
    summary="Backend API for the frontend",
    version="0.1.0",
    docs_url="/api/",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.get("/api/greet")


def greet():
    """Returns a greeting"""
    return {"message": "Hello from the backend!"}


@app.get("/api/ahref/kd/")
async def getAhrefKD(keywords: str = Query(...)):
    # Base64 decode the keywords
    keyword = base64.urlsafe_b64decode(keywords.encode()).decode()

    if keyword:
        path = "/tmp/chromium"
        path = "/vercel/.cache/puppeteer/chrome/linux-123.0.6312.86"

        cloudflare_bypass = None
        # Try each path in sequence until a valid one is found

        # Check if the path exists
        if os.path.exists(path):
            print("tmp is found")
            # List all files and directories in the path
            files_and_dirs = os.listdir(path)

            # Filter out directories and only list files
            files = [f for f in files_and_dirs if os.path.isfile(os.path.join(path, f))]

            # Print all files
            for file in files:
                print(file)
            cloudflare_bypass = CloudflareBypass(browser_path=path)

        else:
            print("The path does not exist")
            cloudflare_bypass = CloudflareBypass(browser_path=None)

        # co = ChromiumOptions().set_browser_path(path).auto_port()
        # page1 = ChromiumPage(co)
        page1 = cloudflare_bypass.driver
        url = "https://ahrefs.com/keyword-difficulty/"
        if "," in keyword:
            keywords = keyword.split(",")
        else:
            keywords = [keyword]
        datas = []
        if keyword in keywords:
            page1.get(url)
            # keyword = "remini.ai"
            page1.ele("@placeholder=Enter keyword").input(keyword)

            # 点击登录按钮
            page1.ele("text=Check keyword").click()
            cookies = cloudflare_bypass.bypass(url)

            kd = page1.ele(".css-16bvajg-chartValue").text

            kds = page1.ele(".css-1wi5h2-row css-1crciv5 css-6rbp9c").text
            #     print(kd)
            #     print(kds)
            data = {"keyword": keyword, "kd": kd, "des": kds}
            datas.append(data)

            return data
    else:
        return []
