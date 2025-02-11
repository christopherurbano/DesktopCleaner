How to Use This Script
Save the script to a file, for example desktop_cleaner.py.

Open a terminal or command prompt and navigate to the directory containing desktop_cleaner.py.

Run the script with the desired options. For example:

To sort files on your Desktop:
python desktop_cleaner.py --sort

To remove duplicate files on your Desktop:
python desktop_cleaner.py --dedupe

To remove files older than 60 days:
python desktop_cleaner.py --remove-old 60

To combine functionalities (e.g., sort and remove duplicates):
python desktop_cleaner.py --sort --dedupe

Optional: If you want to clean a different folder (not the default Desktop), use the --path argument:
python desktop_cleaner.py --path "C:/Your/Custom/Path" --sort
