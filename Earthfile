VERSION 0.6
FROM ubuntu:jammy

dockerfile:
  FROM DOCKERFILE .
  SAVE IMAGE starlight

up:
    LOCALLY
    WITH DOCKER --load=+dockerfile
        RUN docker run -e DISCORD_API_KEY=$DISCORD_API_KEY -e GUILD_ID=$GUILD_ID -v $(pwd)/data:/data --rm starlight:latest
    END
