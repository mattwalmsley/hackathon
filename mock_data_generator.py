import csv
import random
from datetime import datetime, timedelta

from faker import Faker

from mock_data import industry_product_dict, region_country_dict, bank_departments, deal_types

# Define mock data date range
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 1, 1)
delta = timedelta(days=90)

# Define mock data size
ROWS_OF_DATA = 100
EMPLOYEES = 30
COMPANIES = 40
MAX_CLIENTS_PER_COMPANY = 5
MAX_IDEAL_CLIENTS_PER_EMPLOYEE = 5
MAX_EMPLOYEE_EXPERIENCE = 25
MAX_YEARS_WITH_BANK = 75

# Define CSV header rows
deals_header = ['Deal ID', 'Product', 'Country', 'Client (Person)', 'Client (Company)', 'Bank Employee Contact',
                'Start Date',
                'End Date', 'Deal Type']

clients_header = ['Client Name', 'Company', 'Industry', 'Region', 'Years with Bank']

employees_header = ['Employee Name', 'Company Department', 'Industry', 'Region', 'Client Capacity (Count)',
                    'Experience (Years)', 'Designation']

# Set up fake data generator
fake = Faker()


def get_names(count):
    names = []
    while len(names) < count:
        names.append(fake.unique.name())
    return names


def populate_mock_data():
    # company and client data
    while len(company_client_dict) < COMPANIES:
        company_name = fake.unique.company()

        # populate companies with clients
        temp_client_names = get_names(random.randint(1, MAX_CLIENTS_PER_COMPANY))
        company_client_dict[company_name] = temp_client_names
        for name in temp_client_names:
            client_names.append(name)

        # populate companies with regions
        company_region_dict[company_name] = random.choice(list(region_country_dict.keys()))

        # populate companies with industries
        company_industry_dict[company_name] = random.choice(list(industry_product_dict.keys()))

    # bank employee contacts
    for employee_name in employee_names:
        employee_designation_dict[employee_name] = random.choice(deal_types)
        employee_department_dict[employee_name] = random.choice(bank_departments)
        employee_industry_dict[employee_name] = random.choice(list(industry_product_dict.keys()))
        employee_region_dict[employee_name] = random.choice(list(region_country_dict.keys()))


def generate_deals():
    data = []
    for row in range(ROWS_OF_DATA):

        if company_client_dict is None:
            return

        # Choose random company and assign mock data
        while True:
            company = random.choice(list(company_client_dict.keys()))
            client_name = random.choice(company_client_dict[company])
            industry = company_industry_dict[company]
            product = random.choice(industry_product_dict[industry])
            region = company_region_dict[company]
            country = random.choice(region_country_dict[region])
            bank_employee_contact = random.choice(employee_names)

            # only break when bank employee contact is suitable
            if (industry == employee_industry_dict[bank_employee_contact]
                    and region == employee_region_dict[bank_employee_contact]):
                client_employee_dict[client_name] = bank_employee_contact
                break

        deal_type = employee_designation_dict[bank_employee_contact]

        # Choose deal type based on bank employee contact designation

        # Choose random start and end dates
        while True:
            deal_start = datetime.combine(fake.date_between_dates(date_start=start_date, date_end=end_date),
                                          datetime.min.time())
            deal_end = deal_start + delta

            if deal_end <= end_date:
                break

        # Append data row
        data.append([
            row + 1, product, country, client_name, company, bank_employee_contact, deal_start.strftime('%Y-%m-%d'),
            deal_end.strftime('%Y-%m-%d'), deal_type
        ])

    return data


def generate_employees():
    data = []
    for employee in client_employee_dict.values():
        data.append([
            employee, employee_department_dict[employee], employee_industry_dict[employee],
            employee_region_dict[employee], random.randint(1, MAX_IDEAL_CLIENTS_PER_EMPLOYEE),
            random.randint(1, MAX_EMPLOYEE_EXPERIENCE), employee_designation_dict[employee]
        ])
    return data


def generate_clients():
    data = []
    for company, clients in company_client_dict.items():
        for client_name in clients:
            data.append([
                client_name, company, company_industry_dict[company],
                company_region_dict[company], random.randint(1, MAX_YEARS_WITH_BANK)
            ])
    return data


def write_to_csv(filename, headers, data):
    # Write to CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"{filename} generated!")


if __name__ == '__main__':
    # define mock data structures
    client_names = []
    employee_names = get_names(EMPLOYEES)
    company_client_dict = {}
    company_industry_dict = {}
    company_region_dict = {}
    client_employee_dict = {}
    employee_department_dict = {}
    employee_designation_dict = {}
    employee_industry_dict = {}
    employee_region_dict = {}

    populate_mock_data()

    write_to_csv("deals.csv", deals_header, generate_deals())
    write_to_csv("clients.csv", clients_header, generate_clients())
    write_to_csv("employees.csv", employees_header, generate_employees())
