# winter_research
Chat UI for research project

1. *git clone* <repository>
2. *cd winter_research*
3. *cd docker*
4. *docker build . --tag winter*
5. *cd ..*
5a. check the permissions of the app.db and potentially change them *chmod 764 app.db*
6. ./start_script <container_name> <port_number> (i.e. ./start_script research 1111)
7. python -m winter
8. http://0.0.0.0:5000/1
9. http://0.0.0.0:5000/2
