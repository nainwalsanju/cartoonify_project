echo "BUILD_START"
python3.10 -m pip install - requirements.txt
python3.10 manage.py collectstatic --noinput --clear
echo "BUILD_END"

