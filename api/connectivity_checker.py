
from fastapi import FastAPI,HTTPException, status
from sql.tables import Website
from services import scheduler

app_connectivity_checker = FastAPI()



@app_connectivity_checker.get("/status/{id}")
async def website_status(id: int):
    website = await Website.select().where(id == Website.id)
    if not website:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Website Not Found")
    url =  website[0]['url']
    url_status = scheduler.task_checker(url)
    result_status = scheduler.task_check_result(url_status, url)
    date = scheduler.get_time()
    if result_status != 'Online!':
        raise HTTPException (status.HTTP_500_INTERNAL_SERVER_ERROR, detail ="Internal Server Error")
    return {'id': id, 'url': url, 'Status': result_status, 'time': date}


if __name__=="__main__":
    app_connectivity_checker.run()