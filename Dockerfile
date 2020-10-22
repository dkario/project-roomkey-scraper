FROM nikolaik/python-nodejs:python3.7-nodejs14

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install -g serverless

RUN npm ci

COPY . .

CMD [ "sls", "deploy" ]
