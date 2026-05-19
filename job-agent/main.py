from modules.resume_parser import parse_resume
from modules.job_scraper import scrape_jobs
from modules.matcher import match_jobs
from modules.generator import generate_content
from modules.tracker import init_db, save_application, get_all_applications

MATCH_THRESHOLD = 70

def run_agent(job_title, num_jobs=10):
    print("=" * 50)
    print("   AI JOB APPLICATION AGENT")
    print("=" * 50)

    # Step 1 - Parse resume
    print("\n[1/4] Parsing your resume...")
    resume = parse_resume()
    print(f"      Hello {resume['name']}! Resume parsed successfully.")

    # Step 2 - Scrape jobs
    print(f"\n[2/4] Searching for '{job_title}' jobs...")
    jobs = scrape_jobs(job_title, num_jobs=num_jobs)
    print(f"      Found {len(jobs)} jobs")

    # Step 3 - Init database
    init_db()

    # Step 4 - Process each job
    print(f"\n[3/4] Matching and generating applications...")
    print(f"      Threshold: {MATCH_THRESHOLD}/100\n")

    saved = 0
    skipped = 0

    for i, job in enumerate(jobs):
        print(f"  [{i+1}/{len(jobs)}] {job['title']} at {job['company']}")

        # Match
        match_result = match_jobs(resume, job)
        score = match_result["match_score"]
        print(f"         Score: {score}/100", end=" ")

        if score < MATCH_THRESHOLD:
            print("-> Skipped")
            skipped += 1
            continue

        print("-> Generating...")

        # Generate cover letter + bullets
        content_result = generate_content(resume, job)

        # Save to tracker
        save_application(job, match_result, content_result)
        saved += 1

    # Step 5 - Summary
    print(f"\n[4/4] Done!")
    print(f"      Saved   : {saved} applications")
    print(f"      Skipped : {skipped} jobs (below threshold)")

    print("\n--- YOUR APPLICATIONS ---")
    for row in get_all_applications():
        print(f"  [{row[0]}] {row[2]} at {row[1]} | Score: {row[3]} | Status: {row[4]} | Date: {row[5]}")

    print("\nOpen applications.db to read full cover letters.")
    print("=" * 50)

if __name__ == "__main__":
    run_agent(
        job_title="python developer",
        num_jobs=10
    )