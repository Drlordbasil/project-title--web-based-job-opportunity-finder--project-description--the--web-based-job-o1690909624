import requests
from bs4 import BeautifulSoup


class JobOpportunityFinder:
    def __init__(self):
        self.base_url = "https://example.com/jobs"
        self.company_api_url = "https://api.example.com/company/{}"

    def fetch_job_listings(self) -> list:
        """
        Fetches job listings from a website using web scraping technique.
        Sends a GET request to the website and parses the HTML using BeautifulSoup.
        Extracts relevant information such as job title, company name, and job description.
        Returns a list of job listings.
        """
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        job_listings = []

        listings = soup.find_all('div', class_='job-listing')

        for listing in listings:
            title = listing.find('h2', class_='job-title').text.strip()
            company = listing.find('div', class_='company-name').text.strip()
            description = listing.find(
                'div', class_='job-description').text.strip()

            job_listings.append(
                {'title': title, 'company': company, 'description': description})

        return job_listings

    def filter_job_listings(self, job_listings: list, keyword: str) -> list:
        """
        Filters job listings based on a given keyword.
        Takes a list of job listings and returns only the listings that contain the keyword in the title or description.
        """
        filtered_listings = [listing for listing in job_listings if keyword.lower(
        ) in listing['title'].lower() or keyword.lower() in listing['description'].lower()]
        return filtered_listings

    def fetch_company_info(self, company_name: str) -> dict:
        """
        Fetches additional information about a company using an external API.
        Takes a company name as input and sends a GET request to the API to fetch the information.
        Returns the company information as a dictionary.
        """
        url = self.company_api_url.format(company_name)
        response = requests.get(url)
        company_info = response.json()

        return company_info

    def save_job_opportunities(self, filtered_listings: list) -> None:
        """
        Saves the filtered job opportunities to a file.
        Creates a new file and writes each job listing as a separate line in a structured format.
        """
        with open('job_opportunities.txt', 'w') as file:
            for listing in filtered_listings:
                file.write(f"Title: {listing['title']}\n")
                file.write(f"Company: {listing['company']}\n")
                file.write(f"Description: {listing['description']}\n")
                file.write("\n")

    def main(self) -> None:
        print("Welcome to the Web-Based Job Opportunity Finder!\n")
        keyword = input(
            "Please enter a keyword to search for job opportunities: ")
        job_listings = self.fetch_job_listings()
        filtered_listings = self.filter_job_listings(job_listings, keyword)

        if filtered_listings:
            self.save_job_opportunities(filtered_listings)
            print(
                f"\n{len(filtered_listings)} job opportunities found and saved in 'job_opportunities.txt'.")
            choice = input(
                "Do you want to fetch additional information about the companies? (yes/no): ")

            if choice.lower() == 'yes':
                for listing in filtered_listings:
                    company_info = self.fetch_company_info(listing['company'])
                    print(
                        f"\nAdditional Information about {listing['company']}:\n")
                    print(f"Location: {company_info['location']}")
                    print(f"Website: {company_info['website']}")
                    print(f"Size: {company_info['size']}")
                    print(f"Industry: {company_info['industry']}")
        else:
            print("No job opportunities found for the given keyword.")


if __name__ == "__main__":
    finder = JobOpportunityFinder()
    finder.main()
