# Image Captioning
**A Django App for image captioning (PyTorch)**

- [Image Captioning](#image-captioning)
  - [Live Demo](#live-demo)
  - [Install](#install)
  - [Deployment on Heroku](#deployment-on-heroku)
    - [Git-based deployment](#git-based-deployment)
    - [Docker-based Deployment(Ours)](#docker-based-deploymentours)
      - [Local Test](#local-test)
      - [Heroku Deployment Using Container Registry](#heroku-deployment-using-container-registry)
  - [Model](#model)

## Live Demo

[看图说话 (img-captioning.herokuapp.com)](https://img-captioning.herokuapp.com/)

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
you can find more information in Dockerfile. Since I'm new to docker, the docker image may be redundent and relatively big. PRs are welcome.

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

3. set secret key for Django in Heroku

   ```bash
   heroku config:set DJANGO_SECRET_KEY=<SOME_SECRET_VALUE> -a limitless-atoll-51647
   ```

4. add Heroku url to `ALLOWED_HOSTS` in `./pytorch_django/setting.py`

   ```python
   ALLOWED_HOSTS = ['<your_app_name>.herokuapp.com']
   ```

5. Login, build docker image, Push docker image and release(it may take minutes to push image)

   ```bash
   heroku container:login -i
   docker build -t registry.heroku.com/<your_app_name>/web .
   docker push registry.heroku.com/<your_app_name>/web
   heroku container:release -a <your_app_name> web
   ```

6. Finally, you can view your app running in Heroku https://APP_NAME.herokuapp.com

## Model

paper:["Show and Tell: A Neural Image Caption Generator" by Vinayls et al. (ICML2015)](https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Vinyals_Show_and_Tell_2015_CVPR_paper.pdf)

Use ResNet-152 to encode a 224*224 RGB picture as a 256-dim embedding, then use a LSTM model to decode. Origin model is trained in MSCOCO dataset.

You can modify models by changing `image/image_captioning/models.py` as well as `image_captioning.py`. Model parameters can be found in `static/*`.



