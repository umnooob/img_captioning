# Image Captioning
**A Django App for image captioning (PyTorch)**

## Install

1. Download project

   ```bash
   git clone https://github.com/umnooob/img_captioning.git
   cd ./img_captioning
   ```

2. Set up environment

   ```bash
   conda create -n <env_name>
   pip install -r requirements
   ```

3. Copy all static files from  `STATICFILES_DIRS` to `STATIC_ROOT`

   ```bash
   python manage.py collectstatic
   ```

4. Start Django project

   ```bash
   python manage.py runserver
   ```

5. You will see our Image Captioning App in http://127.0.0.1:8000/

## Deployment on Heroku

### Git-based deployment

You can refer to this [blog](https://stefanbschneider.github.io/blog/pytorch-django) for detailed instructions. Since our deployment will exceed [maximum slug size of 500MB](https://devcenter.heroku.com/articles/slug-compiler#slug-size) , we will use Docker-based Deployment.

If your employment doesn't exceed 500MB and your model params file exceed 200MB, you can use [git lfs](https://git-lfs.github.com/) and this [Heroku Buildpack](https://elements.heroku.com/buildpacks/raxod502/heroku-buildpack-git-lfs) for simple git-based deployment.

### Docker-based Deployment(Ours)

[Reference](https://testdriven.io/blog/deploying-django-to-heroku-with-docker/#heroku-container-runtime)

#### Local Test

1. [Install docker](https://www.docker.com/products/docker-desktop)

2.  build image and spin up a container

   ```bash
   docker build -t web:latest .
   docker run -d --name <container_name> -e "PORT=8765" -e "DEBUG=1" -p 8007:8765 web:latest
   ```

3. You can see App in  http://localhost:8007

4. Remove the running container

   ```bash
   docker stop <container_name>
   docker rm <container_name>
   ```

#### Heroku Deployment Using Container Registry

1. [Sign up](https://signup.heroku.com/) for Heroku account, and then install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) .
2. create a new app in Heroku
3. 
