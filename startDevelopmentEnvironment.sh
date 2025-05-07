#!/bin/bash
function failIfNotSuccess(){
	if [ $1 -ne 0 ]; then
		echo $2
		pushd -0 && dirs -c > /dev/null
		exit 1
	fi
}

if [ -f /.dockerenv ]; then
   echo "You can not start the development environment inside a docker container"
else
	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
	pushd $DIR >/dev/null

    # Build Master Of VALAWAI
	pushd ../ >/dev/null
	if [ ! -d MOV ]; then
		
		if [ -z "$(docker images -q valawai/mov:latest 2> /dev/null)" ]; then
			echo "Cannot found the MOV docker image"
			pushd -0 && dirs -c > /dev/null
			exit 1
		fi

	else
		pushd MOV >/dev/null
		if [ -z "$(docker images -q valawai/mov:latest 2> /dev/null)" ]; then

			./buildDockerImages.sh latest
			failIfNotSuccess $? "Cannot create the MOV image"

		else
				
			SRC_DATE=$(TZ=UTC0 git log -1 --quiet --date=local --format="%cd" --date=format-local:'%Y-%m-%dT%H:%M:%S.000000000Z')
			IMG_DATE=$(docker inspect -f '{{ .Created }}' valawai/mov:latest)
			if [[ $SRC_DATE > $IMG_DATE ]]; then
				# The image is older that the last modified file

				./buildDockerImages.sh latest
				failIfNotSuccess $? "Cannot create the MOV image"
			fi
		fi
		popd >/dev/null
	fi
    popd >/dev/null

	DOCKER_ARGS=""
	if [ "no-cache" = "$1" ];
	then
		DOCKER_ARGS="$DOCKER_ARGS --no-cache"
		if [ -e .env ];
		then
			source .env
		fi
		rm -rf ${MONGO_LOCAL_DATA:-~/mongo_data/eduteamsDB}
	fi
	DOCKER_BUILDKIT=1 docker build $DOCKER_ARGS --pull -f docker/dev/Dockerfile -t valawai/c1_echo_example_with_python_and_pika:dev .
	if [ $? -eq 0 ]; then
		docker compose -f docker/dev/docker-compose.yaml up -d
		failIfNotSuccess $? "Cannot start the required services"
		
		DOCKER_PARAMS="--rm --name c1_echo_example_with_python_and_pika_dev --add-host=host.docker.internal:host-gateway -v /var/run/docker.sock:/var/run/docker.sock -it"
		if [[ "$OSTYPE" == "darwin"* ]]; then
			DOCKER_PARAMS="$DOCKER_PARAMS -e TESTCONTAINERS_HOST_OVERRIDE=docker.for.mac.host.internal"
		fi
		docker run $DOCKER_PARAMS -v "${PWD}":/app valawai/c1_echo_example_with_python_and_pika:dev /bin/bash
		./stopDevelopmentEnvironment.sh
	fi
	popd >/dev/null
fi
