from bs4 import BeautifulSoup
import requests

class ScrapeJobs:
    def __init__(self, role, location = None):
        self.role = '+'.join(role.split())
        if location != None:
            self.location = '+'.join(location.split())
        else:
            self.location = ''
        self.base = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords='
        self.url = self.base+self.role+'&txtLocation='+self.location

        self.unfamiliar_skills = input("Enter a skill / skills you are unfamiliar with: ")
        self.unfamiliar_skills = [i.strip() for i in self.unfamiliar_skills.split(',')]
        if self.unfamiliar_skills == ['']:
            self.unfamiliar_skills = []

    def save_jobs(self, f):
        self.filter_count = 0
        for i in self.unfamiliar_skills:
            if i in self.skills:
                self.filter_count += 1

        if self.filter_count == 0 or self.unfamiliar_skills == []:
            f.write(f"Company Name: {self.company_name} \n")
            f.write(f"Experience: {self.experience} \n")
            f.write(f"Location: {self.location} \n")
            f.write(f"Skills Required: {self.skills} \n")
            f.write(f"Publish Date: {self.published_date} \n")
            f.write(f"More Info: {self.more_info} \n")
            f.write("\n")
            f.write('-' * 200)
            f.write("\n")
        else:
            pass

    def scrape(self):
        self.source = requests.get(self.url).text
        self.soup = BeautifulSoup(self.source, 'lxml')
        self.filename = self.role + ' jobs'
        with open(self.filename+'.txt', 'w') as f:
            for index,job in enumerate(self.soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')):
                self.company_name = job.header.find('h3', class_ = 'joblist-comp-name').text.strip()
                self.experience = job.find('ul').li.text.split('l')[1].strip()
                self.location = job.find('ul', class_ = 'top-jd-dtl clearfix').span.text.strip()
                self.skills = job.find('span', class_ = 'srp-skills').text.replace(' ', '').strip()
                self.published_date = job.find('span', class_ = 'sim-posted').span.text.strip()
                self.more_info = job.header.h2.a['href']
                self.save_jobs(f)
        f.close()
        print("File saved successfully.")


if __name__ == '__main__':
    job = ScrapeJobs('Python Developer', 'Pune')
    job.scrape()


# >> Enter a skill / skills you are unfamiliar with: linux, javascript
# >> File saved successfully.
