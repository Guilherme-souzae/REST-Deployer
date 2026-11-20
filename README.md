# REST-Deployer

PUSH TEST

Installation instructions

> The commands below assume **Ubuntu Server 22.04 or 24.04** on both EC2 instances.

# The following infrastructure should be created in AWS

- One Security Group for Jenkins with:
  - SSH open for MyIP
  - 8080 open for AnyIP
- One Security Group for API with:
  - SSH open for MyIP and Jenkins
  - 5000 open for AnyIP

Then create two EC2 instances, one each one with a created SG.
After this you should prepare the instances to run the containers and fetch
the content from Github.

## Jenkins instance

Log in the Jenkins instance and run the following script:

```bash
# Install Git and Docker's official repository dependencies
sudo apt-get update
sudo apt-get install -y git ca-certificates curl

# Add Docker's official GPG key and repository
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine and Docker Compose (plugin)
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin

# Start Docker on boot and allow the current user to run it without sudo
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

Log out and log in again so the new group takes effect, then check the installation:

```bash
git --version
docker --version
docker compose version
```

Prepare the Jenkins home folder (it is bind-mounted at the same path inside and
outside the container, so Docker volumes started by Jenkins resolve correctly)
and download the repository:

```bash
sudo mkdir -p /var/jenkins_home
sudo chown -R 1000:1000 /var/jenkins_home

git clone https://github.com/Guilherme-souzae/REST-Deployer.git
cd REST-Deployer/jenkins
```

Jenkins needs access to the host's Docker socket to run Newman containers.
Get the GID of the host's `docker` group and use it in the `group_add` field of
`docker-compose.yml`:

```bash
getent group docker | cut -d: -f3
```

Finally, start Jenkins:

```bash
sudo docker compose up -d --build
```

The Jenkins intance should be well prepared

## API instance

Log in the API instance and run the following script:

```bash
# Install Git and Docker's official repository dependencies
sudo apt-get update
sudo apt-get install -y git ca-certificates curl

# Add Docker's official GPG key and repository
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Start Docker on boot and allow the current user to run it without sudo
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

Log out and log in again, then check the installation:

```bash
git --version
docker --version
```

Jenkins deploys over SSH, so the **public** key that matches the SSH private
key saved in Jenkins must be present on this instance:

```bash
echo "<PUBLIC_KEY_CONTENT>" >> ~/.ssh/authorized_keys
```

The API instance should be well prepared

The infrasctucture is ready, just get then both public IPS in order to acess the API
setup the Jenkins Environment

# Jenkins configuration
Log in into the Jenkins mainpage by using the Jenkins EC2 Instance public IP address
followed by the 8080 port.

The default User and Password are both CHANGEME, you should change them after logging in
You should then just save env credentials on Jenkins, go to the credentials page on Jenkins
and save the following content:
- SSH key
- FlaskAPI IP
- SourceEmail Address
- TargetEmail Address

The system is now working! You should be able to perform the CICD pipeline manually by running
the Jenkins Job.

# Webhook
Finally, in order to automate the CICD pipeline, create a weebhook targeted to the Jenkins
IP address.