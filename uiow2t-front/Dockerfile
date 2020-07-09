FROM node:latest

RUN useradd front

WORKDIR /home/front

COPY public public
COPY src src
COPY package-lock.json package.json yarn.lock ./

RUN yarn

# chown freezing, debug later
# RUN chown -R front:front ./
# USER front