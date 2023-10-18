FROM gradle:jdk11-alpine as builder

WORKDIR /app
COPY ./build.gradle /app/build.gradle
COPY ./src /app/src
COPY ./version.txt /app/version.txt
COPY ./www /app/www

RUN gradle jarCli
RUN gradle copyWww

FROM adoptopenjdk/openjdk11:alpine-jre

COPY --from=builder /app/build/libs/MinecraftStatsCLI.jar /app/MinecraftStatsCLI.jar
# copy from raw_www to www in entrypoint.sh
COPY --from=builder /app/build/www /app/raw_www
COPY www /app/raw_www

COPY ./stats /app/stats
COPY ./entrypoint.sh /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

