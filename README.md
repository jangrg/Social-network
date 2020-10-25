backend setup from terminal:

    create database:
        sudo -u postgres psql
        create user janez with password '12345678';
        create database social_network with owner janez;

    django setup:
        cd backend
        mkvirtualenv social-network
        setvirtualenvproject
        pip install -r requirements.txt
        ./manage.py migrate
        ./manage.py runserver

nuxt setup:

    npm i
    npm run dev