VERSION 0.6
FROM ubuntu:jammy

dockerfile:
  FROM DOCKERFILE .

up:
  FROM +dockerfile
  RUN --secret DISCORD_API_KEY --secret GUILD_ID ./start.sh
