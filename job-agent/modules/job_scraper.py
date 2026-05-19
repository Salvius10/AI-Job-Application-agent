import requests

def scrape_jobs(job_title,num_jobs=10):
    url = f"https://remotive.com/api/remote-jobs?search={job_title}&limit={num_jobs}"
    print(f"Fetching jobs for {job_title}")
    response=requests.get(url)
    data=response.json()
    jobs=[]
    for job in data.get("jobs",[]):
        jobs.append({
            "title": job["title"],
            "company": job["company_name"],
            "description": job["description"][:500],
            "url": job["url"]
        })
    return jobs[:num_jobs]


