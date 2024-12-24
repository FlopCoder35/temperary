echo "BUILD START"

# Install dependencies using Python's built-in pip3
python3 -m pip install -r requirement.txt
python3 manage.py migrations
python3 manage.py migrate --noinput
# Collect static files for Django
python3 manage.py collectstatic --noinput --clear


# Create the output directory for static files
mkdir -p staticfiles_build

# Move static files to the output directory
mv $(find . -type f -name 'static*') staticfiles_build/

echo "BUILD END"
