# !/bin/bash
py manage.py migrate
fixtures=$(ls seed/)
while IFS= read -r fixture; do
    echo -n "Seeding "
    echo $fixture
    py manage.py loaddata seed/$fixture
done <<< "$fixtures"