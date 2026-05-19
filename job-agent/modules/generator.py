from modules.llama_helper import ask_llama
import json

def generate_content(resume_data,job):
    prompt = f"""You are a professional job application writer.
    Based on the resume and job below, generate application content.

    Return ONLY valid JSON. No explanation. No markdown.

    Required keys:
    - "cover_letter" (string, 2 short paragraphs, personalized to the job)
    - "tailored_bullets" (list of 3 strings, improved resume bullet points using job keywords)

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

    print("Fetching one job...")
    jobs = scrape_jobs("python developer", num_jobs=1)
    job = jobs[0]

    print(f"\nGenerating for: {job['title']} at {job['company']}\n")
    result = generate_content(resume, job)

    print("COVER LETTER:")
    print(result["cover_letter"])
    print("\nTAILORED BULLETS:")
    for bullet in result["tailored_bullets"]:
        print(f"  - {bullet}")