pass="foo"
containerName="ad-bot"
networkName="custom0"
localPort=6000
containerPort=5000
imageName="ad-bot"
tag="latest"

# Tagging to push image to a cloud registry
# $repo = "ta4h1r"
# docker tag $imageName:$tag $repo/$imageName:$tag
# docker push $repo/$imageName:$tag

echo $pass | sudo docker build -t $imageName:$tag .
echo $pass | sudo docker run -itd --name=$containerName --network=$networkName --restart unless-stopped -p $localPort:$containerPort $imageName:$tag
