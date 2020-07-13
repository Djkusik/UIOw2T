FROM node:latest

RUN useradd front

WORKDIR /home/front

COPY package-lock.json package.json yarn.lock ./

RUN yarn

COPY public public
COPY src src

# chown freezing, debug later
# RUN chown -R front:front ./
# USER front
