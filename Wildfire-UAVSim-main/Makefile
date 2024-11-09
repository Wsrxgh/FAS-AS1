.PHONY: 
	build

run:build
	docker run -it --name Wildfire-UAVSimContainer -v .:/code -p 8521:8521 -p 55555:55555 wildfire-uvasim-image:latest

build:remove
	docker build -t wildfire-uvasim-image:latest .

runFirst:buildFirst
	docker run -it --name Wildfire-UAVSimContainer -v .:/code -p 8521:8521 -p 55555:55555 wildfire-uvasim-image:latest

buildFirst:
	docker build -t wildfire-uvasim-image:latest .

restart:
	docker restart Wildfire-UAVSimContainer
	docker attach Wildfire-UAVSimContainer

remove:
	docker rm Wildfire-UAVSimContainer

clean:remove
	docker rmi wildfire-uvasim-image

stop:
	docker stop Wildfire-UAVSimContainer
