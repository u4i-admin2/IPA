mkdir prisoners/fixtures/ | true
./manage.py dumpdata prisoners --indent=4 --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --output prisoners/fixtures/prisoners.json
mkdir prisons/fixtures/ | true
./manage.py dumpdata prisons --indent=4 --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --output prisons/fixtures/prisons.json
mkdir core_types/fixtures/ | true
./manage.py dumpdata core_types --indent=4 --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --output core_types/fixtures/core_types.json
mkdir api/fixtures/ | true
./manage.py dumpdata api --indent=4 --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --output api/fixtures/api.json
mkdir judges/fixtures/ | true
./manage.py dumpdata judges --indent=4 --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --output judges/fixtures/judges.json
mkdir public/fixtures/ | true
./manage.py dumpdata public --indent=4 --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --output public/fixtures/public.json
mkdir report/fixtures/ | true
./manage.py dumpdata report --indent=4 --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --output report/fixtures/report.json
