from modules.llama_helper import ask_llama
import json

def match_jobs(resume_data,job):
    prompt = f"""You are a job matching assistant.
    Compare this resume against the job and return a JSON object.

    Return ONLY valid JSON. No explanation. No markdown.

    Required keys:
    - "match_score" (integer between 0 and 100)
    - "match_reason" (one short sentence why)
    - "missing_skills" (list of strings, skills in job but not in resume)

    Resume:
    Name: {resume_data['name']}
    Skills: {', '.join(resume_data['skills'])}
    Experience: {json.dumps(resume_data['experience'])}
    Education: {resume_data['education']}

    Job Title: {job['title']}
    Company: {job['company']}
    Description: {job['description']}"""
    result=ask_llama(prompt,expect_json=True)
    return result


if __name__ == "__main__":
    from modules.resume_parser import parse_resume
    from modules.job_scraper import scrape_jobs

    print("Parsing resume...")
    resume = parse_resume()

    print("Fetching jobs...")
    jobs = scrape_jobs("python developer", num_jobs=3)

    print("\nMatching jobs...\n")
    for job in jobs:
        print(f"Job   : {job['title']} at {job['company']}")
        result = match_jobs(resume, job)
        print(f"Score : {result['match_score']}")
        print(f"Reason: {result['match_reason']}")
        print(f"Missing: {result['missing_skills']}")
        print("---")