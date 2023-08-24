# EXTRACT H1B DATA BASED ON OCCUPATION

Automate data extraction (employer (sponsor), number of applicants, and average salary) process from the H1B website based on occupation.
URL: https://www.myvisajobs.com/Reports/2023-H1B-Visa-Category.aspx?T=OC

## Description

This program is intended to facilitate the data extraction from the H1B website using the Selenium package.

When navigating to the URL, there is a list of occupations (a total of 199 rows) in a table where each occupation is clickable (hyperlink). Clicking on an occupation link leads to a page displaying every employer who sponsors individuals with that specific occupation.

The program will click on each row in the occupation table on every page and extract data about employers (sponsors), the number of applicants, and the average salary. The output will include the employer's name, number of applicants, average salary, and the occupation sponsored by the employer. The program can be reused to extract other data from this website.

The extracted output can be utilized for in-depth data analysis and visualization, including:
1. Identifying occupations more likely to be sponsored through H1B.
2. Identifying employers more likely to sponsor based on the listed occupations.
3. Analyzing the average salaries of occupations sponsored through H1B.

## Getting Started

### Dependencies

* Python 3.x
* Selenium package ver. 4.11.2
* Adblocker extension crx file (extension_5_8_1_0.crx)
* List of H1B occupation csv file

### Installing

1. Create a folder on your local computer.
2. Copy and paste the crx and csv files into the folder.
3. Create a .py file with any name (ensure both crx and csv files are in the same folder).
4. Copy and paste the Python code into the .py file.

### Executing program

How to run the program:
* [Line 33] Replace the 'path' variable in the code with the path to the crx file (the format should look like this: 'C:/Users/username/Downloads/extension_5_8_1_0.crx').
* [Line 224] Rename the file if necessary (optional).
* Run the program.

## Help

**FAQ:**

Q: Chromedriver is only compatible with version 14, but I have Chromedriver version 16.
A: Update your Selenium to version 4.11.2 (pip install -U selenium==4.11.2).

Q: The pop-up ads from the URL are not allowing me to extract data.
A: Make sure the crx file works. You'll know if the crx file works if the adblocker installation page shows up. It might take some time to finish downloading the adblocker. If you need more time, go to line 227 and increase the number (currently set to 12).

Q: The code is running, but it suddenly stops extracting.
A: Ensure that the device is set to high performance and plugged in, as the code will run for approximately 1 hour, depending on your device.

Q: The program is stuck, and I want to continue extracting data from where it stopped.
A: 1. Check the CSV file where it stops. For example, if it stops at occupation 'Material Scientists' (row 82 or index 80), you can delete the data up to the last completed data extraction. 2. Change the 'occ_row' variable based on the index number (referring to the occupation CSV file). 3. Change the 'occ_page' variable based on the page the occupation is on (e.g., occupation = 'Material Scientist' at row 82 corresponds to pages 51 - 100 or occ_page = 3). 4. Go to line 231, highlight the code, and CTRL + / to avoid extra header. Refer to line 36 for more details on the page indexing.

If you encounter any other errors, please contact me (contact details below).

## Authors

Contributor's name and contact information:

Name: Steven Gilbert
Email: stevenjgilb@gmail.com
Linkedin: www.linkedin.com/in/stevenjgilb

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the Berkely Software Distribution (BSD) License - see the LICENSE.md file for details.

## Acknowledgments

Inspiration
* [Tinkernut](https://www.youtube.com/watch?v=tRNwTXeJ75U&t=299s&ab_channel=Tinkernut)

Data source
* [Myvisajobs.com](https://www.myvisajobs.com/)