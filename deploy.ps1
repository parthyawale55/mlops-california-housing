# Stop and remove any existing container
docker stop mlops-housing-app
docker rm mlops-housing-app

# Pull the latest image
docker pull pdyawale/mlops-housing-app:latest

# Run the container with volume mapping for logs
docker run -d `
  --name mlops-housing-app `
  -p 8000:8000 `
  -v "${PWD}/logs:/app/logs" `
  pdyawale/mlops-housing-app:latest
