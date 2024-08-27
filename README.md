# Cloud Security Event Scraper

==========================

## Description

---

The Cloud Security Event Scraper is a web scraping project built using Scrapy, a Python framework for building web scrapers. The project aims to scrape event data from a specific website and store it in a structured format.

## Installation

---

To install the project, follow these steps:

### Prerequisites

- Python 3.6 or higher
- Scrapy 2.4 or higher

### Installation Steps

1. Clone the repository using Git:
   ```bash
   git clone https://github.com/<your-username>/event_scraper.git
   ```

````
2. Navigate to the project directory:
   ```bash
cd event_scraper
````

3. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. Create the `cloud_security_events` database, create a user in the database and set up the following environment variables:
   ```bash
   export MYSQL_USER="<username>"
   export MYSQL_PWD="<password>"
   ```

````

## Usage
-----

To run the scraper, use the following command:
   ```bash
scrapy crawl eventscraper
````

This will start the scraper and begin extracting event data from the target website.

### Usage Examples

- To scrape events from a specific event type (e.g., webcasts, summits, or series), use the following command:
  ```bash
  scrapy crawl eventscraper -a event_type=webcasts
  ```

````
* To scrape events from multiple event types, use the following command:
   ```bash
scrapy crawl eventscraper -a event_type=webcasts,summits
````

## Contribution

---

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

### Step 1: Fork the Repository

Fork the repository using the "Fork" button on the top-right corner of the repository page.

### Step 2: Create a New Branch

Create a new branch for your feature or bug fix using the following command:

```bash
git checkout -b feature/your-feature-name
```

### Step 3: Make Changes

Make the necessary changes to the code, following the project's coding standards and guidelines.

### Step 4: Commit Changes

Commit your changes using a descriptive commit message:

```bash
git commit -m "Added new feature: your-feature-name"
```

### Step 5: Push Changes

Push your changes to the remote repository:

```bash
git push origin feature/your-feature-name
```

### Step 6: Create a Pull Request

Create a pull request to merge your changes into the main repository.
