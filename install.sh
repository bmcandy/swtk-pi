# Install docker & docker compose
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
# Add user to docker group
sudo usermod -aG docker $USER
# Build docker containers
docker-compose build